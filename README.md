# Landing Page Personaliser - AI PM Assignment (Troopod)

A full-stack application that analyzes ad creatives and personalizes landing pages using AI agents. Takes an ad image and landing page URL as input, extracts ad insights, scrapes landing page content, and generates personalized copy following CRO principles.

---

## 📊 Mermaid Diagrams Guide

This README includes **12 comprehensive Mermaid diagrams** visualizing system architecture, data flows, and operational logic:

| Diagram | Purpose |
|---------|---------|
| 🏗️ System Architecture | Full user flow through all components |
| 🔄 Two-Agent Data Flow | Parallel vision & text processing |
| 🔌 API Components & Models | Technology stack topology |
| 🤝 Communication Protocol | HTTP/JSON message flow |
| ⚙️ Configuration Flow | Startup & model selection |
| 📝 Request/Response Lifecycle | Sequence diagram |
| 🚨 Error Handling | Decision tree for failures |
| 🧪 Testing Strategy | Test coverage matrix |
| 🧠 Hallucination Prevention | Multi-layer constraints |
| 📖 Prompt Engineering | Detailed prompt structure |
| 🔄 Model Fallback | Provider error handling |
| 🚀 Deployment Architecture | Development → Production |

---

## 📋 System Architecture

```mermaid
graph TD
    A["👤 User Input<br/>Ad Image URL + Landing Page URL"] --> B["🎨 Frontend<br/>Next.js React"]
    B --> C["🔌 FastAPI Backend<br/>POST /enhance"]
    
    C --> D["👁️ Agent 1: Vision<br/>Ad Analyzer"]
    C --> E["🌐 Scraper<br/>Jina.ai"]
    
    D --> F["📊 Extract Ad Insights<br/>Headline, Offer, CTA<br/>Tone, Target Audience"]
    E --> G["📄 Landing Page Content<br/>First 2000 chars"]
    
    F --> H["📋 JSON Data<br/>Ad Analysis"]
    G --> I["📋 Context Data<br/>Page Content"]
    
    H --> J["🤖 Agent 2: Text<br/>CRO Specialist"]
    I --> J
    
    J --> K["✍️ Generate Personalized Copy<br/>new_h1, new_subhead,<br/>new_cta, reasoning"]
    
    K --> L["📤 JSON Response<br/>200 OK"]
    L --> B
    
    B --> M["🎯 Display Results<br/>User Sees Personalized Copy"]
    
    style D fill:#4CAF50,stroke:#2E7D32,color:#fff
    style J fill:#2196F3,stroke:#1565C0,color:#fff
    style E fill:#FF9800,stroke:#E65100,color:#fff
    style C fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

### System Flow

1. **User Input** → Frontend form accepts ad image URL + landing page URL
2. **Agent 1 (Vision)** → Analyzes ad image, extracts:
   - Headline
   - Offer/Value Proposition
   - CTA Text
   - Tone (energetic, professional, casual, etc.)
   - Target Audience
3. **Page Scraper** → Fetches landing page content via Jina.ai
4. **Agent 2 (Text)** → Generates personalized copy using:
   - Ad insights from Agent 1
   - Landing page context
   - CRO best practices
5. **Output** → New headline, subheadline, CTA, and reasoning

### Two-Agent Data Flow

```mermaid
graph LR
    subgraph "Agent 1: Vision & Analysis"
        A1["🖼️ Ad Image<br/>URL"]
        A2["👁️ Vision Model<br/>OpenRouter"]
        A3["📊 Extract JSON<br/>headline, offer, cta<br/>tone, audience"]
    end
    
    subgraph "Agent 2: CRO Copy Generation"
        B1["📋 Agent 1 JSON<br/>+ Page Context"]
        B2["🤖 Text Model<br/>OpenRouter"]
        B3["✍️ Generate JSON<br/>new_h1, new_subhead<br/>new_cta, reasoning"]
    end
    
    subgraph "Scraper (Parallel)"
        C1["🌐 Landing Page URL"]
        C2["🔗 Jina.ai"]
        C3["📄 Page Content<br/>2000 chars"]
    end
    
    A1 --> A2
    A2 --> A3
    
    C1 --> C2
    C2 --> C3
    
    A3 --> B1
    C3 --> B1
    
    B1 --> B2
    B2 --> B3
    
    B3 --> D["📤 Response<br/>Personalized Copy"]
    
    style A2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style A3 fill:#A5D6A7,stroke:#558B2F,color:#000
    style B2 fill:#2196F3,stroke:#1565C0,color:#fff
    style B3 fill:#90CAF9,stroke:#1565C0,color:#000
    style C2 fill:#FF9800,stroke:#E65100,color:#fff
    style D fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

