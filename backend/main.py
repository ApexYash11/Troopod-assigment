"""
TROOPOD LANDING PAGE PERSONALISER - BACKEND

To run this application:

1. Navigate to the backend directory:
   cd backend

2. Install dependencies:
   pip install -r requirements.txt

3. Add your real OpenRouter API key and model to .env:
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
   OPENROUTER_MODEL=anthropic/claude-sonnet-4-20250514

4. Start the server:
   uvicorn main:app --reload

The API will be available at http://localhost:8000
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from scraper import scrape_page, parse_page_elements
from agents import run_agent1, run_agent2

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Validate environment variables at startup
try:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    if not OPENROUTER_MODEL:
        raise ValueError("OPENROUTER_MODEL environment variable not set")
except ValueError as e:
    logger.error(f"Configuration error: {str(e)}")
    raise

app = FastAPI(title="Landing Page Personaliser")

# Enable CORS for localhost:3000 (development)
# Update the domain for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # TODO: Add your production frontend URL here (e.g., "https://yourdomain.com")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnhanceRequest(BaseModel):
    ad_image_url: str
    landing_page_url: str


@app.get("/")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/enhance")
async def enhance(request: EnhanceRequest):
    """
    Main endpoint: takes ad image and landing page URL,
    scrapes the page, runs two AI agents, and returns personalized copy
    with both original and new content for side-by-side comparison.
    """
    try:
        logger.info(f"Processing enhance request for {request.landing_page_url}")
        
        # Step 1: Scrape the landing page
        page_content = await scrape_page(request.landing_page_url)
        
        # Step 2: Parse original page elements
        original_elements = parse_page_elements(page_content)
        
        # Step 3: Analyze the ad image
        ad_json = run_agent1(request.ad_image_url)
        if "error" in ad_json:
            logger.error(f"Agent 1 error: {ad_json}")
            return JSONResponse(
                status_code=500, 
                content={"error": "Ad analysis failed", "details": ad_json}
            )
        
        # Step 4: Generate personalized copy
        result = run_agent2(ad_json, page_content)
        if "error" in result:
            logger.error(f"Agent 2 error: {result}")
            return JSONResponse(
                status_code=500,
                content={"error": "Copy generation failed", "details": result}
            )
        
        # Step 5: Return the results with both original and new content
        response_data = {
            "original_h1": original_elements.get("h1", "Not found"),
            "new_h1": result.get("new_h1", ""),
            "original_subhead": original_elements.get("subhead", "Not found"),
            "new_subhead": result.get("new_subhead", ""),
            "original_cta": original_elements.get("cta", "Not found"),
            "new_cta": result.get("new_cta", ""),
            "reasoning": result.get("reasoning", "")
        }
        
        logger.info("Successfully generated personalized copy")
        return JSONResponse(status_code=200, content=response_data)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )
