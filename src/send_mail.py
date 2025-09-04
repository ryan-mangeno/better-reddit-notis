import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECV_EMAIL")
app_password = os.getenv("GOOGLE_APP_PASSWORD")


def send_email(subject, body, image_path=None):
  """
     sends a notification to an email, I am sending an email to msyelf from one email to another
     google uses app passwords to get past 2fa 
  """

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # sends a photo if included
    if image_path:
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
            img_name = os.path.basename(image_path)
            msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=img_name)

    #  Gmail SMTP
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
