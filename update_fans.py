# coding: utf-8
import time
import json
import re
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://www.facebook.com/newtoydesign"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

like_match = re.search(r'([\d,]+)\s*按讚數', text)
follow_match = re.search(r'([\d,]+)\s*位+追蹤者', text)

fans = None
followers = None

if like_match:
    fans = int(like_match.group(1).replace(",", ""))
    print(f"👍 抓到按讚數：{fans} 人")
else:
    print("❌ 沒抓到按讚數")

if follow_match:
    followers = int(follow_match.group(1).replace(",", ""))
    print(f"👣 抓到追蹤者：{followers} 人")
else:
    print("❌ 沒抓到追蹤者")

driver.quit()

# ✅ 只有兩者都抓到才寫入 JSON 與 git push
if fans is not None and followers is not None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "fans": fans,
        "followers": followers,
        "updated": now
    }

    with open("fans.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("📦 fans.json 已更新")

    
    print("✅ 已 push 到 GitHub Pages")
else:
    print("⚠️ 沒有完整數據，不寫入檔案")

input("程式執行完畢，按 Enter 鍵關閉...")
