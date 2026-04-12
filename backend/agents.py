import base64
import json
import os
from io import BytesIO
from typing import Any

import google.generativeai as genai
import httpx
from dotenv import load_dotenv
from PIL import Image

load_dotenv(override=True)


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} environment variable not set")
    return value


GEMINI_API_KEY = _get_required_env("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

AGENT1_SYSTEM_PROMPT = "You are an ad analyst. Return JSON only. No preamble. No markdown."
AGENT2_SYSTEM_PROMPT = (
    "You are a CRO specialist. Return JSON only. No preamble. No markdown. "
    "Only use claims present in the ad. Do not invent features, prices, or benefits. "
    "Keep outputs concise to avoid truncation."
)



def _fetch_image_as_pil(image_url: str) -> Image.Image:
    """Fetch image from URL and convert to PIL Image."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/*,*/*;q=0.8",
    }

    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(image_url, headers=headers)
        response.raise_for_status()

    if len(response.content) > 4_000_000:
        raise ValueError("Ad image is too large; please use a smaller image URL")

    return Image.open(BytesIO(response.content))


def _image_url_to_base64(image_url: str) -> str:
    """Convert image URL to base64 string."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/*,*/*;q=0.8",
    }

    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(image_url, headers=headers)
        response.raise_for_status()

    if len(response.content) > 4_000_000:
        raise ValueError("Ad image is too large; please use a smaller image URL")

    return base64.b64encode(response.content).decode("ascii")


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


def run_agent1(ad_image_url: str) -> dict:
    """
    Analyze an ad image using Gemini's vision capabilities.
    Extracts headline, offer, CTA text, tone, and target audience.

    Args:
        ad_image_url: URL of the ad image

    Returns:
        Dictionary with extracted ad information or error object
    """
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=AGENT1_SYSTEM_PROMPT,
    )

    response_text = ""
    try:
        # Try with PIL Image first
        image = _fetch_image_as_pil(ad_image_url)

        response = model.generate_content(
            [
                image,
                (
                    "Extract the following from this ad image and return as compact JSON: "
                    "headline, offer, cta_text, tone (one word), target_audience"
                ),
            ],
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=350,
                temperature=0,
            ),
        )

        response_text = response.text
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
            or "could not download" in error_text
            or "image" in error_text
        )

        if image_fetch_related:
            # Image fetch failed; return error
            return {
                "error": f"agent1 failed: {str(e)}",
            }

        return {"error": f"agent1 failed: {str(e)}"}


def run_agent2(ad_json: dict, page_content: str) -> dict:
    """
    Generate personalized landing page copy using Gemini's language model.

    Args:
        ad_json: Dictionary with ad analysis from run_agent1
        page_content: Scraped content from the landing page

    Returns:
        Dictionary with new headline, subheadline, CTA, and reasoning or error object
    """
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=AGENT2_SYSTEM_PROMPT,
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

        response = model.generate_content(
            user_message,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=220,
                temperature=0,
            ),
        )

        response_text = response.text
        parsed = _parse_json_response(response_text)
        return parsed

    except json.JSONDecodeError:
        return {"error": "agent2 parse failed", "raw": response_text}
    except Exception as e:
        return {"error": f"agent2 failed: {str(e)}"}

