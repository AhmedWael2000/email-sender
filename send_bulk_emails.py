import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import ssl
import csv
import time

load_dotenv()

# --- Configuration ---
SENDER_EMAIL = os.getenv('SENDER_EMAIL_TOP_SOFTWARE')
APP_PASSWORD = os.getenv('APP_PASSWORD_TOP_SOFTWARE')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

SUBJECT = 'نظام متخصص لإدارة مصنعك للرخام و الجرانيت | Specialized System for Your Marble and Granite Factory Management'
HTML_TEMPLATE_PATH = 'email_with_icons.html'
CSV_FILE_PATH = 'Marble Factories.csv'

# --- 1. Read the HTML Template ---
try:
    with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        html_template = file.read()
except FileNotFoundError:
    print(f"❌ Error: HTML template not found at {HTML_TEMPLATE_PATH}")
    exit()

# --- 2. Read CSV and Send Emails ---
try:
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        total_clients = 0
        success_count = 0
        failed_count = 0
        
        # Count total rows first
        rows = list(csv_reader)
        total_clients = len(rows)
        
        print(f"\n📧 Starting email campaign to {total_clients} clients...")
        print("=" * 60)
        
        for index, row in enumerate(rows, start=1):
            arabic_name = row['Arabic Name'].strip()
            english_name = row['English Name'].strip()
            recipient_email = row['Email'].strip()
            
            print(f"\n[{index}/{total_clients}] Processing: {arabic_name} ({english_name})")
            print(f"📮 Email: {recipient_email}")
            
            # --- 3. Personalize the HTML content ---
            # Replace placeholders with actual names
            personalized_html = html_template
            
            # Replace Arabic greeting placeholder
            personalized_html = personalized_html.replace(
                'تحية طيبة [السيد/ة...],',
                f'تحية طيبة {arabic_name},'
            )
            
            # Replace Arabic "To:" field
            personalized_html = personalized_html.replace(
                '<strong>إلى:</strong> [الاسم/المسمى الوظيفي للشخص المعني - مثال: مدير العمليات، المدير\n                                العام]\n                            </p>',
                f'<strong>إلى:</strong> {arabic_name}\n                            </p>'
            )
            
            # Replace English greeting
            personalized_html = personalized_html.replace(
                'Dear [Mr./Ms. ...],',
                f'Dear {english_name},'
            )
            
            # Replace English "To:" field
            personalized_html = personalized_html.replace(
                '<strong>To:</strong> [Name/Job Title of the Concerned Person - Example:\n                                            Operations Manager, General Manager]\n                                        </p>',
                f'<strong>To:</strong> {english_name}\n                                        </p>'
            )
            
            # --- 4. Create the Email ---
            msg = MIMEMultipart('alternative')
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = SUBJECT
            
            email_body = MIMEText(personalized_html, 'html', 'utf-8')
            msg.attach(email_body)
            
            # --- 5. Send the Email ---
            try:
                print(f"📤 Connecting to {SMTP_SERVER}...")
                
                context = ssl.create_default_context()
                
                # Use SMTP_SSL for port 465 (SSL connection)
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
                
                print(f"✅ SUCCESS! Email sent to {arabic_name} ({recipient_email})")
                success_count += 1
                
                # Wait 2 seconds between emails to avoid spam filters
                if index < total_clients:
                    print("⏳ Waiting 2 seconds before next email...")
                    time.sleep(2)
                
            except Exception as e:
                print(f"❌ FAILED to send to {arabic_name}: {e}")
                failed_count += 1
        
        # --- 6. Final Summary ---
        print("\n" + "=" * 60)
        print("📊 EMAIL CAMPAIGN SUMMARY")
        print("=" * 60)
        print(f"Total Clients: {total_clients}")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"Success Rate: {(success_count/total_clients*100):.1f}%")
        print("=" * 60)

except FileNotFoundError:
    print(f"❌ Error: CSV file not found at {CSV_FILE_PATH}")
except Exception as e:
    print(f"❌ An error occurred: {e}")
