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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from scraper import scrape_page
from agents import run_agent1, run_agent2

app = FastAPI(title="Landing Page Personaliser")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    scrapes the page, runs two AI agents, and returns personalized copy.
    """
    try:
        # Step 1: Scrape the landing page
        page_content = await scrape_page(request.landing_page_url)
        
        # Step 2: Analyze the ad image
        ad_json = run_agent1(request.ad_image_url)
        if "error" in ad_json:
            return JSONResponse(status_code=500, content={"error": "Ad analysis failed", "details": ad_json})
        
        # Step 3: Generate personalized copy
        result = run_agent2(ad_json, page_content)
        if "error" in result:
            return JSONResponse(status_code=500, content={"error": "Copy generation failed", "details": result})
        
        # Return the results
        return JSONResponse(status_code=200, content={
            "new_h1": result.get("new_h1"),
            "new_subhead": result.get("new_subhead"),
            "new_cta": result.get("new_cta"),
            "reasoning": result.get("reasoning")
        })
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
