@echo off
SET VENV_NAME=venv

echo 🔍 Checking for Virtual Environment...

IF NOT EXIST %VENV_NAME% (
    echo 🛠️ Creating Virtual Environment: %VENV_NAME%...
    python -m venv %VENV_NAME%
) ELSE (
    echo ✅ Virtual Environment already exists.
)

echo ⚡ Activating Environment...
call %VENV_NAME%\Scripts\activate

echo 📦 Updating Pip and Installing Requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🎉 SETUP COMPLETE!
echo To start working, run: call venv\Scripts\activate
echo.
pause