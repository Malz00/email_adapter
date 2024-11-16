# import smtplib
# from email.message import EmailMessage
# from jinja2 import Environment, FileSystemLoader
# from pathlib import Path
# import os
# from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL

# from dotenv import load_dotenv

# load_dotenv()
# template_dir = Path('templates') 
# env = Environment(loader=FileSystemLoader(template_dir))

# template = env.get_template('Index.html')

# email = EmailMessage()
# email['from'] =  FROM_EMAIL 
# email['to'] = 'malcolmibrahim31@gmail.com'  
# email['subject'] = 'You are really studying. Keep up the work!'

# context = {
#     'name': 'Co-writer  welcome on board we are glad to have you here', 
# }

# html_content = template.render(context)
# email.set_content(html_content, 'html')


# try:
#     with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
        
#         if not SMTP_USER or not SMTP_PASSWORD:
#             raise ValueError("SMTP credentials are missing!")

#         smtp.login(SMTP_USER, SMTP_PASSWORD)
#         smtp.send_message(email)
#         print('All good, boss! Email sent successfully.')
        
# except Exception as e:
#     print(f"Error: {e}")











import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import json
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables from .env
load_dotenv()

# Set up the template directory and Jinja2 environment
template_dir = Path('templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Load email data from JSON file
with open('data/email_data.json') as f:
    email_data = json.load(f)

# Create the email message
email = EmailMessage()
email['from'] = FROM_EMAIL
email['to'] = email_data['to_email']
email['subject'] = email_data['subject']

# Email context for the template (you can modify these)
context = {
    'name': 'Co-writer',  # Can be dynamic based on your email content
    'body': email_data['body']
}

# Render the HTML content using the template
template = env.get_template('Index.html')
html_content = template.render(context)
email.set_content(html_content, 'html')

# Function to handle file attachments
def attach_files(email, file_paths):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                # Guess the MIME type based on file extension
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                
                # Extract the file name from the path and set the content-disposition header
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{os.path.basename(file_path)}"'
                )
                
                # Attach the file to the email
                email.attach(part)
        else:
            print(f"Warning: {file_path} is not a valid file.")

# Attach the files from the email data
file_paths = email_data['attachments']
attach_files(email, file_paths)

# Send the email using SMTP
try:
    with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()  # Encrypt communication
        
        if not SMTP_USER or not SMTP_PASSWORD:
            raise ValueError("SMTP credentials are missing!")
        
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(email)
        print('All good, boss! Email sent successfully.')
        
except Exception as e:
    print(f"Error: {e}")