### API Components & Models

```mermaid
graph TB
    subgraph "Frontend Layer"
        FE["Next.js 14<br/>React 18<br/>TypeScript"]
    end
    
    subgraph "Backend API"
        API["FastAPI<br/>Port: 8000"]
        HC["GET /<br/>Health Check"]
        MAIN["POST /enhance<br/>Main Logic"]
    end
    
    subgraph "AI Models"
        M1["🔷 Agent 1: Vision Model<br/>google/gemma-3-4b-it:free"]
        M2["🔷 Agent 2: Text Model<br/>google/gemma-3-4b-it:free"]
    end
    
    subgraph "External Services"
        OR["OpenRouter API<br/>🔑 API Key"]
        JN["Jina.ai<br/>Page Scraper"]
    end
    
    FE -->|"POST /enhance<br/>{ ad_image_url,<br/>landing_page_url }"| API
    API --> HC
    API --> MAIN
    
    MAIN --> M1
    MAIN --> JN
    
    M1 --> OR
    M2 --> OR
    
    MAIN --> M2
    
    OR -->|Vision Analysis| M1
    OR -->|Copy Generation| M2
    
    JN -->|Page Content| MAIN
    
    M1 -->|Ad Insights<br/>JSON| MAIN
    M2 -->|Personalized Copy| MAIN
    
    MAIN -->|"{ new_h1,<br/>new_subhead,<br/>new_cta,<br/>reasoning }"| API
    API -->|Response| FE
    
    style FE fill:#FBE9E7,stroke:#D84315,color:#000
    style API fill:#E8F5E9,stroke:#2E7D32,color:#000
    style M1 fill:#E3F2FD,stroke:#1565C0,color:#000
    style M2 fill:#E3F2FD,stroke:#1565C0,color:#000
    style OR fill:#F3E5F5,stroke:#6A1B9A,color:#fff
    style JN fill:#FFF3E0,stroke:#E65100,color:#000
```

### Component Communication Protocol

```mermaid
graph LR
    subgraph "Protocol Stack"
        D["📋 Data Layer<br/>JSON"]
        T["🔗 Transport<br/>HTTP/HTTPS"]
        M["🤝 Message Format<br/>REST API"]
    end
    
    subgraph "Frontend"
        F["React Form<br/>POST Request"]
    end
    
    subgraph "Backend Processing"
        B1["FastAPI<br/>Parse JSON"]
        B2["Agent 1<br/>Vision Analysis"]
        B3["Scraper<br/>Jina.ai"]
        B4["Agent 2<br/>Text Generation"]
        B5["Response Builder<br/>Format JSON"]
    end
    
    subgraph "External Communication"
        E1["OpenRouter<br/>gRPC-like<br/>API v1"]
        E2["Jina.ai<br/>HTTP GET<br/>r.jina.ai"]
    end
    
    D --> T
    T --> M
    
    F -->|"JSON: {<br/>ad_image_url,<br/>landing_page_url<br/>}"| M
    M --> B1
    
    B1 --> B2
    B1 --> B3
    
    B2 -->|"JSON Request<br/>image input"| E1
    B3 -->|"URL Input"| E2
    
    E1 -->|"JSON Response<br/>ad insights"| B2
    E2 -->|"HTML/Text"| B3
    
    B2 --> B4
    B3 --> B4
    
    B4 -->|"JSON Request<br/>insights + context"| E1
    E1 -->|"JSON Response<br/>personalized copy"| B4
    
    B4 --> B5
    B5 -->|"JSON: {<br/>new_h1,<br/>new_subhead,<br/>new_cta,<br/>reasoning<br/>}"| F
    
    style D fill:#E8F5E9,stroke:#2E7D32,color:#000
    style T fill:#E3F2FD,stroke:#1565C0,color:#000
    style M fill:#F3E5F5,stroke:#512DA8,color:#fff
    style F fill:#FBE9E7,stroke:#D84315,color:#000
    style B1 fill:#FFFDE7,stroke:#F57F17,color:#000
    style B2 fill:#E8F5E9,stroke:#2E7D32,color:#000
    style B3 fill:#FFF3E0,stroke:#E65100,color:#000
    style B4 fill:#E8F5E9,stroke:#2E7D32,color:#000
    style B5 fill:#F3E5F5,stroke:#512DA8,color:#fff
    style E1 fill:#BBDEFB,stroke:#1565C0,color:#000
    style E2 fill:#BBDEFB,stroke:#1565C0,color:#000
```

