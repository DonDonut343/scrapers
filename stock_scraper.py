import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# URL of the web page to scrape
url = '<website>'

# Function to fetch the web page content
def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Function to extract the desired element from the page
def extract_stock_info(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    # Replace 'your_element_id_or_class' with the actual ID or class of the element you want to monitor
    stock_element = soup.find('div', {'id': 'product-form__inventory.inventory'})
    return stock_element.text.strip() if stock_element else None

# Function to send an email notification
def send_email_notification(item_name, current_stock, recipient_email):
    sender_email = '<email adress>'
    sender_password = '<app password>'
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = f"Stock Alert: {item_name} is available!"

    body = f"De {item_name} is {current_stock}. Orderen!!"
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Notification email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error sending email notification: {e}")

# Main function to monitor the stock and send notifications
def main():
    while True:
        page_content = get_page_content(url)
        if page_content:
            stock_info = extract_stock_info(page_content)
            if stock_info:
                if 'Binnenkort beschikbaar' not in stock_info:
                    # Replace 'Item Name' with the name of the item you are monitoring
                    item_name = '<...>'
                    recipient_email = '<email adress>'
                    send_email_notification(item_name, stock_info, recipient_email)
                    # Add optional code here to send an SMS notification via Twilio if desired
                    send_sms_notification(item_name, stock_info, '<number>')
            else:
                print("Niet op voorraad.", flush=True)
        else:
            print("Failed to fetch the page content.", flush=True)

        # Adjust the time interval (in seconds) as per your preference (e.g., check every hour) (now: every 30 s)
        time.sleep(30)

if __name__ == '__main__':
    main()

# Function to send SMS

from twilio.rest import Client

# Replace these with your Twilio credentials
twilio_account_sid = '<ID>'
twilio_auth_token = '<auth>'
twilio_phone_number = '<...>'

# Function to send an SMS notification using Twilio
def send_sms_notification(item_name, current_stock, recipient_phone_number):
    client = Client(twilio_account_sid, twilio_auth_token)
    message_body = f"De {item_name} is {current_stock}. Orderen!!"
    try:
        client.messages.create(from_=twilio_phone_number, to=recipient_phone_number, body=message_body)
        print("SMS notification sent successfully!")
    except Exception as e:
        print(f"Error sending SMS notification: {e}")

