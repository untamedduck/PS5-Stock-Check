import json
import smtplib
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage

log = ""


def check_availablility(url, phrase):
    global log
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features="html.parser")

        if phrase in soup.text:
            return False
        return True
    except:
        log += "Error parsing website"


def main():
    url = "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6523169.p?skuId=6523169"
    phrase = "Sold Out".casefold()
    available = check_availablility(url, phrase)
    logfile = open('Log.txt', 'r+')
    successmessage = "PS5 is available"
    if successmessage in logfile.read():
        print("PS5 found in stock already")
        return

    if available:
        log += successmessage
        try:
            with open('config.json') as file:
                config = json.load(file)
                username = config["username"]
                password = config["password"]
                fromAddress = config["fromAddress"]
                toAddress = config["toAddress"]
        except:
            log += "error"

        msg = EmailMessage()
        msg['subject'] = "Playstation in stock"
        msg['from'] = fromAddress
        msg["To"] = toAddress
        msg.set_content("PS5 is in stock at" + url)

        server = smtplib.SMTP("smptp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()

    if __name__ == "__main__":
        main()
