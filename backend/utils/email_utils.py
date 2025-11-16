import re
import smtplib 
from email.message import EmailMessage
def check_email(email) -> bool:
    """Check if the provided email address is valid."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def send_contact_email(
        smtp_host:str, 
        smtp_port:int,
        smtp_user:str,
        smtp_pass:str, 
        sender:str,
        recipient:str,
        name:str,
        email:str,
        message:str
)-> None:
    #email structure
    msg = EmailMessage()
    msg['Subject'] = f"New contact form submission from {name}"
    msg['From'] = sender 
    msg['To'] = recipient
    #TODO: CONTINUE 
    pass 