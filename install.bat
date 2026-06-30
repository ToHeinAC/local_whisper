@echo off
cd /d "%~dp0"

if not exist ".env" (
    echo Creating .env from .env.example ...
    copy /y ".env.example" ".env" >nul
)

echo Installing dependencies with uv ...
uv sync || goto :error

echo Downloading whisper model ...
uv run python -m src.download_model || goto :error

echo Creating desktop shortcut ...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\create_shortcut.ps1"

echo.
echo Installation complete. Launch with run.bat or the desktop shortcut.
pause
exit /b 0

:error
echo.
echo Installation failed. See messages above.
pause
exit /b 1
