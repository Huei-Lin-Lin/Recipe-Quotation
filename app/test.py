from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver_path = ".\\website\\chromedriver\\chromedriver.exe"
service = Service(executable_path=driver_path)
options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--disable-gpu')  # 關閉 GPU 避免某些系統或是網頁出錯
options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖片, 提升速度
options.add_argument('--no-sandbox')  # 以最高權限執行
options.add_argument("--disable-javascript")  # 禁用 JavaScript
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')  # 啟動時看不到任何 UI 畫面
prefs = {
    'profile.default_content_setting_values':  {
        'notifications': 2
    }
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.twfood.cc/"
driver.get(url)
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "index_search03")),
    "找不到指定的元素"
)
search = search_box.find_element(By.ID, "textfield")
search.clear()
search.send_keys('蒜頭')
search.send_keys(Keys.RETURN)
