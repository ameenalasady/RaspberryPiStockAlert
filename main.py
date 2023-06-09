import requests
from bs4 import BeautifulSoup
from discord import SyncWebhook
import time
from datetime import datetime
import os


webhookURL = str(os.environ.get("WEBHOOK"))
webhook = SyncWebhook.from_url(webhookURL)


CanaKitLinks = ["https://www.canakit.com/raspberry-pi-4.html", "https://www.canakit.com/raspberry-pi-4-2gb.html",
                "https://www.canakit.com/raspberry-pi-4-4gb.html", "https://www.canakit.com/raspberry-pi-4-8gb.html"]

PiShopLinks = ["https://www.pishop.ca/product/raspberry-pi-4-model-b-1gb/", "https://www.pishop.ca/product/raspberry-pi-4-model-b-2gb/",
               "https://www.pishop.ca/product/raspberry-pi-4-model-b-4gb/", "https://www.pishop.ca/product/raspberry-pi-4-model-b-8gb/"]


while (True):

    try:

        CanaKitValues = []
        PiShopValues = []

        now = datetime.now()
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')

        # CanaKit:
        for i in range(len(CanaKitLinks)):
            html = requests.get(CanaKitLinks[i])
            soup = BeautifulSoup(html.content, "html.parser")
            elements = soup.find_all(id='ProductAddToCartDiv')
            CanaKitValues.append(elements[0].text)

        # PiShop:
        for i in range(len(PiShopLinks)):
            html = requests.get(PiShopLinks[i])
            soup = BeautifulSoup(html.content, "html.parser")
            elements = soup.find(id="form-action-addToCart")
            PiShopValues.append(elements.get("value"))

        print(current_time, CanaKitValues, PiShopValues)

        for i in range(len(CanaKitValues)):
            if CanaKitValues[i] != "Pre-Orders Sold Out":
                webhook.send(current_time + ": CanaKit " + str(2**i) +
                             "GB in stock. " + str(PiShopLinks[i]))

        for i in range(len(PiShopValues)):
            if PiShopValues[i] != "Out of stock":
                webhook.send(current_time + " PiShop " + str(2**i) +
                             " GB in stock. " + str(PiShopLinks[i]))
    except:
        print("Something went wrong.")

    time.sleep(10)