---

## 🏗️ Project Structure

```
Troopod-assigment/
├── backend/
│   ├── main.py              # FastAPI app + endpoints
│   ├── agents.py            # Agent 1 & 2 logic
│   ├── scraper.py           # Landing page scraper
│   ├── requirements.txt      # Python dependencies
│   └── .env                 # API keys (OpenRouter)
├── frontend/
│   ├── pages/
│   │   └── index.tsx        # Main UI form
│   ├── package.json         # Node dependencies
│   ├── tailwind.config.js   # Tailwind CSS config
│   └── tsconfig.json        # TypeScript config
├── README.md                # This file
└── RESULTS.md               # Testing results & evidence
```

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- OpenRouter API key (free or paid): https://openrouter.ai

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
OPENROUTER_MODEL=google/gemma-3-4b-it:free
GEMINI_API_KEY=YOUR_GEMINI_KEY_IF_USING
EOL

# Start FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Available Free Vision Models:**
- `google/gemma-3-4b-it:free` (Small, fast)
- `meta-llama/llama-3.2-11b-vision-instruct:free` (11B, capable)
- `mistralai/pixtral-12b:free` (12B, Mistral's vision)

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Navigate to http://localhost:3000
```

---

## 🔧 API Endpoints

### Health Check
```bash
GET /
Response: {"status": "ok"}
```

### Enhance (Main Endpoint)
```bash
POST /enhance
Content-Type: application/json

Request:
{
  "ad_image_url": "https://example.com/ad.png",
  "landing_page_url": "https://example.com"
}

Success Response (200):
{
  "new_h1": "Personalized headline",
  "new_subhead": "Enhanced subheading",
  "new_cta": "Action-oriented CTA",
  "reasoning": "Why these changes work for this audience"
}

Error Response (500/429):
{
  "error": "Ad analysis failed",
  "details": {
    "error": "Rate limit or model error"
  }
}
```

### Example Request (PowerShell)
```powershell
$payload = @{
  ad_image_url = "https://raw.githubusercontent.com/github/explore/main/topics/python/python.png"
  landing_page_url = "https://example.com"
} | ConvertTo-Json -Compress

Invoke-WebRequest -Uri "http://127.0.0.1:8000/enhance" `
  -Method POST `
  -ContentType "application/json" `
  -Body $payload `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Request/Response Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Frontend<br/>Next.js
    participant Backend as Backend<br/>FastAPI
    participant Vision as Agent 1<br/>Vision Model
    participant Scraper as Scraper<br/>Jina.ai
    participant Text as Agent 2<br/>Text Model
    
    User->>Frontend: Enter URLs
    Frontend->>Backend: POST /enhance
    Backend->>Vision: Analyze Ad Image
    Backend->>Scraper: Fetch Page Content
    
    Vision-->>Backend: Ad Insights JSON
    Scraper-->>Backend: Page Text
    
    Backend->>Text: Generate Copy
    Text-->>Backend: Personalized Copy JSON
    
    Backend-->>Frontend: 200 OK Response
    Frontend-->>User: Display Results
```

---

## 🛡️ Error Handling & Robustness

### Error Handling Flow

```mermaid
graph TD
    A["🚀 API Request<br/>/enhance"] --> B{Agent 1<br/>Executes?}
    
    B -->|✅ Success| C{Agent 2<br/>Executes?}
    B -->|❌ Fail| D["Image Fetch Error<br/>or Model Issue"]
    
    D --> E["Return Error<br/>500 / 404"]
    
    C -->|✅ Success| F["🎉 Return<br/>Personalized Copy<br/>200 OK"]
    C -->|❌ 429| G["Rate Limit<br/>Upstream"]
    C -->|❌ Fail| H["Parse Error<br/>or Model Error"]
    
    G --> I["Return 429<br/>With Retry Info"]
    H --> J["Return Error<br/>500"]
    
    E --> K["📊 Structured Error<br/>Response"]
    I --> K
    J --> K
    
    K --> L["User Gets Clear<br/>Error Message"]
    F --> L
    
    style F fill:#4CAF50,stroke:#2E7D32,color:#fff
    style K fill:#FF5722,stroke:#D84315,color:#fff
    style L fill:#2196F3,stroke:#1565C0,color:#fff
```

### Hallucination Prevention Strategy

```mermaid
graph LR
    A["🧠 LLM Output"] --> B["🎯 Constraint 1<br/>System Prompt:<br/>No fabrication"]
    
    B --> C["🧮 Constraint 2<br/>Word Limits:<br/>h1≤12, subhead≤16"]
    
    C --> D["📋 Constraint 3<br/>Token Limit:<br/>350 tokens max"]
    
    D --> E["{ } Parse<br/>JSON Extract"]
    
    E --> F["✔️ Validate<br/>Schema Match"]
    
    F -->|Valid| G["✅ Return<br/>Personalized Copy"]
    F -->|Invalid| H["🔄 Fallback<br/>Extract from Markdown"]
    
    H -->|Found| G
    H -->|Not Found| I["❌ Return Error<br/>Parse Failed"]
    
    style G fill:#4CAF50,stroke:#2E7D32,color:#fff
    style I fill:#FF5722,stroke:#D84315,color:#fff
```

### Prompt Engineering & Output Control

```mermaid
graph TD
    START["🎯 Prompt Engineering"]
    
    START --> P1["📝 Agent 1: Vision Prompt<br/>Extract ONLY these fields:<br/>- headline<br/>- offer<br/>- cta<br/>- tone<br/>- audience"]
    
    START --> P2["📝 Agent 2: Text Prompt<br/>Generate ONLY these fields:<br/>- new_h1 max 12 words<br/>- new_subhead max 16 words<br/>- new_cta max 6 words<br/>- reasoning short"]
    
    P1 --> M1["🔧 Model Parameters<br/>temperature=0<br/>max_tokens=350<br/>top_p=0.9"]
    
    P2 --> M2["🔧 Model Parameters<br/>temperature=0<br/>max_tokens=220<br/>top_p=0.9"]
    
    M1 --> E1["🎨 Agent 1 Output<br/><br/>json<br/>{<br/>  'headline': 'Actual text...',<br/>  'offer': '...',<br/>  'cta': '...',<br/>  'tone': '...',<br/>  'audience': '...'<br/>}"]
    
    M2 --> E2["🎨 Agent 2 Output<br/><br/>json<br/>{<br/>  'new_h1': 'Max 12 words',<br/>  'new_subhead': 'Max 16 words',<br/>  'new_cta': 'Max 6 words',<br/>  'reasoning': 'Why...'<br/>}"]
    
    E1 --> V1["✅ Validation Layer<br/>- Verify JSON syntax<br/>- Check field presence<br/>- Validate word counts"]
    
    E2 --> V2["✅ Validation Layer<br/>- Verify JSON syntax<br/>- Check field presence<br/>- Verify word limits<br/>- No offensive content"]
    
    V1 --> F["✅ Formatted Response<br/>200 OK"]
    V2 --> F
    
    style E1 fill:#E3F2FD,stroke:#1976D2,color:#000
    style E2 fill:#E3F2FD,stroke:#1976D2,color:#000
    style V1 fill:#C8E6C9,stroke:#388E3C,color:#000
    style V2 fill:#C8E6C9,stroke:#388E3C,color:#000
    style F fill:#4CAF50,stroke:#2E7D32,color:#fff
```

### Model Fallback & Rate Limit Handling

```mermaid
graph TD
    A["🎯 User Request<br/>Select Model"] --> B["🤖 Model 1<br/>Primary Choice"]
    
    B -->|✅ Success| C["🎉 Generate<br/>Personalized Copy"]
    
    B -->|404| D["⚠️ Model<br/>Not Available"]
    B -->|429| E["⏱️ Rate Limited<br/>Quota Exceeded"]
    
    D --> F["🔄 Fallback to<br/>Model 2"]
    E --> G["⏳ Wait Signal<br/>Retry in 25s"]
    
    F -->|✅ Success| C
    F -->|❌ Fail| H["🔄 Fallback to<br/>Model 3"]
    
    H -->|✅ Success| C
    H -->|❌ Fail| I["❌ All Models Failed<br/>Return Error"]
    
    G --> J["⏳ User Can<br/>Retry Later"]
    
    I --> K["📤 Error: No Models<br/>Available"]
    C --> K
    J --> K
    
    style C fill:#4CAF50,stroke:#2E7D32,color:#fff
    style K fill:#2196F3,stroke:#1565C0,color:#fff
    style I fill:#FF5722,stroke:#D84315,color:#fff
```

### Broken UI / Failed Requests
- **Graceful Error Messages**: Returns structured error objects with details
- **Status Codes**: Appropriate HTTP codes (200 success, 429 rate-limit, 404 model not found, 500 agent error)
- **CORS Support**: Enabled for frontend integration
- **Try-Catch Blocks**: Comprehensive error handling in agents and scraper

### Rate Limiting
- **Multiple Model Fallbacks**: Auto-switches between free models if one hits quota
- **Upstream Provider Handling**: Detects 429 errors and provides user-friendly messages
- **Free Tier Management**: Free OpenRouter quotas reset periodically
- **Paid Key Support**: Seamlessly switches to paid models if provided

### Inconsistent Outputs
- **System Role Fallback**: Some providers reject system role; merged into user message
- **Content Type Detection**: Handles various response formats (list, dict, plaintext)
- **Image Format Support**: Falls back between URL references and base64 encoding
- **Deterministic Settings**: Temperature 0 for all API calls, fixed system instructions

---

## 🎯 Key Features & Assumptions

### Features Implemented
✅ Vision-based ad analysis (Agent 1)  
✅ CRO-optimized copy generation (Agent 2)  
✅ Multi-model fallback strategy  
✅ Error handling & graceful degradation  
✅ CORS-enabled for frontend  
✅ TypeScript frontend with form validation  
✅ Landing page scraping via Jina.ai  
✅ Environment-based model switching  

### Assumptions
- **Free-tier quotas**: Free models have limited requests/day; paid keys recommended
- **Jina.ai availability**: Landing page scraper relies on Jina.ai API
- **Ad images are public URLs**: System fetches from provided URLs
- **JSON output format**: Agents trained to respond in JSON without markdown
- **CRO principles scope**: Personalization focuses on headline, subheading, CTA (not full page rewrite)
- **Single-document context**: Only processes first 2000 chars of landing page

### Testing Strategy

```mermaid
graph TD
    START["🧪 Test Suite"]
    
    START --> HEALTH["1️⃣ Health Check<br/>GET /"]
    START --> E2E["2️⃣ End-to-End<br/>POST /enhance"]
    START --> ERROR["3️⃣ Error Scenarios<br/>429, 404, Timeout"]
    START --> PERF["4️⃣ Performance<br/>Latency, Memory"]
    
    HEALTH -->|"✅ PASS"| H_PASS["Status 200<br/>Response OK"]
    
    E2E -->|"✅ PASS"| E_PASS["Full Flow:<br/>Image → Agent1 → Agent2<br/>→ Personalized Copy"]
    E2E -->|"⚠️ FAIL"| E_FAIL["429 Rate Limit<br/>404 Model Missing<br/>Parse Error"]
    
    ERROR -->|"✅ PASS"| E_PASS2["Errors Handled:<br/>Structured Response<br/>Proper Status Code"]
    ERROR -->|"📋 EXPECTED"| E_FAIL2["Known Issues:<br/>Free Model Quotas<br/>Rate Limits"]
    
    PERF -->|"✅ PASS"| P_PASS["Agent 1: 3-5s<br/>Agent 2: 2-4s<br/>Total: 7-12s"]
    PERF -->|"⚠️ WARN"| P_WARN["Free Models Slower<br/>Consider Paid Keys<br/>for Production"]
    
    H_PASS --> REPORT["📊 See RESULTS.md<br/>24 Tests Documented<br/>16 Pass, 8 Expected Fail"]
    E_PASS --> REPORT
    E_PASS2 --> REPORT
    P_PASS --> REPORT
    E_FAIL2 --> REPORT
    
    REPORT --> END["✅ Test Coverage Complete"]
    
    style HEALTH fill:#E3F2FD,stroke:#1976D2,color:#000
    style E2E fill:#E3F2FD,stroke:#1976D2,color:#000
    style ERROR fill:#FFF3E0,stroke:#F57C00,color:#000
    style PERF fill:#F3E5F5,stroke:#7B1FA2,color:#000
    style H_PASS fill:#C8E6C9,stroke:#388E3C,color:#000
    style E_PASS fill:#C8E6C9,stroke:#388E3C,color:#000
    style E_PASS2 fill:#C8E6C9,stroke:#388E3C,color:#000
    style P_PASS fill:#C8E6C9,stroke:#388E3C,color:#000
    style E_FAIL2 fill:#FFECB3,stroke:#F57F17,color:#000
    style REPORT fill:#E1BEE7,stroke:#512DA8,color:#000
```

---

## 🚀 Deployment Options

### Deployment Architecture

```mermaid
graph TD
    subgraph "Development"
        A["💻 Local Machine<br/>Python + Node.js<br/>venv / npm"]
    end
    
    subgraph "Production - Cloud"
        B["🎨 Frontend<br/>Vercel / Netlify<br/>Next.js"]
        C["🔌 Backend<br/>Render / Railway<br/>FastAPI + Python"]
        D["🔑 API Keys<br/>Environment Secrets<br/>CI/CD Pipeline"]
    end
    
    subgraph "External Services"
        E["📡 OpenRouter<br/>LLM Provider<br/>Vision + Text Models"]
        F["🌐 Jina.ai<br/>Web Scraper<br/>Landing Page Content"]
    end
    
    A -->|Dev Mode| B
    A -->|Dev Mode| C
    
    B -->|Calls| C
    C -->|Uses| D
    C -->|Calls| E
    C -->|Calls| F
    
    style A fill:#FFC107,stroke:#F57F17,color:#000
    style B fill:#2196F3,stroke:#1565C0,color:#fff
    style C fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style D fill:#FF5722,stroke:#D84315,color:#fff
    style E fill:#4CAF50,stroke:#2E7D32,color:#fff
    style F fill:#FF9800,stroke:#E65100,color:#fff
```

### Local Development
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Docker (Future)
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Production
- Deploy backend to: Render, Vercel, Railway, or AWS Lambda
- Deploy frontend to: Vercel, Netlify
- Use paid OpenRouter key for consistent quota access

---

## 📝 Configuration

### Environment Variables
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx  # Required
OPENROUTER_MODEL=google/gemma-3-4b-it:free  # Default vision model
GEMINI_API_KEY=xxxxxxxxxxxxx                # Optional (for fallback)
```

### Model Selection Guide
| Model | Type | Size | Speed | Cost | Vision |
|-------|------|------|-------|------|--------|
| `google/gemma-3-4b-it:free` | Text + Vision | 4B | Fast | Free | ✅ |
| `meta-llama/llama-3.2-11b-vision:free` | Text + Vision | 11B | Medium | Free | ✅ |
| `mistralai/pixtral-12b:free` | Text + Vision | 12B | Medium | Free | ✅ |

### Configuration Flow

```mermaid
graph TD
    START["🔧 System Startup"] --> LOAD[".env File<br/>Load ENV variables"]
    LOAD --> CHECK{"API Key<br/>Valid?"}
    
    CHECK -->|❌ No| ERROR["⚠️ Exit<br/>Missing OPENROUTER_API_KEY"]
    CHECK -->|✅ Yes| SELECT["📋 Model Selection<br/>from OPENROUTER_MODEL"]
    
    SELECT --> AGENT1["👁️ Agent 1<br/>Vision Model"]
    SELECT --> AGENT2["🤖 Agent 2<br/>Text Model"]
    
    AGENT1 --> TRY1["🔄 Try Primary Model"]
    AGENT2 --> TRY2["🔄 Try Primary Model"]
    
    TRY1 -->|404<br/>Not Found| FB1["↩️ Fallback<br/>meta-llama/llama..."]
    TRY1 -->|429<br/>Rate Limit| FB2["⏱️ Wait & Retry<br/>or Error"]
    TRY1 -->|✅ Success| RUN1["▶️ Execute<br/>Vision Analysis"]
    
    TRY2 -->|404<br/>Not Found| FB3["↩️ Fallback<br/>mistralai/pixtral..."]
    TRY2 -->|429<br/>Rate Limit| FB4["⏱️ Wait & Retry<br/>or Error"]
    TRY2 -->|✅ Success| RUN2["▶️ Execute<br/>Text Generation"]
    
    RUN1 --> OUTPUT["📤 Return JSON<br/>Response"]
    RUN2 --> OUTPUT
    
    ERROR --> END["❌ End"]
    OUTPUT --> END["✅ End"]
    
    style LOAD fill:#C8E6C9,stroke:#2E7D32,color:#000
    style AGENT1 fill:#BBDEFB,stroke:#1565C0,color:#000
    style AGENT2 fill:#BBDEFB,stroke:#1565C0,color:#000
    style RUN1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style RUN2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style FB1 fill:#FFE082,stroke:#F57F17,color:#000
    style FB2 fill:#FFE082,stroke:#F57F17,color:#000
    style FB3 fill:#FFE082,stroke:#F57F17,color:#000
    style FB4 fill:#FFE082,stroke:#F57F17,color:#000
    style ERROR fill:#FFCDD2,stroke:#C62828,color:#fff
```


---

## 🔐 Security Notes

⚠️ **IMPORTANT**: API keys are sensitive  
- Never commit `.env` to version control
- Rotate keys in OpenRouter dashboard if exposed
- Use separate keys for dev/prod environments
- Consider using environment secrets in CI/CD

---

## 📚 Technologies

**Backend:**
- FastAPI (web framework)
- OpenAI SDK (OpenRouter API client)
- httpx (HTTP client for scraping)
- Pydantic (data validation)
- python-dotenv (environment management)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- React Hooks (state management)

**External APIs:**
- OpenRouter (LLM access)
- Jina.ai (web scraping)

---

## 📊 Testing & Results

See [RESULTS.md](./RESULTS.md) for:
- Live API test outputs
- Response examples with various models
- Performance metrics
- Error scenarios and handling
- Before/after personalization examples

---

## ✋ Next Steps for Enhancement

1. **Cache System**: Store scraped pages and ad analyses to reduce API calls
2. **A/B Testing**: Generate multiple variants, not just one personalized copy
3. **Analytics**: Track which personalized headlines convert better
4. **Fine-tuning**: Train custom models on CRO best practices
5. **Batch Processing**: Support uploading multiple ads at once
6. **UI Improvements**: Live preview of personalized page, not just copy
7. **Server-side Rate Limiting**: Implement request throttling

---

## 📧 Submission Details

**Assignment**: AI PM - Troopod  
**Submitted To**: nj@troopod.io  
**Date**: April 13, 2026  

**Includes:**
- ✅ Working FastAPI backend with two AI agents
- ✅ Frontend UI (Next.js + React + TypeScript)
- ✅ Landing page scraping via Jina.ai
- ✅ Error handling & fallback logic
- ✅ Testing results & evidence (RESULTS.md)
- ✅ Complete architecture documentation
- ✅ Installation & deployment instructions

---

**Built with ❤️ for Troopod AI PM Assignment**
