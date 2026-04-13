# Landing Page Personaliser - AI PM Assignment (Troopod)

A full-stack application that analyzes ad creatives and personalizes landing pages using AI agents. Users input an ad image URL (or upload a file) and a landing page URL. The system scrapes the landing page, runs two AI agents, and returns personalized copy (headline, subheadline, CTA button text) that better matches the ad messaging. Results are displayed side-by-side showing before/after comparison.

---

## Quick Setup

### Prerequisites
- **Python 3.9+** (backend)
- **Node.js 18+** (frontend)
- **OpenRouter API key** (free tier available)

### Backend Setup (60 seconds)

```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Create .env file with your OpenRouter credentials
echo "OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE" > .env
echo "OPENROUTER_MODEL=anthropic/claude-sonnet-4-20250514" >> .env

# Start server
uvicorn main:app --reload
# Backend running at http://localhost:8000
```

### Frontend Setup (60 seconds)

```bash
cd frontend
npm install
npm run dev
# Frontend running at http://localhost:3000
```

**That's it!** Open http://localhost:3000 in your browser.

---

## System Architecture Diagrams

### Overall System Flow

```mermaid
graph TD
    A["User Input:<br/>Ad Image + Page URL"] --> B["Frontend<br/>Next.js + React"]
    B -->|"POST /enhance<br/>JSON"| C["FastAPI Backend"]
    
    C --> D["Agent 1<br/>Vision Analysis"]
    C --> E["Scraper<br/>Jina.ai"]
    
    D -->|"Extract ad data<br/>headline, offer, tone..."| F["Ad Insights"]
    E -->|"Fetch page content"| G["Page Text"]
    
    F --> H["Agent 2<br/>CRO Specialist"]
    G --> H
    
    H -->|"Generate new copy"| I["Personalized Content"]
    I -->|"Return JSON<br/>original + new fields"| C
    
    C -->|"200 OK Response"| B
    B -->|"Side-by-side display"| A
    
    style D fill:#4CAF50,stroke:#2E7D32,color:#fff
    style H fill:#2196F3,stroke:#1565C0,color:#fff
    style E fill:#FF9800,stroke:#E65100,color:#fff
    style B fill:#673AB7,stroke:#512DA8,color:#fff
    style C fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

### Request/Response Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Agent1 as Agent 1
    participant Scraper
    participant Agent2 as Agent 2
    
    User->>Frontend: Enter ad image URL + page URL
    Frontend->>Frontend: Validate & show progress
    Frontend->>Backend: POST /enhance (JSON)
    
    par Parallel Processing
        Backend->>Agent1: Analyze ad image
        Backend->>Scraper: Fetch page content
    and
        Agent1->>Agent1: Extract insights
        Scraper->>Scraper: Parse elements
    end
    
    Agent1-->>Backend: Ad JSON (headline, offer, tone)
    Scraper-->>Backend: Page content + parsed elements
    
    Backend->>Agent2: Generate personalized copy
    Agent2->>Agent2: Match ad tone + messaging
    Agent2-->>Backend: New copy JSON
    
    Backend->>Backend: Combine original + new fields
    Backend-->>Frontend: 200 OK Response
    
    Frontend->>Frontend: Parse response
    Frontend->>User: Display before/after side-by-side
```

### Frontend UI Layout

```mermaid
graph TD
    A["Frontend Layout"] --> B["Input Form"]
    A --> C["Loading State"]
    A --> D["Error State"]
    A --> E["Results Display"]
    
    B --> B1["Ad Image Input<br/>(URL or Upload)"]
    B --> B2["Landing Page URL"]
    B --> B3["Personalise Button"]
    
    C --> C1["Spinner Icon"]
    C --> C2["Progress Steps<br/>1. Scraping page<br/>2. Analysing ad<br/>3. Generating copy"]
    
    D --> D1["Error Message<br/>Red Card"]
    D --> D2["Retry Button"]
    
    E --> E1["Two Column Grid"]
    E1 --> E1A["Left: Original<br/>(Gray/Muted)"]
    E1 --> E1B["Right: Personalised<br/>(Dark + Green Accent)"]
    E --> E2["Yellow Card Below<br/>Reasoning"]
    E --> E3["Action Buttons<br/>Start Over &<br/>Try Another Page"]
    
    style C fill:#2196F3,stroke:#1565C0,color:#fff
    style D fill:#FF5722,stroke:#D84315,color:#fff
    style E fill:#4CAF50,stroke:#2E7D32,color:#fff
```

### Two-Agent Data Flow

