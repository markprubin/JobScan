import requests
from bs4 import BeautifulSoup
import smtplib

# Check for updates

def check_updates():
    url = "www.example.com/careers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_postings = soup.find_all('div', class_='job_posting')
    
    # Check for updates by comparing to prev. state
    # Send email notification if updates detected