@echo off
echo Starting Misinfo Guardian Backend...
cd /d "%~dp0backend"
set PYTHONPATH=%~dp0backend
"%~dp0.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
