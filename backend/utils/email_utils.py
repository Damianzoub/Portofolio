import re
import os
import resend
from dotenv import load_dotenv
load_dotenv()
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
def send_email(to:str,subject:str,html:str):
    return resend.Emails.send({
        "from":os.getenv("EMAIL_FROM"),
        "to":[to],
        "subject":subject,
        "html":html
    })

def send_contact_email(name:str,email:str,message:str):
    return resend.Emails.send({
        "from":EMAIL_FROM,
        "to":[EMAIL_TO],
        "reply_to":email,
        "subject":f"New message from {name}",
        "html":f"""
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Message:</b> {message}</p>
        """
    })

def send_user_confirmation_email(user_email:str,user_name:str):
    resend.Emails.send({
        "from":EMAIL_FROM,
        "to":[user_email],
        "subject": "Got your message (Automated Message)",
        "html": f"<p>Hi {user_name}, thanks for reaching out - I'll contact you soon</p>"
    })


def check_email(email) -> bool:
    """Check if the provided email address is valid."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