```mermaid
graph LR
    subgraph Agent1["Agent 1: Vision"]
        I1["Ad Image URL"] --> M1["Claude Vision Model"]
        M1 --> O1["Extract: headline<br/>offer, cta_text<br/>tone, audience"]
    end
    
    subgraph Scraper["Page Scraper"]
        I2["Page URL"] --> J["Jina.ai"]
        J --> O2["Raw page content"]
        O2 --> P["Parse page elements:<br/>- first heading H1<br/>- second heading<br/>- button text"]
    end
    
    subgraph Agent2["Agent 2: CRO"]
        O1 --> M2["Claude Text Model"]
        P --> M2
        O3["Ad tone +<br/>Page context"] --> M2
        M2 --> O3A["Generate:<br/>new_h1, new_subhead<br/>new_cta, reasoning"]
    end
    
    Agent1 --> Agent2
    Scraper --> Agent2
    Agent2 --> Result["Final Response:<br/>original_h1, new_h1<br/>original_subhead, new_subhead<br/>original_cta, new_cta<br/>reasoning"]
    
    style M1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M2 fill:#2196F3,stroke:#1565C0,color:#fff
    style J fill:#FF9800,stroke:#E65100,color:#fff
    style Result fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

### Error Handling Flow

```mermaid
graph TD
    A["POST /enhance Request"] --> B{Ad Analysis<br/>Succeeds?}
    
    B -->|Yes| C{Scraping<br/>Succeeds?}
    B -->|No| E["Return 500<br/>Ad Analysis Failed"]
    
    C -->|Yes| D{Copy Generation<br/>Succeeds?}
    C -->|No| F["Return 400<br/>Page Not Accessible"]
    
    D -->|Yes| G["Return 200<br/>Personalized Copy"]
    D -->|No| H{JSON Parse<br/>Failed?}
    
    H -->|Yes| I["Retry with<br/>Stricter Prompt"]
    H -->|No| J["Return 500<br/>Generation Failed"]
    
    I -->|Success| G
    I -->|Fail| K["Return 500<br/>Parse Error"]
    
    E --> L["Frontend<br/>Shows Error Card<br/>with Retry Button"]
    F --> L
    J --> L
    K --> L
    G --> M["Frontend<br/>Shows Side-by-Side<br/>Comparison"]
    
    style G fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M fill:#4CAF50,stroke:#2E7D32,color:#fff
    style L fill:#FF5722,stroke:#D84315,color:#fff
    style E fill:#FF5722,stroke:#D84315,color:#fff
    style F fill:#FF5722,stroke:#D84315,color:#fff
    style K fill:#FF5722,stroke:#D84315,color:#fff
```

## How It Works

1. User Input - Upload ad image (file or URL) and paste landing page URL
2. Backend Processing - Agent 1 analyzes the ad to extract headline, offer, CTA, tone, target audience
3. Page Scraping - Fetches landing page content via Jina.ai and parses original elements
4. CRO Optimization - Agent 2 generates personalized copy matching the ad messaging
5. Results Display - Shows side-by-side comparison: original (left) vs personalized (right)

---

## API Contract

### POST /enhance

**Request:**
```json
{
  "ad_image_url": "https://example.com/ad.jpg or data:image/png;base64,...",
  "landing_page_url": "https://example.com/landing"
}
```

**Success Response (200):**
```json
{
  "original_h1": "Current page headline",
  "new_h1": "Personalised headline",
  "original_subhead": "Current page subheadline",
  "new_subhead": "Personalised subheadline",
  "original_cta": "Original button text",
  "new_cta": "Personalised button text",
  "reasoning": "One-sentence explanation of the changes"
}
```

**Error Response (400/500):**
```json
{
  "error": "Clear error message describing what failed"
}
```

---

## Key Features Implemented

- File Upload + URL Input - Support both ad image upload and direct URLs
- Side-by-Side Display - Before/after comparison with color-coded styling
- Multi-Step Progress Indicator - Cycles through loading steps (Scraping → Analysing → Generating)
- Error Handling - Clear error messages with "Retry" button
- Start Over Button - Reset all state and form
- Configurable API Endpoint - Use NEXT_PUBLIC_API_URL environment variable
- Agent Prompt Optimization - Exact specifications with temperature=0 for deterministic output
- JSON Retry Logic - On parse failure, retry with stricter prompt; fallback to error dict
- CORS Security - Restricted to localhost:3000
- Environment Validation - Clear startup errors if API keys missing
- Structured Logging - Debug-level logs for troubleshooting

---

## Agent Specifications

### Agent 1: Ad Analyst

**System Prompt:**
> You are an expert ad analyst. Extract structured data from ad creatives. Return raw JSON only. No markdown. No explanation. No code blocks.

**Returns:**
```json
{
  "headline": "the main headline or hook of the ad",
  "offer": "the specific offer, discount, or benefit being promoted",
  "cta_text": "the call to action text",
  "tone": "one word only: urgent OR warm OR bold OR playful OR professional",
  "target_audience": "who this ad is speaking to in 5 words or less"
}
```

**Settings:** temperature=0, max_tokens=350

### Agent 2: CRO Specialist

**System Prompt:**
> You are a senior CRO specialist with 10 years experience. You personalise landing pages to match ad creatives. Increase message match between ad and page. Return raw JSON only. No markdown. No explanation. No code blocks. Critical rule: Only use claims, offers, and benefits that appear in the ad data. Never invent new features, prices, or guarantees.

**Returns:**
```json
{
  "new_h1": "new headline that echoes the ad promise",
  "new_subhead": "new subheadline that expands on the ad offer",
  "new_cta": "new CTA button text that matches ad action",
  "reasoning": "one sentence explaining what you changed and why"
}
```

**Settings:** temperature=0, max_tokens=220

---

## Project Structure

```
backend/
├── main.py              # FastAPI app, /enhance endpoint, CORS config
├── agents.py            # Agent 1 & 2 implementations with retry logic
├── scraper.py           # Page scraping + content parsing
└── requirements.txt     # Python dependencies (pinned versions)

