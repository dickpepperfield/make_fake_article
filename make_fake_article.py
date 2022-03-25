import os
import random
import smtplib
import ssl
import requests
import argparse
import feedparser
import tensorflow as tf
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from pexels_api import API
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load environment vars
load_dotenv()

# Vars found in .env
RSS_FEED = os.getenv('RSS_FEED')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
GPT_SEED = random.randint(0,100)
GPT_MAX_LEN = random.randint(700,900)


# For development, use a smaller number here so it runs faster
# GPT_MAX_LEN = 50

# Function to provide user inputs and output userargs
def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Generate a fake news article and post it.')
    parser.add_argument('-f', '--feed', type=str, default=RSS_FEED, help="The feed to use, in XML format")
    parser.add_argument('-c', '--category', type=str, default='Technology', help="Category of RSS feed, is used for the image search as well.")
    parser.add_argument('-l', '--max-length', type=int, default=GPT_MAX_LEN, help="Number of tokens used in text generation.")
    return parser.parse_args(argv)

# Function to grab an image from Unsplash.com, using the --category userarg as a search term
def getImage(get_args):
    # Setup requests.get resiliancy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    # Connect PEXELS API
    api = API(PEXELS_API_KEY)
    api.search(get_args.category, page=random.randint(0,20), results_per_page=1)
    photos = api.get_entries()
    # Grab landscape image
    for photo in photos:
        response = http.get(photo.landscape, allow_redirects=True, timeout=10)
        open('tmp/temp_img.png', 'wb').write(response.content)

def loadTitle(get_args):
    feed = feedparser.parse(get_args.feed)
    with open('tmp/feeds', 'w') as f:
        for item in feed.entries:
            print(item[ "title" ], file=f) 

    Title = random.choice(list(open('tmp/feeds')))
    return Title

# Function to create the text, input text that the article is built from is provided from 
# random_title, out of the tmp/feeds list
def createGPT2Text(loadTitle):
    # GPT2 Stuff
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    GPT2 = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    # Input is random title from above, generate text using tensorflow
    input_sequence = loadTitle
    input_ids = tokenizer.encode(input_sequence, return_tensors='tf')
    sample_output = GPT2.generate(
                             input_ids,
                             do_sample = True,
                             max_length = GPT_MAX_LEN,
                             top_k = 0,
                             temperature = 0.8
    )
    # Output here
    GPT2Output = tokenizer.decode(sample_output[0], skip_special_tokens = True)

    return GPT2Output

# Function to construct the email, attach the article and image, and then send it to 
# post to email. Has a few hard coded shortcodes that could be ripped out for userargs 
# and sensible defaults.
def constructAndSendEmail(get_args,loadTitle,createGPT2Text):
    # Basic email properties
    message = MIMEMultipart("alternative")
    message["Subject"] = loadTitle
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    # Create the plain-text version of the message
    text = (createGPT2Text + f"""\n\n
            [tags post, Daily, News, Fake, {get_args.category}] [category {get_args.category}]
            ⚠ ALL TEXT IN THIS POST IS COMPLETELY FAKE AND AI GENERATED ⚠\n\n<a href="about-us">Read more about how it's done here.</a>\n\n
            """)

    # Get the image and create it
    fp = open('tmp/temp_img.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')

    # Turn these into plain/html MIMEText objects
    messageText = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(messageText)
    message.attach(msgImage)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(
                EMAIL_SENDER, EMAIL_RECEIVER, message.as_string()
            )

# Main function
def main():
    userargs = get_args()
    getImage(userargs)

    title = loadTitle(userargs)
    content = createGPT2Text(title)

    constructAndSendEmail(userargs, title, content)

if __name__ == "__main__":

    main()