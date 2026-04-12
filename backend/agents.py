import base64
import json
import os
from typing import Any, cast

import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} environment variable not set")
    return value


OPENROUTER_API_KEY = _get_required_env("OPENROUTER_API_KEY")
OPENROUTER_MODEL = _get_required_env("OPENROUTER_MODEL")


AGENT1_SYSTEM_PROMPT = "You are an ad analyst. Return JSON only. No preamble. No markdown."


def _extract_message_text(response: Any) -> str:
    content = response.choices[0].message.content

    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        chunks: list[str] = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                chunks.append(str(part.get("text", "")))
            else:
                text_value = getattr(part, "text", None)
                if text_value:
                    chunks.append(str(text_value))
        return "".join(chunks)

    return str(content)


def _parse_json_response(response_text: str) -> dict:
    """Parse JSON from response, handling markdown wrapping."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(response_text[start : end + 1])
        raise


def _image_url_to_data_url(image_url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/*,*/*;q=0.8",
    }

    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(image_url, headers=headers)
        response.raise_for_status()

    if len(response.content) > 4_000_000:
        raise ValueError("Ad image is too large; please use a smaller image URL")

    content_type = response.headers.get("content-type", "").split(";")[0].strip()
    if not content_type.startswith("image/"):
        content_type = "image/jpeg"

    image_b64 = base64.b64encode(response.content).decode("ascii")
    return f"data:{content_type};base64,{image_b64}"


def _create_json_completion(
    client: OpenAI,
    model: str,
    messages: list[dict[str, Any]],
    max_tokens: int,
) -> Any:
    typed_messages = cast(Any, messages)

    return client.chat.completions.create(
        model=model,
        messages=typed_messages,
        temperature=0,
        max_tokens=max_tokens,
    )


def _run_with_system_fallback(
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_content: Any,
    max_tokens: int,
) -> Any:
    primary_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    try:
        return _create_json_completion(client, model, primary_messages, max_tokens)
    except Exception as exc:
        error_text = str(exc)
        provider_rejects_system = (
            "developer instruction is not enabled" in error_text.lower()
            or "system instruction" in error_text.lower()
        )
        if not provider_rejects_system:
            raise

        if isinstance(user_content, list):
            merged_user_content = [
                {
                    "type": "text",
                    "text": f"Follow these instructions exactly: {system_prompt}",
                }
            ] + user_content
        else:
            merged_user_content = (
                "Follow these instructions exactly:\n"
                f"{system_prompt}\n\n"
                f"{user_content}"
            )

        fallback_messages = [{"role": "user", "content": merged_user_content}]
        return _create_json_completion(client, model, fallback_messages, max_tokens)


def run_agent1(ad_image_url: str) -> dict:
    """
    Analyze an ad image using vision capabilities via OpenRouter.
    Extracts headline, offer, CTA text, tone, and target audience.
    
    Args:
        ad_image_url: URL of the ad image
        
    Returns:
        Dictionary with extracted ad information or error object
    """
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    def _user_content_for_image(image_source: str) -> list[dict[str, Any]]:
        return [
            {
                "type": "image_url",
                "image_url": {"url": image_source},
            },
            {
                "type": "text",
                "text": (
                    "Extract the following from this ad image and return as compact JSON: "
                    "headline, offer, cta_text, tone (one word), target_audience"
                ),
            },
        ]

    response_text = ""
    try:
        response = _run_with_system_fallback(
            client=client,
            model=OPENROUTER_MODEL,
            system_prompt=AGENT1_SYSTEM_PROMPT,
            user_content=_user_content_for_image(ad_image_url),
            max_tokens=350,
        )

        response_text = _extract_message_text(response)
        parsed = _parse_json_response(response_text)
        return parsed

    except json.JSONDecodeError as first_parse_error:
        # JSON parse failed; return error with raw response for debugging
        return {
            "error": "agent1 parse failed",
            "raw": response_text,
            "details": str(first_parse_error),
        }

    except Exception as e:
        error_text = str(e).lower()
        image_fetch_related = (
            "forbidden" in error_text
            or "no endpoints found that support image input" in error_text
            or "could not download" in error_text
            or "image" in error_text and "url" in error_text
        )

        if image_fetch_related:
            # Image fetch failed; return error
            return {
                "error": f"agent1 failed: {str(e)}",
            }

        return {"error": f"agent1 failed: {str(e)}"}


def run_agent2(ad_json: dict, page_content: str) -> dict:
    """
    Generate personalized landing page copy using CRO expertise via OpenRouter.
    
    Args:
        ad_json: Dictionary with ad analysis from run_agent1
        page_content: Scraped content from the landing page
        
    Returns:
        Dictionary with new headline, subheadline, CTA, and reasoning or error object
    """
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    response_text = ""
    try:
        user_message = f"""
Ad Analysis:
{json.dumps(ad_json, indent=2)}

Landing Page Content:
{page_content[:2000]}

Generate personalized copy for this landing page based on the ad insights. Return as JSON with: new_h1, new_subhead, new_cta, reasoning (one sentence). Only use claims present in the ad. Do not invent features, prices, or benefits.
Keep output concise: new_h1 <= 12 words, new_subhead <= 16 words, new_cta <= 6 words, reasoning <= 14 words.
"""
        
        response = _run_with_system_fallback(
            client=client,
            model=OPENROUTER_MODEL,
            system_prompt=(
                "You are a CRO specialist. Return JSON only. No preamble. No markdown. "
                "Only use claims present in the ad. Do not invent features, prices, or benefits. "
                "Keep outputs concise to avoid truncation."
            ),
            user_content=user_message,
            max_tokens=220,
        )

        response_text = _extract_message_text(response)
        parsed = _parse_json_response(response_text)
        return parsed
        
    except json.JSONDecodeError:
        return {"error": "agent2 parse failed", "raw": response_text}
    except Exception as e:
        return {"error": f"agent2 failed: {str(e)}"}

