from re import sub
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import time
import difflib

load_dotenv()

# Single URL
url = os.getenv("URLLIST")
# List of URLs
# url_list = os.getenv("URLLIST").split(",") if os.getenv("URLLIST") else []


# Check for updates
def check_updates():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_container = soup.find('div', class_="postings-wrapper")
    new_content = content_container.get_text(strip=True)
    
    try:
        with open("updates.txt", "r") as file:
            old_content = file.read()
    except FileNotFoundError:
        old_content = "" # Assume no existing file put in empty string

    differ = difflib.Differ()
    differences = list(differ.compare(old_content.splitlines(), new_content.splitlines()))

    # Ensures that only real updates are passed, and any whitespace that occurs due to no changes being made does not trigger a "change"
    updates = [line for line in differences if line.startswith('+') or line.startswith('-') or line.startswith('?')]
    
    if updates:
        update_text = '\n'.join(updates)
        send_email(subject, update_text, sender, recipients, password)
        
        # Update updates.txt
        with open("updates.txt", "w") as file:
            file.write(new_content)
            
    else:
        no_updates_message = "No updates found today."
        send_email("Daily Job Posting Update - No Changes", no_updates_message, sender, recipients, password)

subject = "Daily Job Posting Update"
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
        
        # Timer
        # time.sleep(86400)


if __name__ == '__main__':
    # main()
    check_updates()
    
    # To test send_email function ()
    # send_email(subject, body, sender, recipients, password)