frontend/
├── pages/
│   ├── _app.tsx         # Next.js app wrapper
│   └── index.tsx        # Main UI with form, file upload, results display
├── styles/
│   └── globals.css      # Tailwind styles
└── package.json         # Node dependencies

README.md                # This file
RESULTS.md              # Testing results & examples
.gitignore              # Git ignore patterns
```

---

## CORS & Security

**Allowed Origins:**
- http://localhost:3000
- http://127.0.0.1:3000
- (TODO: Add production frontend URL)

**Update for Production:**
Edit backend/main.py line ~45 and add your Vercel domain or other frontend URL.

---

## Dependencies

### Backend (Requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2
python-dotenv==1.0.0
pydantic==2.5.2
openai==1.12.0
```

### Frontend (package.json)
```
next@^14.0.0
react@^18.0.0
react-dom@^18.0.0
typescript@^5.0.0
tailwindcss@^3.0.0
```

---

## Environment Variables

### Backend (.env)
```
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
OPENROUTER_MODEL=anthropic/claude-sonnet-4-20250514
```

### Frontend (.env.local - optional)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check `.env` file has valid `OPENROUTER_API_KEY` |
| Frontend can't connect | Ensure backend running on `http://localhost:8000` |
| Page scraping fails | Verify URL is accessible; some pages block Jina.ai |
| Ad image analysis failed | Try URL first; file upload must be under 4MB |
| Rate limit error (429) | OpenRouter quota exhausted; use paid key or wait |

---

## Testing

### Manual Test Flow
1. Open http://localhost:3000
2. Upload an ad image (or paste URL)
3. Enter a landing page URL (e.g., https://example.com)
4. Click "Personalise"
5. Wait for progress indicator to cycle through steps
6. View results: original (left) vs personalised (right)
7. Click "Start over" to test another page

### Sample Test URLs
- **Landing Page**: https://example.com, https://example.org
- **Ad Image**: Any public image URL (JPG, PNG, GIF, WebP)

---

## Files Modified During Audit

### Backend (Phase 1)
- agents.py - Updated prompts, added retry logic, temperature=0
- scraper.py - Added parse_page_elements(), improved error handling
- main.py - Fixed CORS, updated /enhance response shape, added logging
- requirements.txt - Pinned versions, removed unused dependencies

### Frontend (Phase 2)
- pages/index.tsx - Complete rewrite: file upload, before/after display, progress indicator, error retry, start over button

### Configuration (Phase 3)
- .gitignore - Added .env.local, organized patterns
- README.md - Updated with setup, API contract, troubleshooting

---

## Next Steps

This is a working assignment submission. For production use:

1. **Deploy Backend**: Push to Render, Railway, or Vercel (serverless)
2. **Deploy Frontend**: Push to Vercel or Netlify
3. **Use Paid OpenRouter Key**: Free tier has daily quotas
4. **Set Environment Variables**: In hosting platform's dashboard
5. **Update CORS Domain**: Change allowed_origins in main.py
6. **Monitor Usage**: Track OpenRouter API costs and Jina.ai quotas
7. **Add Caching**: Store results to reduce API calls
8. **Implement Analytics**: Track personalization effectiveness

---

## Contact

For questions or issues, refer to:
- Backend logs: Terminal where `uvicorn main:app` is running
- Frontend console: Browser DevTools → Console
- API responses: Check error messages in red card on UI

---

**Built with passion for Troopod AI PM Assignment**  
**April 2026**
