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
    msg['Reply-To'] = email 
    body=f"""
    You have received a new message from your website contact form.

    Here are the details:

    Name: {name}
    Email: {email}
    Message: 
    {message}
"""
    msg.set_content(body)
    with smtplib.SMTP(smtp_host,smtp_port) as server:
        server.starttls()
        server.login(smtp_user,smtp_pass)
        server.send_message(msg)


def send_user_confirmation_email(
        smtp_host:str,
        smtp_port:int,
        smtp_user:str,
        smtp_pass:str,
        sender:str,
        user_email:str,
        user_name:str
)-> None: 
    msg = EmailMessage()
    msg['Subject'] = "Thank you for contacting us!"
    msg['From'] = sender
    msg['To'] = user_email
    body=f"""
    Hi {user_name},
    Thank you for reaching out! I have received your message and will get back to you shortly.

    Best regards,
    Damianos Zoumpos
    -----
    This is an automated confirmation email.
"""
    msg.set_content(body)
    with smtplib.SMTP(smtp_host,smtp_port) as serveer:
        serveer.starttls()
        serveer.login(smtp_user,smtp_pass)
        serveer.send_message(msg)