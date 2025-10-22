@echo off
echo ========================================
echo  🎓 UniQuest College Search Chatbot
echo ========================================
echo.
echo Starting the backend server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import flask, pandas, flask_cors" >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies are ready!
echo.
echo 🚀 Starting UniQuest backend server...
echo    Backend will be available at: http://localhost:5000
echo    Frontend should be opened at: frontend/index.html
echo.
echo ⚠️  Keep this window open while using the chatbot
echo ⚠️  Press Ctrl+C to stop the server
echo.

cd backend
python chatbot.py

pause