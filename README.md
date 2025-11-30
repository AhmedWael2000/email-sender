# Email Sender GUI Application

A user-friendly graphical interface for sending bulk personalized emails using HTML templates and CSV recipient lists.

## Features

- ✨ **Modern GUI Interface** - Easy-to-use interface with file browsers
- 📧 **Bulk Email Sending** - Send personalized emails to multiple recipients
- 📊 **Real-time Progress** - Track email sending progress with visual indicators
- 📝 **Detailed Logging** - View detailed logs of the email campaign
- ⚙️ **Configurable SMTP** - Support for any SMTP server (Gmail, Outlook, etc.)
- 🔒 **Secure** - Uses app-specific passwords and SSL encryption
- 💾 **Auto-load Settings** - Automatically loads configuration from .env file if present

## Requirements

- Python 3.8 or higher
- Windows operating system (for the .exe file)

## Installation

### Option 1: Run Python Script Directly

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install required packages:
   ```bash
   pip install python-dotenv
   ```
3. Run the application:
   ```bash
   python email_sender_gui.py
   ```

### Option 2: Build and Use Executable

1. Install PyInstaller:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the executable:
   ```bash
   build_exe.bat
   ```

3. The executable will be created in the `dist` folder as `EmailSender.exe`

## Usage

### 1. Prepare Your Files

#### CSV File Format
Your CSV file should have the following columns:
- `Arabic Name` - Recipient's name in Arabic
- `English Name` - Recipient's name in English  
- `Email` - Recipient's email address

Example (`recipients.csv`):
```csv
Arabic Name,English Name,Email
محمد أحمد,Mohammed Ahmed,mohammed@example.com
فاطمة علي,Fatima Ali,fatima@example.com
```

#### HTML Template
Your HTML template should contain placeholders:
- `[Arabic Name]` - Will be replaced with the Arabic name
- `[English Name]` - Will be replaced with the English name

Example:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Dear [English Name]</h1>
    <p>عزيزي [Arabic Name]</p>
    <p>Your personalized message here...</p>
</body>
</html>
```

### 2. Configure Email Settings

You can either:

**Option A: Use the GUI**
- Fill in all the fields in the "Email Configuration" section

**Option B: Use .env file**
- Create a `.env` file in the same directory as the executable
- Add your configuration:

```env
SENDER_EMAIL_TOP_SOFTWARE=your-email@gmail.com
APP_PASSWORD_TOP_SOFTWARE=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SUBJECT=Your Email Subject
HTML_TEMPLATE_PATH=path/to/your/template.html
CSV_FILE_PATH=path/to/your/recipients.csv
```

### 3. Get Gmail App Password

If using Gmail:

1. Go to your Google Account settings
2. Select "Security"
3. Enable "2-Step Verification" if not already enabled
4. Under "2-Step Verification", select "App passwords"
5. Generate a new app password for "Mail"
6. Copy the 16-character password (remove spaces)
7. Use this password in the "App Password" field

### 4. Run the Application

1. **Launch the app** (double-click `EmailSender.exe` or run `python email_sender_gui.py`)

2. **Select Files**:
   - Click "Browse..." next to "HTML Template" and select your HTML file
   - Click "Browse..." next to "CSV File" and select your recipients CSV

3. **Configure Email** (if not using .env):
   - Enter your sender email
   - Enter your app password
   - Set SMTP server and port (default: Gmail settings)
   - Set email subject

4. **Send Emails**:
   - Click "🚀 Send Emails"
   - Confirm the action
   - Monitor progress in the log area
   - Wait for completion message

### 5. Monitor Progress

The application provides:
- **Progress Bar** - Visual indication of completion
- **Status Label** - Current recipient being processed
- **Detailed Log** - Complete log of all actions and results
- **Summary** - Final statistics after campaign completion

## SMTP Settings for Popular Providers

### Gmail
- SMTP Server: `smtp.gmail.com`
- SMTP Port: `465`
- Note: Requires app-specific password (not your regular Gmail password)

### Outlook/Hotmail
- SMTP Server: `smtp-mail.outlook.com`
- SMTP Port: `587`

### Yahoo Mail
- SMTP Server: `smtp.mail.yahoo.com`
- SMTP Port: `465`

### Custom SMTP
- Contact your email provider for SMTP settings

## Features Explained

### Personalization
The application automatically replaces placeholders in your HTML template:
- `[Arabic Name]` → Replaced with the recipient's Arabic name
- `[English Name]` → Replaced with the recipient's English name

### Rate Limiting
The application automatically waits 2 seconds between emails to:
- Avoid triggering spam filters
- Stay within SMTP server rate limits
- Improve deliverability

### Error Handling
- Invalid files are detected before sending
- Failed emails are logged separately
- Campaign continues even if individual emails fail
- Detailed error messages for troubleshooting

## Troubleshooting

### "Authentication Failed"
- Make sure you're using an app-specific password (not your regular email password)
- Verify your email and password are correct
- Check that 2-factor authentication is enabled (for Gmail)

### "Connection Failed"
- Check your internet connection
- Verify SMTP server and port settings
- Check if your firewall/antivirus is blocking connections

### "Template Not Found"
- Verify the HTML template file path is correct
- Make sure the file exists and is accessible

### "No Data in CSV"
- Check that your CSV file has the correct format
- Verify column names match exactly: "Arabic Name", "English Name", "Email"
- Ensure the file is saved as UTF-8 encoding

### Emails Going to Spam
- Verify sender email domain reputation
- Avoid spam trigger words in subject/content
- Consider warming up your sending domain
- Don't send too many emails at once

## Security Notes

⚠️ **Important Security Reminders:**

1. **Never share your app password** with anyone
2. **Don't commit .env files** to version control (already in .gitignore)
3. **Use app-specific passwords**, not your main email password
4. **Keep the executable secure** as it may contain cached credentials
5. **Test with a small batch** before sending to all recipients

## Building From Source

To build the executable yourself:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   build_exe.bat
   ```

Or manually with PyInstaller:
```bash
pyinstaller --name="EmailSender" --onefile --windowed email_sender_gui.py
```

## File Structure

```
mail template/
├── email_sender_gui.py      # Main GUI application
├── send_bulk_emails.py      # Original CLI script
├── requirements.txt         # Python dependencies
├── build_exe.bat           # Build script for executable
├── .env                    # Configuration file (optional)
├── email_with_icons.html   # Your HTML template
├── Marble Factories.csv    # Your recipient list
└── dist/
    └── EmailSender.exe     # Built executable (after build)
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the log output for specific error messages
3. Verify your SMTP settings with your email provider

## License

This tool is provided as-is for personal and commercial use.

---

**Made with ❤️ for efficient email campaigns**
