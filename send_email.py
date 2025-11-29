import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()
# --- Configuration ---
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
SUBJECT = 'نظام متخصص لإدارة مصنعك للرخام و الجرانيت | Specialized System for Your Marble and Granite Factory Management'
HTML_FILE_PATH = 'email_with_icons.html'

# --- 1. Read the HTML Content ---
try:
    with open(HTML_FILE_PATH, 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print(f"Error: HTML file not found at {HTML_FILE_PATH}")
    exit()

# --- 2. Create the Email Structure ---
msg = MIMEMultipart('alternative')
msg['From'] = SENDER_EMAIL
msg['To'] = RECIPIENT_EMAIL
msg['Subject'] = SUBJECT

# Attach the HTML content
# 'html' indicates the type, 'utf-8' ensures Arabic characters display correctly
email_body = MIMEText(html_content, 'html', 'utf-8')
msg.attach(email_body)

# --- 3. Send the Email via Gmail's SMTP Server ---
try:
    print(f"Connecting to Gmail server...")
    # Connect to Gmail's SMTP server (Port 587 is for TLS)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() # Secure the connection
    
    # Login using your App Password
    server.login(SENDER_EMAIL, APP_PASSWORD)
    
    # Send the email
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    
    print(f"✅ Success! Email sent to {RECIPIENT_EMAIL}")

except Exception as e:
    print(f"❌ An error occurred: {e}")
finally:
    # Close the connection
    try:
        server.quit()
    except:
        pass