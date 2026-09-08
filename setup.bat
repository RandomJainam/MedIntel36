@echo off
setlocal EnableExtensions EnableDelayedExpansion

title MedIntel360 Setup

cd /d "%~dp0"

echo.
echo ============================================================
echo                    MedIntel360 Setup
echo ============================================================
echo.
echo Project directory:
echo %CD%
echo.

REM ============================================================
REM STEP 1 - CHECK PYTHON
REM ============================================================

echo [1/10] Checking Python...
echo.

set "PYTHON_CMD="

where py >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)

where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

echo ERROR: Python was not found.
echo.
echo Please install Python 3.10 or newer and try again.
echo.
pause
exit /b 1

:python_found

echo Python command found: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM ============================================================
REM STEP 2 - CREATE VIRTUAL ENVIRONMENT
REM ============================================================

echo [2/10] Preparing virtual environment...
echo.

if exist ".venv\Scripts\python.exe" (
    echo Existing virtual environment detected.
    echo Using existing environment.
    echo.
    goto :venv_ready
)

echo Creating virtual environment...
echo.

%PYTHON_CMD% -m venv .venv

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment.
    echo.
    pause
    exit /b 1
)

echo.
echo Virtual environment created successfully.
echo.

:venv_ready

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment Python was not found.
    echo.
    pause
    exit /b 1
)

echo Virtual environment:
echo %VENV_PYTHON%
echo.

REM ============================================================
REM STEP 3 - INSTALL DEPENDENCIES
REM ============================================================

echo [3/10] Installing Python dependencies...
echo.

if not exist "requirements.txt" (
    echo ERROR: requirements.txt was not found.
    echo.
    pause
    exit /b 1
)

echo Upgrading pip...
"%VENV_PYTHON%" -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo WARNING: pip upgrade failed.
    echo Continuing with the existing pip version.
    echo.
)

echo.
echo Installing project dependencies...
echo.

"%VENV_PYTHON%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully.
echo.

REM ============================================================
REM STEP 4 - CONFIGURE ENVIRONMENT
REM ============================================================

echo [4/10] Configuring MedIntel360...
echo.

if exist ".env" (
    echo An existing .env file was found.
    echo.

    choice /C YN /N /M "Do you want to replace the existing API configuration? [Y/N]: "

    if errorlevel 2 (
        echo.
        echo Existing .env configuration will be kept.
        echo.
        goto :env_ready
    )
)

echo.
echo ------------------------------------------------------------
echo OpenRouter Configuration
echo ------------------------------------------------------------
echo.
echo The API key will be stored locally in .env.
echo .env is excluded from Git.
echo.

REM ------------------------------------------------------------
REM Masked API key input
REM ------------------------------------------------------------

for /f "delims=" %%A in ('powershell -NoProfile -Command "$p=Read-Host ''Enter OpenRouter API Key'' -AsSecureString; $b=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); try {[Runtime.InteropServices.Marshal]::PtrToStringBSTR($b)} finally {[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b)}"') do (
    set "OPENROUTER_API_KEY=%%A"
)

echo.

set /p "MODEL_NAME=Enter model name [deepseek/deepseek-chat-v3-0324]: "

if "!MODEL_NAME!"=="" (
    set "MODEL_NAME=deepseek/deepseek-chat-v3-0324"
)

(
    echo OPENROUTER_API_KEY=!OPENROUTER_API_KEY!
    echo MODEL_NAME=!MODEL_NAME!
) > ".env"

echo.
echo Environment configuration saved successfully.
echo Model: !MODEL_NAME!
echo.

:env_ready

REM ============================================================
REM STEP 5 - DATABASE
REM ============================================================

echo [5/10] Initializing database...
echo.

if not exist "database\create_database.py" (
    echo ERROR: database\create_database.py was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" database\create_database.py

if errorlevel 1 (
    echo.
    echo ERROR: Database initialization failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Database initialized successfully.
echo.

REM ============================================================
REM STEP 6 - STAR SCHEMA
REM ============================================================

echo [6/10] Building star schema...
echo.

if not exist "etl\build_star_schema.py" (
    echo ERROR: etl\build_star_schema.py was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" etl\build_star_schema.py

if errorlevel 1 (
    echo.
    echo ERROR: Star schema creation failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Star schema completed successfully.
echo.

REM ============================================================
REM STEP 7 - FEATURE ENGINEERING
REM ============================================================

echo [7/10] Building feature store...
echo.

if not exist "etl\feature_engineering_v1.py" (
    echo ERROR: etl\feature_engineering_v1.py was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" etl\feature_engineering_v1.py

if errorlevel 1 (
    echo.
    echo ERROR: Feature engineering failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Feature store completed successfully.
echo.

REM ============================================================
REM STEP 8 - GOLD LAYER
REM ============================================================

echo [8/10] Building analytics gold layer...
echo.

if not exist "etl\gold_layer.py" (
    echo ERROR: etl\gold_layer.py was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" etl\gold_layer.py

if errorlevel 1 (
    echo.
    echo ERROR: Gold layer creation failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Gold layer completed successfully.
echo.

REM ============================================================
REM STEP 9 - VERIFY APPLICATION
REM ============================================================

echo [9/10] Verifying MedIntel360 application...
echo.

if not exist "dashboard\Home.py" (
    echo ERROR: dashboard\Home.py was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" -c "import streamlit, pandas, sqlalchemy, dotenv; print('Required application packages verified.')"

if errorlevel 1 (
    echo.
    echo ERROR: Application dependency verification failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Application verification completed.
echo.

REM ============================================================
REM STEP 10 - LAUNCH APPLICATION
REM ============================================================

echo [10/10] Launching MedIntel360...
echo.

echo ============================================================
echo                 SETUP COMPLETE
echo ============================================================
echo.
echo Database        : READY
echo Star Schema     : READY
echo Feature Store   : READY
echo Gold Layer      : READY
echo Environment     : READY
echo Application     : READY
echo.
echo Starting Streamlit dashboard...
echo.
echo ============================================================
echo.

"%VENV_PYTHON%" -m streamlit run dashboard\Home.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch MedIntel360.
    echo.
    pause
    exit /b 1
)

endlocal