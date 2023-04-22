import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    email = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    recipient = os.environ['RECIPIENT']

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(os.environ['SMTP_SERVER'], os.environ['SMTP_PORT'])
    server.starttls()
    server.login(email, password)
    server.sendmail(email, recipient, msg.as_string())
    server.quit()

def read_expected_robots_txt(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

def main():
    url = 'https://timberlin.de/robots.txt'
    expected_robots_txt = read_expected_robots_txt('expected-robots.txt')

    response = requests.get(url)

    if response.status_code != 200 or response.text.strip() != expected_robots_txt:
        subject = 'Änderung in robots.txt oder Statuscode nicht 200'
        body = f'Statuscode: {response.status_code}\n\nInhalt der robots.txt:\n\n{response.text}'
        send_email(subject, body)

if __name__ == '__main__':
    main()
