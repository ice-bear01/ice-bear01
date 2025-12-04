import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from dotenv import load_dotenv

load_dotenv() 

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """
    Create Gmail API service using OAuth2 refresh token.
    """
    creds = Credentials(
        None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        scopes=SCOPES,
    )
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(to_email: str, code: str, purpose: str = "register"):
    """
    Send a verification email via Gmail API with Glass-style design.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    #sender_email = "yourpersonalemail@gmail.com" (uncomment this if you want your personal email to be used)
    #But this is NOT recommended because:not secure accidentally pushes your email into GitHub still requires a matching refresh token

    
    # Email content based on purpose
    if purpose == "register":
        subject = "Glass - Verify Your Email"
        heading = "Welcome to Glass"
        body_text = "Thank you for signing up with Glass!"
    elif purpose == "reset":
        subject = "Glass - Password Reset Verification Code"
        heading = "Password Reset Request"
        body_text = "You requested to reset your password. Use this code to proceed."
    else:
        subject = "Glass - Verification Code"
        heading = "Email Verification"
        body_text = "Use the verification code below to continue."

    # Plain text fallback
    text = f"[Glass] Your verification code is: {code}"

    # HTML email content
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <body style="font-family: Arial, sans-serif; background: linear-gradient(to bottom, #e0f7ff, #f4f4f4); padding: 40px;">
        <div style="max-width: 500px; margin: auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
          <h2 style="color: #006989; text-align: center; font-size: 28px; margin-bottom: 20px;">{heading}</h2>
          <p style="font-size: 16px; color: #006989; margin-bottom: 10px;">Hello,</p>
          <p style="font-size: 16px; color: #006989; line-height: 1.5; margin-bottom: 30px;">
            {body_text}<br>
            Your verification code is:
          </p>
          <div style="text-align: center; margin: 20px 0;">
            <span style="display: inline-block; font-size: 28px; font-weight: bold; color: white; background: #006989; padding: 10px 25px; border-radius: 8px; letter-spacing: 4px;">
              {code}
            </span>
          </div>
          <p style="font-size: 14px; color: #006989; text-align: center; margin-top: 20px;">
            If you didn’t request this code, please ignore this email.
          </p>
          <p style="font-size: 12px; color: #999; text-align: center; margin-top: 25px;">
            © {datetime.datetime.now().year} Glass. All rights reserved.
          </p>
        </div>
      </body>
    </html>
    """

    # Create MIME message
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Glass <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Encode and send
    try:
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service = get_gmail_service()
        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
