# Misinfo Guardian - Quick Start Guide

## ✅ Setup Complete!

### What's Been Installed:
1. ✅ Python virtual environment (`.venv`)
2. ✅ Backend dependencies (FastAPI, uvicorn, langgraph, etc.)
3. ✅ Environment file (`.env`)
4. ✅ Backend server code

---

## 🚀 How to Run

### 1. Start Backend Server

**Option A: Use the batch file (easiest)**
```
Double-click: start_backend.bat
```

**Option B: Manual PowerShell**
```powershell
cd C:\Users\omwag\OneDrive\Desktop\Mumbai-Hacks\backend
$env:PYTHONPATH="C:\Users\omwag\OneDrive\Desktop\Mumbai-Hacks\backend"
C:/Users/omwag/OneDrive/Desktop/Mumbai-Hacks/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Server will run at: **http://localhost:8000**

Test it: Open http://localhost:8000/api/health in your browser

---

### 2. Install Chrome Extension

1. Open Chrome and go to: **chrome://extensions**
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select folder: `C:\Users\omwag\OneDrive\Desktop\Mumbai-Hacks\extension`
5. Extension should appear with name "Misinfo Guardian"

---

### 3. Test the Extension

1. Go to **https://twitter.com** or **https://x.com**
2. Open DevTools (F12) → Console tab
3. Scroll slowly and stop on a tweet
4. Wait ~1.3 seconds while keeping the tweet visible
5. You should see:
   - Console log: `[MisinfoGuardian] verifying tweet text: ...`
   - A verdict badge appears on the tweet (✅ Accurate, ❌ Contradicted, ⚠️ Unverified)

---

## 🔧 Configuration

### Add API Keys (Optional - for better results)

Edit `.env` file:
```
SERPER_API_KEY=your_actual_key_here
GROQ_API_KEY=your_actual_key_here
```

Without API keys, the system uses fallback DuckDuckGo search.

---

## 📁 Project Structure

```
Mumbai-Hacks/
├── extension/          # Chrome extension
│   ├── manifest.json
│   ├── content/
│   │   └── content.js  # Main detection & badge logic
│   └── background/
│       └── background.js
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── main.py     # Server entry point
│   │   └── routers/
│   │       └── verify.py  # /api/verify endpoint
│   └── tools/
│       └── search_manager.py  # Search functionality
└── .venv/              # Python environment
```

---

## 🐛 Troubleshooting

**Backend not starting?**
- Check if port 8000 is in use: `Get-NetTCPConnection -LocalPort 8000`
- Kill process: `Stop-Process -Id <PID>`

**Extension not detecting tweets?**
- Check console for errors
- Ensure backend is running (test health endpoint)
- Reload extension: chrome://extensions → Reload button

**No badges appearing?**
- Verify tweets match selector: `article[data-testid="tweet"]`
- Check Network tab for POST to `/api/verify`
- Ensure backend returns valid JSON response

---

## 📝 Current Status

✅ Backend running on localhost:8000
✅ Extension ready to install
✅ All code pushed to GitHub

**Next Steps:**
- Install extension in Chrome
- Test on Twitter/X
- Add real API keys for production use
