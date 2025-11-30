# Quick Start Guide - Email Sender

## For Users (Non-Technical)

### What You Need

1. **EmailSender.exe** - The application file
2. **Your email HTML template** - The email design file (.html)
3. **Your recipient list** - A CSV file with names and emails
4. **Your email credentials** - Email address and app password

---

## Step-by-Step Instructions

### 1️⃣ Get Your Gmail App Password

Before using the app, you need a special password from Gmail:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click "Security" on the left
3. Make sure "2-Step Verification" is ON
4. Scroll down and click "App passwords"
5. Select "Mail" and your device
6. Copy the 16-character password (it looks like: `xxxx xxxx xxxx xxxx`)
7. **Save this password** - you'll need it in the app

### 2️⃣ Launch the Application

- Double-click **EmailSender.exe**
- A window will open with the Email Sender interface

### 3️⃣ Select Your Files

**HTML Template:**
- Click the **"Browse..."** button next to "HTML Template"
- Find and select your email template file (ends with `.html`)
- Click "Open"

**Recipient List:**
- Click the **"Browse..."** button next to "CSV File"
- Find and select your recipient list (ends with `.csv`)
- Click "Open"

### 4️⃣ Enter Email Settings

Fill in the following fields:

- **Sender Email**: Your Gmail address (e.g., `yourname@gmail.com`)
- **App Password**: Paste the 16-character password from Step 1
- **SMTP Server**: Leave as `smtp.gmail.com` (for Gmail)
- **SMTP Port**: Leave as `465` (for Gmail)
- **Email Subject**: Type the subject line for your emails

### 5️⃣ Send Your Emails

1. Click the **"🚀 Send Emails"** button
2. A confirmation window will appear - click **"Yes"**
3. Watch the progress bar and log messages
4. When complete, you'll see a summary message

### 6️⃣ Review Results

The app will show you:
- ✅ How many emails were sent successfully
- ❌ How many failed (if any)
- 📊 Overall success rate

---

## Your CSV File Format

Your recipient list should be a CSV file with these exact column names:

```
Arabic Name,English Name,Email
محمد أحمد,Mohammed Ahmed,mohammed@example.com
فاطمة علي,Fatima Ali,fatima@example.com
أحمد حسن,Ahmed Hassan,ahmed@example.com
```

**Important:**
- First row must have: `Arabic Name,English Name,Email`
- Each person gets their own row
- Separate columns with commas
- Save the file as CSV (not Excel)

---

## Your HTML Template

Your email template should include these placeholders:

- `[Arabic Name]` - Will be replaced with each person's Arabic name
- `[English Name]` - Will be replaced with each person's English name

**Example:**
```html
<h1>Dear [English Name]</h1>
<p>عزيزي [Arabic Name]</p>
<p>We are pleased to inform you...</p>
```

---

## Tips for Success

✅ **Test First**: Send to yourself or a test email first
✅ **Check Spam**: Ask recipients to check their spam folder
✅ **Small Batches**: For first-time use, start with 5-10 recipients
✅ **Wait Time**: The app waits 2 seconds between emails (this is normal)
✅ **Keep Window Open**: Don't close the app while sending

---

## Troubleshooting

### Problem: "Authentication Failed"
**Solution**: 
- Make sure you're using the app password (not your regular Gmail password)
- Check that 2-factor authentication is enabled in Google

### Problem: "File Not Found"
**Solution**: 
- Make sure you clicked "Browse" and selected the correct files
- Check that the files are not deleted or moved

### Problem: Emails going to spam
**Solution**: 
- Ask recipients to mark your email as "Not Spam"
- Avoid using too many capital letters or exclamation marks
- Make sure your email content looks professional

### Problem: "Connection Failed"
**Solution**: 
- Check your internet connection
- Make sure your firewall isn't blocking the app
- Verify the SMTP settings are correct

---

## Need Help?

1. Check the detailed **README.md** file
2. Review the log messages in the app
3. Try sending to just one person first to test

---

## Safety Reminders

🔒 **Never share your app password** with anyone
🔒 **Don't send the .exe file with your password** saved
🔒 **Test before sending** to everyone
🔒 **Keep backups** of your CSV and HTML files

---

**Happy Emailing! 📧**
