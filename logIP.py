import public_ip as ip
import datetime, smtplib, configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read('config/config.conf')

# get the email configuration from the config file
smtp_server = config['email']['smtp_server']
port = config['email']['port']
username = config['email']['username']
password = config['email']['password']
sender_email = config['email']['sender_email']
receiver_email = config['email']['receiver_email']
subject = config['email']['subject']
send_mail = config['email']['send_mail']

# get the log file path from the config file                
log_file = config['log']['log_file']
public_ip = ip.get()


def get_current_time(): 
    return datetime.datetime.now()

def log(log_file, current_time, public_ip):
    with open(log_file, 'a') as f:
        f.write(f'Time: {current_time}, IP: {public_ip}\n')

def send_log_Mail(smtp_server, port, sender_email, receiver_email, subject, body):
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted

        # Create email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email Notification sent successfully!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.quit()

while True:
    current_time = get_current_time()
    new_public_ip = ip.get()

    if new_public_ip != public_ip:
        # Log the new IP
        public_ip = new_public_ip
        log(log_file, current_time, public_ip)
        print(f'IP changed to {public_ip}')

        if send_mail:
            # Send email notification
            body = f'IP Logging Service: The IP address has changed to {public_ip}. Time: {current_time}\n New Data written to log file.'
            send_log_Mail(smtp_server, port, sender_email, receiver_email, subject, body)

    else:
        print('No change in IP')