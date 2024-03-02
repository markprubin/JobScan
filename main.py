import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEtext
from dotenv import load_dotenv
import os

load_dotenv()

# Check for updates

def check_updates():
    url = "www.example.com/careers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_postings = soup.find_all('div', class_='job_posting')
    
    # Check for updates by comparing to prev. state
    # Send email notification if updates detected

subject = "Email Test Subject"
body = "This is the body of the text"
sender = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
recipients = ["EMAIL"] # myself in this case
  
def send_email(subject, body, sender, recipients, password):
    msg = MIMEtext(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
    
send_email(subject, body, sender, recipients, password)

def main():
    while True:
        check_updates()
        # Wait 1 day to check
        time.sleep(86400)

if __name__ == '__main__':
    main()