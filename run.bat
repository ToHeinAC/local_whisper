@echo off
cd /d "%~dp0"

set "UV=%~dp0tools\uv.exe"
if exist "%UV%" goto run

where uv >nul 2>nul
if %errorlevel%==0 (
    set "UV=uv"
    goto run
)

echo [local_whisper] uv not found. Please run install.bat first.
pause
exit /b 1

:run
"%UV%" run python -m src.main
