import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "your mail"
SENDER_PASSWORD = "password"
RECEIVER_EMAIL = "receiver mail"


def send_summary_email(alerts):
    if not alerts:
        return

    body = "🚨 Disaster Alert Summary\n\n"

    for i, alert in enumerate(alerts, 1):
        body += f"""
{i}. Disaster Type: {alert['disaster_type']}
   Location: {alert['location']}
   
   Priority: {alert['priority']}
   
   Advice: {alert['advice']}

"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "🚨 Disaster Alert Notification"

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email notification sent")
    except Exception as e:
        print("❌ Email failed:", e)
