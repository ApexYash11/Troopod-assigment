import httpx


async def scrape_page(url: str) -> str:
    """
    Scrape a landing page using Jina.ai's API.
    
    Args:
        url: The URL of the page to scrape
        
    Returns:
        The scraped page content as text
        
    Raises:
        ValueError: If scraping fails
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(jina_url, timeout=10.0)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to scrape page: {str(e)}")
    except Exception as e:
        raise ValueError(f"Scraping error: {str(e)}")
