import os, smtplib
from email.message import EmailMessage
from app.services.email_verification import email_subject, email_body

def send_code(recipient, code, kind):
    host=os.getenv("AL_HUDA_SMTP_HOST","")
    port=int(os.getenv("AL_HUDA_SMTP_PORT","587"))
    username=os.getenv("AL_HUDA_SMTP_USERNAME","")
    password=os.getenv("AL_HUDA_SMTP_PASSWORD","")
    sender=os.getenv("AL_HUDA_NO_REPLY_EMAIL","")
    if not all((host,username,password,sender)):
        raise RuntimeError("Email provider is not configured. Set AL_HUDA_SMTP_* and AL_HUDA_NO_REPLY_EMAIL on the secure backend.")

    msg=EmailMessage()
    msg["Subject"]=email_subject(kind)
    msg["From"]=sender
    msg["To"]=recipient
    msg["Reply-To"]=sender
    msg.set_content(email_body(code,kind))

    with smtplib.SMTP(host,port,timeout=20) as server:
        server.starttls()
        server.login(username,password)
        server.send_message(msg)
