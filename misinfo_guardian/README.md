# Misinfo Guardian

A comprehensive misinformation detection and prevention system built with Chrome Extension, FastAPI backend, and advanced search infrastructure.

## 🎯 Overview

Misinfo Guardian helps users identify and verify potentially misleading information on the web through real-time analysis and fact-checking capabilities.

## 📁 Project Structure

```
misinfo_guardian/
├── extension/          # Chrome Extension (Person A)
│   ├── content/
│   │   └── overlay/   # UI overlay code
│   ├── background/    # Background service worker
│   └── manifest.json  # Extension manifest
│
├── backend/           # FastAPI + Agent Logic (Person B)
│   ├── app/          # FastAPI application
│   ├── agent/        # Agent logic
│   └── tools/        # Agent tools
│
└── infra/            # Search tools, MCP, integration, logs (Person C)
    ├── mcp/          # MCP integration
    ├── search/       # Search tools
    ├── storage/      # Storage utilities
    └── scripts/      # Infrastructure scripts
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for extension development)
- Chrome/Chromium browser

### Extension Setup

1. Navigate to `extension/` directory
2. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension/` directory

### Backend Setup

1. Navigate to `backend/` directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Infrastructure Setup

1. Navigate to `infra/` directory
2. Configure MCP and search tools
3. Set up storage and logging

## 🛠️ Development

### Contributing

This project is organized by component ownership:
- **Person A**: Chrome Extension development
- **Person B**: FastAPI backend and agent logic
- **Person C**: Search tools, MCP integration, and infrastructure

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributors

- Person A: Chrome Extension
- Person B: FastAPI + Agent Logic
- Person C: Search tools, MCP, integration, logs

