:: Email Sender - Build Script
:: Creates a standalone Windows executable with custom icon
@echo off
cls
echo ============================================
echo Email Sender - Build Script
echo ============================================
echo.

:: Check if PyInstaller is installed
echo [1/5] Checking dependencies...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo    PyInstaller not found. Installing...
    pip install pyinstaller python-dotenv
    if errorlevel 1 (
        echo.
        echo ❌ Failed to install PyInstaller!
        echo    Please check your Python installation.
        pause
        exit /b 1
    )
    echo    ✅ PyInstaller installed successfully
) else (
    echo    ✅ PyInstaller is already installed
)
echo.

:: Check if icon file exists
echo [2/5] Checking icon file...
if exist email_icon.ico (
    echo    ✅ Icon file found: email_icon.ico
) else (
    echo    ⚠ Icon file not found: email_icon.ico
    echo    Building without custom icon...
)
echo.

:: Kill any running instances
echo [3/5] Preparing for build...
echo    Checking for running instances...
taskkill /F /IM EmailSender.exe >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ Closed running instance
    timeout /t 2 >nul
) else (
    echo    ✅ No running instances found
)

:: Clean old build artifacts
echo    Cleaning old build files...
if exist build (
    rmdir /s /q build 2>nul
    if exist build (
        echo    ⚠ Could not delete build folder
    ) else (
        echo    ✅ Removed build folder
    )
)

if exist dist (
    rmdir /s /q dist 2>nul
    if exist dist (
        echo    ⚠ Could not delete dist folder
    ) else (
        echo    ✅ Removed dist folder
    )
)

if exist EmailSender.spec (
    del /f /q EmailSender.spec 2>nul
    echo    ✅ Removed spec file
)
echo.

:: Build the executable
echo [4/5] Building executable...
echo    This may take 1-2 minutes...
echo.

pyinstaller --name="EmailSender" ^
    --onefile ^
    --windowed ^
    --icon=email_icon.ico ^
    --add-data ".env;." ^
    --hidden-import=tkinter ^
    --hidden-import=email.mime.multipart ^
    --hidden-import=email.mime.text ^
    --clean ^
    --noconfirm ^
    email_sender_gui.py

echo.

:: Verify the build
echo [5/5] Verifying build...
if exist "dist\EmailSender.exe" (
    echo.
    echo ============================================
    echo ✅ BUILD SUCCESSFUL!
    echo ============================================
    echo.
    echo 📍 Location: dist\EmailSender.exe
    
    for %%F in ("dist\EmailSender.exe") do (
        echo 📦 Size: %%~zF bytes
        echo 📅 Created: %%~tF
    )
    
    echo.
    echo =========================================
    echo Next Steps:
    echo =========================================
    echo 1. Find the executable in the 'dist' folder
    echo 2. Test it by double-clicking EmailSender.exe
    echo 3. Check if the custom icon appears
    echo 4. Distribute to users if everything works
    echo.
    echo To rebuild, just run this script again.
    echo =========================================
) else (
    echo.
    echo ============================================
    echo ❌ BUILD FAILED!
    echo ============================================
    echo.
    echo The executable was not created.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo - Missing dependencies
    echo - Incorrect file paths
    echo - Antivirus blocking PyInstaller
    echo.
)

echo.
pause
