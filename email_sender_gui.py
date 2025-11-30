import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import csv
import time
import os
from pathlib import Path

class EmailSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Email Sender")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Variables
        self.html_template_path = tk.StringVar()
        self.csv_file_path = tk.StringVar()
        self.sender_email = tk.StringVar()
        self.app_password = tk.StringVar()
        self.smtp_server = tk.StringVar(value="smtp.gmail.com")
        self.smtp_port = tk.StringVar(value="465")
        self.email_subject = tk.StringVar(value="Important Message")
        
        self.is_sending = False
        
        # Try to load from .env if exists
        self.load_env_config()
        
        # Setup UI
        self.setup_ui()
        
    def load_env_config(self):
        """Load configuration from .env file if it exists"""
        env_path = Path(".env")
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == 'SENDER_EMAIL_TOP_SOFTWARE':
                                self.sender_email.set(value)
                            elif key == 'APP_PASSWORD_TOP_SOFTWARE':
                                self.app_password.set(value)
                            elif key == 'SMTP_SERVER':
                                self.smtp_server.set(value)
                            elif key == 'SMTP_PORT':
                                self.smtp_port.set(value)
                            elif key == 'SUBJECT':
                                self.email_subject.set(value)
                            elif key == 'HTML_TEMPLATE_PATH':
                                self.html_template_path.set(value)
                            elif key == 'CSV_FILE_PATH':
                                self.csv_file_path.set(value)
            except Exception as e:
                print(f"Could not load .env file: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📧 Bulk Email Sender", 
                                font=('Segoe UI', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # File Selection Section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # HTML Template
        ttk.Label(file_frame, text="HTML Template:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.html_template_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_html).grid(row=0, column=2)
        
        # CSV File
        ttk.Label(file_frame, text="CSV File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.csv_file_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_csv).grid(row=1, column=2)
        
        # Email Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Email Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Sender Email
        ttk.Label(config_frame, text="Sender Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.sender_email, width=50).grid(row=0, column=1, columnspan=2, padx=5, sticky=tk.W)
        
        # App Password
        ttk.Label(config_frame, text="App Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(config_frame, textvariable=self.app_password, width=50, show="*")
        password_entry.grid(row=1, column=1, columnspan=2, padx=5, sticky=tk.W)
        
        # SMTP Server
        ttk.Label(config_frame, text="SMTP Server:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.smtp_server, width=30).grid(row=2, column=1, padx=5, sticky=tk.W)
        
        # SMTP Port
        ttk.Label(config_frame, text="SMTP Port:").grid(row=2, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        ttk.Entry(config_frame, textvariable=self.smtp_port, width=10).grid(row=2, column=3, padx=5, sticky=tk.W)
        
        # Email Subject
        ttk.Label(config_frame, text="Email Subject:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(config_frame, textvariable=self.email_subject, width=50).grid(row=3, column=1, columnspan=2, padx=5, sticky=tk.W)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to send emails", 
                                      font=('Segoe UI', 10))
        self.status_label.pack(pady=(0, 10))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=12, 
                                                   font=('Consolas', 9),
                                                   bg='#1e1e1e', fg='#d4d4d4',
                                                   insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.send_button = ttk.Button(button_frame, text="🚀 Send Emails", 
                                       command=self.start_sending_emails,
                                       style='Accent.TButton')
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏸ Stop", 
                                       command=self.stop_sending,
                                       state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Clear Log", 
                   command=self.clear_log).pack(side=tk.RIGHT)
        
        # Configure styles
        self.configure_styles()
    
    def configure_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        # You can customize styles here if needed
        
    def browse_html(self):
        """Browse for HTML template file"""
        filename = filedialog.askopenfilename(
            title="Select HTML Template",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            self.html_template_path.set(filename)
    
    def browse_csv(self):
        """Browse for CSV file"""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file_path.set(filename)
    
    def log(self, message, tag=None):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        if tag:
            # You can add color tags here
            pass
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """Validate all required inputs"""
        if not self.html_template_path.get():
            messagebox.showerror("Error", "Please select an HTML template file")
            return False
        
        if not self.csv_file_path.get():
            messagebox.showerror("Error", "Please select a CSV file")
            return False
        
        if not self.sender_email.get():
            messagebox.showerror("Error", "Please enter sender email")
            return False
        
        if not self.app_password.get():
            messagebox.showerror("Error", "Please enter app password")
            return False
        
        if not self.smtp_server.get():
            messagebox.showerror("Error", "Please enter SMTP server")
            return False
        
        if not self.smtp_port.get():
            messagebox.showerror("Error", "Please enter SMTP port")
            return False
        
        if not self.email_subject.get():
            messagebox.showerror("Error", "Please enter email subject")
            return False
        
        # Check if files exist
        if not os.path.exists(self.html_template_path.get()):
            messagebox.showerror("Error", "HTML template file not found")
            return False
        
        if not os.path.exists(self.csv_file_path.get()):
            messagebox.showerror("Error", "CSV file not found")
            return False
        
        return True
    
    def start_sending_emails(self):
        """Start sending emails in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Confirm before sending
        response = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to start sending emails?\n\n"
            f"Template: {os.path.basename(self.html_template_path.get())}\n"
            f"Recipients: {os.path.basename(self.csv_file_path.get())}"
        )
        
        if not response:
            return
        
        # Disable send button and enable stop button
        self.send_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_sending = True
        
        # Start sending in a separate thread
        thread = threading.Thread(target=self.send_emails_thread)
        thread.daemon = True
        thread.start()
    
    def stop_sending(self):
        """Stop sending emails"""
        self.is_sending = False
        self.log("\n⏸ Stopping email campaign...")
        self.status_label.config(text="Stopped by user")
        self.send_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def send_emails_thread(self):
        """Thread function to send emails"""
        try:
            # Read HTML template
            with open(self.html_template_path.get(), 'r', encoding='utf-8') as file:
                html_template = file.read()
            
            # Read CSV file
            with open(self.csv_file_path.get(), 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                rows = list(csv_reader)
                total_clients = len(rows)
                
                if total_clients == 0:
                    self.log("❌ No data found in CSV file")
                    self.send_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    return
                
                self.progress_bar['maximum'] = total_clients
                self.progress_bar['value'] = 0
                
                success_count = 0
                failed_count = 0
                
                self.log(f"\n📧 Starting email campaign to {total_clients} clients...")
                self.log("=" * 60)
                
                for index, row in enumerate(rows, start=1):
                    if not self.is_sending:
                        break
                    
                    arabic_name = row.get('Arabic Name', '').strip()
                    english_name = row.get('English Name', '').strip()
                    recipient_email = row.get('Email', '').strip()
                    
                    if not recipient_email:
                        self.log(f"⚠ Skipping row {index}: No email provided")
                        continue
                    
                    self.log(f"\n[{index}/{total_clients}] Processing: {arabic_name} ({english_name})")
                    self.log(f"📮 Email: {recipient_email}")
                    self.status_label.config(text=f"Sending to {recipient_email} ({index}/{total_clients})")
                    
                    # Personalize HTML
                    personalized_html = html_template
                    personalized_html = personalized_html.replace('[Arabic Name]', f'{arabic_name},')
                    personalized_html = personalized_html.replace('[English Name]', f'{english_name},')
                    
                    # Create email
                    msg = MIMEMultipart('alternative')
                    msg['From'] = self.sender_email.get()
                    msg['To'] = recipient_email
                    msg['Subject'] = self.email_subject.get()
                    
                    email_body = MIMEText(personalized_html, 'html', 'utf-8')
                    msg.attach(email_body)
                    
                    # Send email
                    try:
                        self.log(f"📤 Connecting to {self.smtp_server.get()}...")
                        
                        context = ssl.create_default_context()
                        
                        with smtplib.SMTP_SSL(self.smtp_server.get(), 
                                             int(self.smtp_port.get()), 
                                             context=context) as server:
                            server.login(self.sender_email.get(), self.app_password.get())
                            server.sendmail(self.sender_email.get(), recipient_email, msg.as_string())
                        
                        self.log(f"✅ SUCCESS! Email sent to {arabic_name} ({recipient_email})")
                        success_count += 1
                        
                        # Update progress
                        self.progress_bar['value'] = index
                        
                        # Wait between emails
                        if index < total_clients and self.is_sending:
                            self.log("⏳ Waiting 2 seconds before next email...")
                            time.sleep(2)
                        
                    except Exception as e:
                        self.log(f"❌ FAILED to send to {arabic_name}: {str(e)}")
                        failed_count += 1
                
                # Final summary
                self.log("\n" + "=" * 60)
                self.log("📊 EMAIL CAMPAIGN SUMMARY")
                self.log("=" * 60)
                self.log(f"Total Clients: {total_clients}")
                self.log(f"✅ Successful: {success_count}")
                self.log(f"❌ Failed: {failed_count}")
                if total_clients > 0:
                    self.log(f"Success Rate: {(success_count/total_clients*100):.1f}%")
                self.log("=" * 60)
                
                self.status_label.config(text=f"Completed: {success_count}/{total_clients} sent successfully")
                
                messagebox.showinfo(
                    "Campaign Complete",
                    f"Email campaign completed!\n\n"
                    f"Total: {total_clients}\n"
                    f"✅ Successful: {success_count}\n"
                    f"❌ Failed: {failed_count}"
                )
        
        except Exception as e:
            self.log(f"\n❌ An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.send_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.is_sending = False


def main():
    root = tk.Tk()
    app = EmailSenderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
