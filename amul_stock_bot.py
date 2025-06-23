import time
import requests
import os
import telegram
from bs4 import BeautifulSoup

# Telegram bot setup
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
bot = telegram.Bot(token=BOT_TOKEN)

# Product URLs to monitor
PRODUCTS = {
    "High Protein Buttermilk": "https://shop.amul.com/en/product/amul-high-protein-buttermilk-200-ml-or-pack-of-30",
    "High Protein Plain Lassi": "https://shop.amul.com/en/product/amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "High Protein Rose Lassi": "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# To avoid duplicate alerts
last_notified = {name: False for name in PRODUCTS}

def is_in_stock(product_name, url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        btn = soup.find('button', class_='action primary tocart')
        return btn and 'Add to Cart' in btn.text
    except Exception as e:
        print(f"Error checking {product_name}: {e}")
        return False

def check_and_notify():
    for name, url in PRODUCTS.items():
        in_stock = is_in_stock(name, url)
        if in_stock and not last_notified[name]:
            message = f"✅ *{name}* is now IN STOCK!\\n[Buy Now]({url})"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
            last_notified[name] = True
        elif not in_stock:
            last_notified[name] = False

if __name__ == '__main__':
    while True:
        check_and_notify()
        time.sleep(300)  # check every 5 minutes
