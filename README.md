# Misinfo Guardian — Agentic Misinformation Detection System

Misinfo Guardian is an **agentic AI system** that detects misinformation in real-time using:

- **LangGraph agent loops**
- **Reflection + Retry strategy**
- **Local MCP (Model Context Protocol) server**
- **Resilient web search tool (Serper + DuckDuckGo fallback)**
- **FastAPI backend**
- Optional Chrome Extension for inline fact checking

This project was built for a 24-hour hackathon with a focus on reliability, accuracy, and agentic reasoning.

---

## 🚀 Features

- Extracts claims automatically from text
- Generates rich search queries
- Uses MCP server to run web search tools
- Scores evidence and determines factual verdicts
- Reflection Loop: retries and improves results for low-confidence cases
- End-to-end FastAPI interface (`/api/verify`)
- Fully modular architecture for extension integration

---

## 🧠 Architecture

```
misinfo_guardian/
├── backend/ # FastAPI + LangGraph agent
├── infra/   # MCP server, tools, search layer
├── extension/ # Chrome extension (optional, future)
└── README.md
```

---

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- LangGraph
- MCP Protocol (custom server)
- Serper API + DuckDuckGo fallback
- Uvicorn
- Requests

---

## 🔧 Setup Instructions

### 1. Clone repo

```bash
git clone <YOUR_REPO_URL>
cd misinfo_guardian
```

### 2. Create .env file

```bash
cp .env.example .env
```

Add your `SERPER_API_KEY` and any other keys.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MCP Server

```bash
cd infra/mcp
python server.py
```

Must print:

```
[registry] Registered tool: search
TOOL_REGISTRY contains: ['search']
```

### 5. Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

**Swagger UI:**
http://127.0.0.1:8000/docs

### 6. Test Agentic Engine

```bash
python -m agent.test_agent
```

---

## 🧪 API Usage

**POST** `/api/verify` 

```json
{
  "text": "Claim to fact-check"
}
```

**Response:**

- `claim` 
- `queries` 
- `sources` 
- `verdict` 
- `confidence` 
- `attempts` 
- `reasoning` 

---

## 📦 Future Work

- Chrome extension for inline fact-checking
- Historical misinformation patterns
- Multi-source credibility scoring
- Real-time news monitoring

---

## 📝 License

MIT License (included in LICENSE file)
