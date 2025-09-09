#!/usr/bin/env python3

import smtplib
import logging
from email.message import EmailMessage
import ssl

LOGFILE = "smtp_client.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")

def send_email(smtp_host, smtp_port, username, password, sender, recipient, subject, body, use_tls=True):
    try:
        logging.info("Preparing message")
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)
        logging.info("Connecting to SMTP server %s:%s", smtp_host, smtp_port)
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.set_debuglevel(1)  # show SMTP dialog on stdout
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=ssl.create_default_context(), timeout=10)
            server.set_debuglevel(1)
        if username and password:
            server.login(username, password)
            logging.info("Logged in as %s", username)
        server.send_message(msg)
        logging.info("Message sent to %s", recipient)
        server.quit()
        print("Email sent (check logs for SMTP conversation).")
    except Exception as ex:
        logging.exception("Error sending email: %s", ex)
        print("Error sending email:", ex)

if __name__ == "__main__":
    # For Gmail SMTP, use EXACT host spelling
    smtp_host = "smtp.gmail.com"
    # Uncomment below ONLY if DNS keeps failing (ping smtp.gmail.com first!):
    # smtp_host = "74.125.133.109"  # Temporary fix if DNS doesn't work
    smtp_port = 587  # For STARTTLS; use 465 with use_tls=False for SSL
    username = "31sumitsheoran@gmail.com"     # Your Gmail address
    password = "welp dlbr fyty fxoh"          # Your Gmail app password, NOT your main password
    sender = "31sumitsheoran@gmail.com"       # Should match username for Gmail
    recipient = "ssheoansumit@gmail.com"      # Make sure this is a valid address!
    subject = "CN Lab Assignment 2 - SMTP test"
    body = "Hello,\n\nThis is a test email sent by smtp_client.py for CN Lab Assignment 2.\n\nRegards,\nYour Name"
    print("This script will attempt to send an email. Edit the credentials at top of file before running.")
    send_email(smtp_host, smtp_port, username, password, sender, recipient, subject, body, use_tls=True)
