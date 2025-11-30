---
description: Build the Email Sender executable
---

# Build Email Sender Executable

Follow these steps to create a standalone .exe file for the Email Sender application.

## Prerequisites

1. Python 3.8+ installed
2. Open a terminal in the project directory: `d:\ahmed\support wael\mail template`

## Quick Build

### Single Command Build

// turbo
```bash
.\build_exe.bat
```

This script will automatically:
- ✅ Check and install PyInstaller if needed
- ✅ Verify the icon file exists
- ✅ Close any running instances of EmailSender.exe
- ✅ Clean old build artifacts
- ✅ Build the executable with custom icon
- ✅ Verify the build succeeded

## Build Output

After successful build:
- **Executable location**: `dist\EmailSender.exe`
- **File size**: ~10-11 MB
- **Icon**: Custom blue envelope icon (if email_icon.ico exists)
- **Type**: Standalone Windows executable (no Python required)

## Manual Build (Advanced)

If you prefer to build manually:

### Step 1: Install Dependencies
```bash
pip install pyinstaller python-dotenv
```

### Step 2: Build
```bash
pyinstaller --name="EmailSender" --onefile --windowed --icon=email_icon.ico --add-data ".env;." --clean --noconfirm email_sender_gui.py
```

### Step 3: Find Executable
```
dist\EmailSender.exe
```

## Troubleshooting

### Build Failed
- Check Python is installed correctly
- Verify all source files exist
- Check antivirus isn't blocking PyInstaller

### No Icon Appearing
- Verify `email_icon.ico` exists in the project folder
- Clear Windows icon cache (reboot)
- Rebuild with `build_exe.bat`

### "File in Use" Error
- Close any running EmailSender.exe instances
- The script tries to do this automatically
- Manually kill the process if needed: `taskkill /F /IM EmailSender.exe`

## Distribution

To distribute the application:

1. Copy `dist\EmailSender.exe` 
2. Optionally include:
   - `README.md` - Full documentation
   - `QUICK_START.md` - User-friendly guide
   - Sample `.env` file (without passwords!)
   - Sample CSV and HTML templates

## Notes

- The executable is self-contained (includes Python + all dependencies)
- Works on Windows only
- No Python installation required on target machines
- Users need to configure their own SMTP settings
- Build artifacts (build/, dist/, *.spec) are in .gitignore
