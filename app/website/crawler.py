from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import asyncio


async def crawler(init_cuisine, init_headcount):
    driver_path = "http://selenium:4444/wd/hub"
    # driver_path = ".\\website\\chromedriver\\chromedriver.exe"

    recipeURL = "https://icook.tw"
    twfoodURL = 'https://www.twfood.cc/'

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
    # driver = webdriver.Chrome(service=service, options=options)

    driver = webdriver.Remote(options=options, command_executor=driver_path)

    from .recipe import getRecipeData
    cook_headcount, cook_ingred_dict = getRecipeData(
        driver, init_cuisine, recipeURL)

    from .quotation import quotation
    quotation_food_dict = await quotation(cook_ingred_dict, twfoodURL, driver)

    from .dataArrange import arrangeData
    result_dict = await arrangeData(init_headcount, cook_headcount,
                                    cook_ingred_dict)

    return quotation_food_dict, result_dict
