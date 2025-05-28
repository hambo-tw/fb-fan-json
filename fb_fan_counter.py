from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from bs4 import BeautifulSoup

# 建立 headless 瀏覽器選項
options = Options()
options.headless = False  # 先顯示瀏覽器畫面，debug 比較方便
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

# 載入粉絲團網址
url = 'https://www.facebook.com/newtoydesign'
driver.get(url)

# 等待載入完成
time.sleep(10)

# 取得 HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

# 嘗試抓「按讚數」
like_match = re.search(r'([\d,]+)\s*按讚數', text)
follow_match = re.search(r'([\d,]+)\s*位+追蹤者', text)

if like_match:
    print(f"👍 抓到按讚數：{like_match.group(1)} 人")
else:
    print("❌ 沒抓到按讚數")

if follow_match:
    print(f"👣 抓到追蹤者：{follow_match.group(1)} 人")
else:
    print("❌ 沒抓到追蹤者")

driver.quit()
