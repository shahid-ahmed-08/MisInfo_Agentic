# Misinformation Guardian

An AI-powered Chrome extension and FastAPI backend that detects misinformation on Twitter/X in real-time using advanced LLM-based verification pipelines.

## 🚀 Features

- **Real-time Detection**: Automatically detects and analyzes tweets as you browse
- **AI-Powered Verification**: Uses LLM agents to extract claims, classify content, and verify information
- **Multi-Source Evidence**: Integrates with Serper and DuckDuckGo for fact-checking
- **Chrome Extension**: Seamless browser integration with overlay UI
- **FastAPI Backend**: Scalable, production-ready API server

## 📁 Project Structure

```
misinfo_guardian/
├── extension/          # Chrome extension (Manifest V3)
├── backend/            # FastAPI backend
│   ├── app/            # API routes, services, models
│   ├── agent/          # AI agent pipeline
│   ├── tools/          # Search tool integrations
│   └── common/         # Shared utilities
└── scripts/            # Deployment scripts
```

## 🛠️ Setup

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Update `.env` with your API keys:
- `SERPER_API_KEY`: Your Serper API key
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: Your LLM provider API key
- `DUCKDUCKGO_ENABLED`: Set to `true` to enable DuckDuckGo search

6. Run the backend:
```bash
python -m app.main
# Or use the script:
../scripts/run_backend.sh
```

### Extension

1. Navigate to the extension directory:
```bash
cd extension
```

2. Load the extension in Chrome:
- Open Chrome and go to `chrome://extensions/`
- Enable "Developer mode"
- Click "Load unpacked"
- Select the `extension` folder

## 🔧 Configuration

### Backend Environment Variables

See `backend/.env.example` for all available configuration options.

### Extension Settings

Configure the backend API URL in `extension/content/utils.js` or through the extension popup.

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest tests/
```

## 📝 Development

- Backend API: FastAPI with async support
- Extension: Vanilla JavaScript (Manifest V3)
- AI Pipeline: Modular agent stages (extract → classify → query → verify)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 🙏 Acknowledgments

Built for Mumbai Hacks 2024

