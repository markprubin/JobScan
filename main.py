import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import time
import hashlib

load_dotenv()

url_list = os.getenv("URLLIST").split(",") if os.getenv("URLLIST") else []

# Check for updates
def check_updates():
    response = requests.get(url_list)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_container = soup.find('div', class_="active")
    current_hash = hashlib.sha256(str(content_container).encode('utf-8')).hexdigest()
    
    try:
        with open("previous_hash.txt", "r") as file:
            previous_hash = file.read()
    except FileNotFoundError:
        previous_hash = None # No Previous hash if file doesn't exist
        
    # Compare previous hash to current
    if current_hash != previous_hash:
        send_email()
        # Update previous_hash.txt
        with open("previous_hash.txt", "w") as file:
                  file.write(current_hash)
    
    # Check for updates by comparing to prev. state
    # Send email notification if updates detected

subject = "Daily Job Posting Update"
body = "This is the body of the text"
sender = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
recipients = os.getenv("EMAIL").split(",") if os.getenv("EMAIL") else [] # myself in this case
  
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
    

def main():
    while True:
        check_updates()
        # Wait 1 day to check
        time.sleep(86400)
        # send_email(subject, body, sender, recipients, password)


if __name__ == '__main__':
    # main()
    check_updates()
    # send_email(subject, body, sender, recipients, password)