import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL

from dotenv import load_dotenv

load_dotenv()
template_dir = Path('templates') 
env = Environment(loader=FileSystemLoader(template_dir))

template = env.get_template('Index.html')

email = EmailMessage()
email['from'] =  FROM_EMAIL 
email['to'] = 'malcolmibrahim31@gmail.com'  
email['subject'] = 'You are really studying. Keep up the work!'

context = {
    'name': 'Co-writer  welcome on board we are glad to have you here', 
}

html_content = template.render(context)
email.set_content(html_content, 'html')


try:
    with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        
        if not SMTP_USER or not SMTP_PASSWORD:
            raise ValueError("SMTP credentials are missing!")

        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(email)
        print('All good, boss! Email sent successfully.')
        
except Exception as e:
    print(f"Error: {e}")
