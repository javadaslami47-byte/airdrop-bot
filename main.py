import requests
from bs4 import BeautifulSoup
import time
import os

# --- اطلاعات شما ---
TELEGRAM_TOKEN = '8740696167:AAHSCQete8X7EMDVcFovV9RBjaJnMy-KEJA'
CHAT_ID = '391754544'
MY_WALLET = 'UQDo6vfO8kdvGNATer9nsTEki3ljoGLKoHmS2opGsafmSwxj'
FILE_NAME = "seen_airdrops.txt"

def send_telegram(message):
    # استفاده از پروکسی واسطه برای عبور از محدودیت تونل PythonAnywhere
    # این آدرس پیام شما را به سرور تلگرام منتقل می‌کند
    proxies = {
        'http': 'http://proxy.server:3128',
        'https': 'http://proxy.server:3128',
    }
    
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        # ارسال درخواست از طریق پروکسی داخلی خود PythonAnywhere
        response = requests.post(url, json=payload, proxies=proxies, timeout=20)
        return response.status_code == 200
    except Exception as e:
        print(f"خطای تونل/اتصال: {e}")
        # تلاش مجدد بدون پروکسی (برخی سرورها مستقیم وصل می‌شوند)
        try:
            requests.post(url, json=payload, timeout=15)
        except: pass
        return False

def get_latest_airdrops():
    url = "https://airdrops.io"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w') as f: pass

        response = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = soup.find_all('article', class_='air-article')
        
        with open(FILE_NAME, 'r') as f:
            seen_items = f.read().splitlines()

        for air in airdrops:
            try:
                content = air.find('div', class_='air-content').find('a')
                name = content.text.strip()
                link = content['href']
                
                if name not in seen_items:
                    msg = f"🚀 **ایردراپ جدید!**\n\n📌 پروژه: `{name}`\n👛 ولت: `{MY_WALLET}`\n🔗 [لینک]({link})"
                    if send_telegram(msg):
                        with open(FILE_NAME, 'a') as f:
                            f.write(name + "\n")
            except: continue
    except Exception as e:
        print(f"خطا در دریافت سایت: {e}")

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    send_telegram("✅ اتصال با موفقیت برقرار شد!")
    while True:
        get_latest_airdrops()
        time.sleep(3600)
