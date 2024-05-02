import json
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
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

        new_content = dict()
        for params in find_all_params:
            posting_blocks = soup.find_all(params['name'], class_=params['class'])

            for block in posting_blocks:
                posting_id = block.get(params['job_data']['job_id']['attr'])
                posting_name = block.find(
                    params['job_data']['job_title']['name'],
                    {
                        params['job_data']['job_title']['attr']:
                            params['job_data']['job_title']['value']
                    }).get_text(strip=True)

                new_content[posting_id] = posting_name

        old_content = load_old_content(website_name)

        # Compare old content with new
        updates = {k: v for k, v in new_content.items() if old_content.get(k) != v}

        if updates:
            any_updates = True
            update_text = '<br><br>'.join(updates.values())
            email_body += f"{website_name}<br><br>{update_text}<br>"

        save_new_content(website_name, new_content)


    subject = "Daily Job Posting Update"
    sender = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    recipients = os.getenv("EMAIL").split(",") if os.getenv("EMAIL") else [] # myself in this case

    if any_updates:
        send_email(subject, email_body, sender, recipients, password)
    else:
        send_email("Daily Job Posting Update - No Changes", "No updates found today.", sender, recipients, password)


def load_old_content(website_name):
    try:
        with open(f"{website_name}_updates.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_new_content(website_name, content):
    with open(f"{website_name}_updates.json", "w") as file:
        json.dump(content, file)


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
