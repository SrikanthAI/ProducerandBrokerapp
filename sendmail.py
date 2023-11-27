import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def send_emails(recipient_email):
    # Email configuration
    sender_email = "noreply@getalter.ai"
    password = "vpnrllkhsxbjclkp"
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587

    # Email content
    subject = "new message is added to queue"
    message = {"name":'srikanth'}
    message = json.dumps(message, indent=4)
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            server.send_message(msg)

        print("Emails sent successfully!")
    except Exception as e:
        print("An error occurred while sending emails:", str(e))

send_emails('konneraju31@gmail.com')