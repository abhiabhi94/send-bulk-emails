import smtplib
import ssl
from operator import itemgetter, attrgetter
import os
import json
import sys
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(__file__)
# print(BASE_DIR)


def join_dirs(loc):
    return os.path.join(BASE_DIR, loc)


list_loc = join_dirs('output_cleaned.xlsx')
# list_loc = join_dirs('emails(test) - Sheet1.csv')
text_loc = join_dirs('email_text.txt')
html_loc = join_dirs('email_text.html')
cred_loc = join_dirs('credentials.json')

sent_info = join_dirs('sent_info.txt')

# cred_loc = 'credentials.json'

message = MIMEMultipart("alternative")
message["Subject"] = "Collaboration for STEM Education Programs"

'''
Read file and return it's content
'''


def readFile(loc):
    with open(loc, 'r') as f:
        content = f.read()
    return content


with open(cred_loc, 'r') as f:
    cred = json.load(f)


text = readFile(text_loc)
html = readFile(html_loc)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

message.attach(part1)
message.attach(part2)

df = pd.read_excel(list_loc)
list_email = df['E-mail Address']
# Set sent to -1 for rows where email address is not present
df.loc[list_email.isnull(), 'sent'] = -1
# Extract only those dataframes where email value is present
df_email_valid = df[~list_email.isnull()]

context = ssl.create_default_context()

smtp, sender, port, pwd = itemgetter(
    'smtp', 'sender', 'port', 'password')(cred)

message["From"] = sender

with smtplib.SMTP_SSL(smtp, port, context=context) as server:
    server.login(sender, pwd)
    index_sent = df_email_valid.columns.get_loc('sent')

    for i, data in df_email_valid.iterrows():
        try:
            if "To" in message:
                message.replace_header("To", data['E-mail Address'])
            else:
                message["To"] = data['E-mail Address']
            server.sendmail(
                sender, data['E-mail Address'], message.as_string())
            df.loc[i, 'sent'] = 1
        except Exception as e:
            with open(sent_info, 'a') as f:
                f.write(
                    f'Emails send till index:{i-1}\n Last email was send to {df.loc[i-1]}\n')
            print(e)
            df.to_excel(os.path.join(BASE_DIR, 'sent.xlsx'))
        finally:
            df.to_excel(os.path.join(BASE_DIR, 'sent.xlsx'))


print('All emails were sent successfully')
