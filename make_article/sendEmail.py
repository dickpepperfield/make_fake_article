from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
import ssl

def constructAndSendEmail(get_args,loadTitle,createGPT2Text):
    # Basic email properties
    message = MIMEMultipart("alternative")
    message["Subject"] = loadTitle
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    # Create the plain-text version of the message
    text = (createGPT2Text + f"""\n\n
            [tags post, Daily, News, Fake, {get_args.category}] [category {get_args.category}]
            🔔<strong>ALL TEXT IN THIS POST IS COMPLETELY FAKE AND AI GENERATED</strong>🔔<br><a href="/about">Read more about how it's done here.</a><br><br>
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
