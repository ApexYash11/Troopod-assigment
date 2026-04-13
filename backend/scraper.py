import httpx
import re


async def scrape_page(url: str) -> str:
    """
    Scrape a landing page using Jina.ai's API.
    
    Args:
        url: The URL of the page to scrape
        
    Returns:
        The scraped page content as text
        
    Raises:
        ValueError: If scraping fails or returns empty content
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(jina_url, timeout=10.0)
            response.raise_for_status()
            
            content = response.text
            if not content or content.strip() == "":
                raise ValueError("Jina API returned empty content. The page may be inaccessible or blocked.")
            
            return content
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to scrape page: {str(e)}")
    except Exception as e:
        raise ValueError(f"Scraping error: {str(e)}")


def parse_page_elements(page_content: str) -> dict:
    """
    Extract original headline, subheadline, and CTA from scraped page content.
    Uses simple heuristics: first heading, second line, button-like text.
    
    Args:
        page_content: Raw scraped page content
        
    Returns:
        Dictionary with 'h1', 'subhead', 'cta' keys (fallback to "Not found" if missing)
    """
    lines = page_content.split('\n')
    
    # Extract H1 (first heading-like line)
    h1 = "Not found"
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) > 3 and len(stripped) < 200:
            # Skip lines that look like metadata or URLs
            if not stripped.startswith('http') and not stripped.startswith('#'):
                h1 = stripped[:120]  # Cap at 120 chars
                break
    
    # Extract subhead (second prominent line, skip if same as h1)
    subhead = "Not found"
    found_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) > 10 and len(stripped) < 200:
            if not stripped.startswith('http') and not stripped.startswith('#'):
                found_count += 1
                if found_count == 2:
                    subhead = stripped[:150]  # Cap at 150 chars
                    break
    
    # Extract CTA (look for button-like text or action words)
    cta = "Not found"
    cta_keywords = ['click', 'sign', 'get', 'start', 'join', 'buy', 'learn', 'download', 'submit', 'button', 'cta']
    for line in lines:
        stripped = line.strip()
        if any(keyword in stripped.lower() for keyword in cta_keywords) and len(stripped) < 100:
            cta = stripped[:80]  # Cap at 80 chars
            break
    
    return {
        "h1": h1,
        "subhead": subhead,
        "cta": cta
    }
