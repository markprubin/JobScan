import json
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import difflib
from dotenv import load_dotenv

load_dotenv()

def load_urls():
    with open('urls.json', 'r') as file:
        return json.load(file)

def check_updates(websites_dict):
    email_body = ""
    any_updates = False

    for website_name, config in websites_dict.items():
        url = config['url']
        find_all_params = config['find_all_params']
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_containers = soup.find_all(**find_all_params)
        
        new_content = ""
        for container in content_containers:
            new_content += f"{container.get_text(strip=True)}<br>"

        # Check for updates.txt file and read its content
        try:
            with open("updates.txt", "r") as file:
                old_content = file.read()
        except FileNotFoundError:
            old_content = ""  # If the file doesn't exist, consider it as empty

        # Compare the old content with the new content
        differ = difflib.Differ()
        differences = list(differ.compare(old_content.splitlines(), new_content.splitlines()))
        updates = [line for line in differences if line.startswith('+ ') or line.startswith('- ')]

        if updates:
            any_updates = True
            update_text = '\n'.join(updates)
            email_body += f"{website_name}\n{update_text}\n\n"

    if any_updates:
        send_email(subject, email_body, sender, recipients, password)
    else:
        send_email("Daily Job Posting Update - No Changes", "No updates found today.", sender, recipients, password)

    subject = "Daily Job Posting Update"
    sender = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    recipients = os.getenv("EMAIL").split(",") if os.getenv("EMAIL") else [] # myself in this case
    
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def main():
    websites_dict = load_urls()
    check_updates(websites_dict)

if __name__ == '__main__':
    main()
