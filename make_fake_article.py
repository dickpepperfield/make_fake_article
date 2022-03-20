import os
import random
import smtplib
import ssl
import requests
import argparse
import pyunsplash
import feedparser
import tensorflow as tf
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from random_word import RandomWords
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Load environment vars
load_dotenv()

# Vars found in .env
RSS_FEED = os.getenv('RSS_FEED')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
GPT_SEED = random.randint(0,100)
GPT_MAX_LEN = random.randint(700,900)

# Function to provide user inputs and output userargs
def userArguments():
    parser = argparse.ArgumentParser(description='Generate a fake news article and post it.')
    parser.add_argument('-f', '--feed', default=RSS_FEED)
    parser.add_argument('-c', '--category', default='Technology')
    parser.add_argument('-l', '--max-length', default=GPT_MAX_LEN)
    userargs = parser.parse_args()
    return userargs

# Function to load inputs from --feed, 
# Fetches titles from an RSS feed and dumps them into tmp/feeds 
# then randomly selects one
def loadFeedTitles(userArguments):
    # Grab the feed
    feed = feedparser.parse(userArguments.feed)
    # Create a list on disk from all titles
    with open('tmp/feeds', 'w') as f:
        for item in feed.entries:
            print(item[ "title" ], file=f)   

    # Randomly select one
    random_title = random.choice(list(open('tmp/feeds')))

    return random_title

# Function to grab an image from Unsplash.com, using the --category userarg as a search term
def getImage(userArguments):
    # Connect to API
    pu = pyunsplash.PyUnsplash(api_key=UNSPLASH_API_KEY)
    # Query API for single image
    photos = pu.photos(type_='random', count=1, featured=True, query=userArguments.category)
    [photo] = photos.entries  
    # Save response to disk
    response = requests.get(photo.link_download, allow_redirects=True)
    open('tmp/unsplash_temp.png', 'wb').write(response.content)

# Function to create the text, input text that the article is built from is provided from 
# random_title, out of the tmp/feeds list
def createGPT2Text():
    # Grab a random title
    random_title = random.choice(list(open('tmp/feeds')))

    # GPT2 Stuff
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    GPT2 = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    # Input is random title from above, generate text using tensorflow
    input_sequence = random_title
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
def constructAndSendEmail(userArguments,loadFeedTitles,createGPT2Text):
    # Basic email properties
    message = MIMEMultipart("alternative")
    message["Subject"] = loadFeedTitles
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    # Create the plain-text version of the message
    text = ( f"""⚠ ALL TEXT IN THIS POST IS COMPLETELY FAKE AND AI GENERATED ⚠\n\n<a href="about-us">Read more about how it's done here.</a>\n\n""" +
            createGPT2Text + f"""\n\n
            [tags post, Daily, News, Fake, {userArguments.category}] [category {userArguments.category}]
            ⚠ ALL TEXT IN THIS POST IS COMPLETELY FAKE AND AI GENERATED ⚠\n\n<a href="about-us">Read more about how it's done here.</a>\n\n
            """)

    # Get the image and create it
    fp = open('tmp/unsplash_temp.png', 'rb')
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
    with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_SENDER, EMAIL_RECEIVER, message.as_string()
        )

# Main function
def main():
    userArguments()
    uargs = userArguments()
    loadFeedTitles(uargs)
    createGPT2Text()
    getImage(uargs)
    title = loadFeedTitles(uargs)
    content = createGPT2Text()
    constructAndSendEmail(uargs, title, content)

if __name__ == "__main__":

    main()