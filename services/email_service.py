
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Find .env in the project root
env_path = Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

class EmailService:
    """
    Sends screening reports via Gmail SMTP (No Domain Required).
    """
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD") # This is an APP PASSWORD, not your main password
        
    def send_report(self, dest_email, report_data):
        """
        Sends HTML formatted email report via Gmail.
        """
        if not self.gmail_user or not self.gmail_password:
            print("DEBUG: Gmail credentials missing. Skipping email.")
            return False
            
        try:
            print(f"DEBUG: Initializing Gmail SMTP for {dest_email}...")
            
            # Setup the MIME
            message = MIMEMultipart("alternative")
            message["Subject"] = f"HealthLens AI Report: {report_data['urgency']} Alert"
            message["From"] = f"HealthLens AI Screening <{self.gmail_user}>"
            message["To"] = dest_email
            
            # HTML Template
            html = self.get_template(report_data)
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Connect and Send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls() # Secure the connection
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, dest_email, message.as_string())
            server.quit()
            
            print(f"DEBUG: Gmail report delivered to {dest_email}!")
            return True
        except Exception as e:
            print(f"DEBUG: Gmail SMTP failed: {e}")
            return False

    def get_template(self, data):
        """
        The HTML template for the email report.
        """
        return f"""
        <html>
            <body style="font-family: sans-serif; line-height: 1.6; color: #333; padding: 20px;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 12px; background: white;">
                    <h2 style="color: #2563EB;">HealthLens AI Screening Result</h2>
                    <p><strong>Condition:</strong> {data['condition']}</p>
                    <p><strong>Urgency:</strong> {data['urgency']}</p>
                    <hr/>
                    <div style="padding: 10px; background: #f0f4ff; border-radius: 8px;">
                        <strong>Next Recommendation:</strong><br/>
                        {data['recommendation']}
                    </div>
                </div>
            </body>
        </html>
        """

email_service = EmailService()
