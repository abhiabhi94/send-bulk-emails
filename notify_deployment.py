import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
import sys
from typing import List

RECEIVERS = [
    'mail@domain.com',
    'mail1@domain1.com',
]

PORT = 465
SMTP = 'smtp.gmail.com'

sender = os.environ.get('EMAIL_USER', None)    
if not sender:
  sys.exit('Set an environment variable as EMAIL_USER to be used as the sender.')
  
PASSWORD = os.environ.get('EMAIL_PASS', None)
if not PASSWORD:
    sys.exit('Set an environment variable as EMAIL_PASS as the Password for authenticating the user')


def send_email(subject:str, msg:str, sender:str, receivers:List[str])->None:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender

    part1 = MIMEText(msg, 'plain')
    part2 = MIMEText(msg, 'html')
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP, port=PORT, context=context) as server:
        server.login(sender, PASSWORD)

        for receiver in receivers:
            message['To'] = receiver
            server.sendmail(
                sender, receiver, message.as_string())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='notify status via email')
    parser.add_argument('--site', dest='site', type=str, help='The website to be notified about')
    parser.add_argument('--subject', dest='subject', type=str, help='The subject of the email(default: Continous Development Status for `site`)')
    parser.add_argument('--msg', dest='msg', type=str, help='The message to be send during email')

    args = parser.parse_args()
    website = args.site
    if not args.subject:
        subject = f'Continous Deployment Status for the Website {website}'
    else:
        subject = args.subject

    send_email(subject=subject, msg=args.msg, sender=sender, receivers=RECEIVERS)
