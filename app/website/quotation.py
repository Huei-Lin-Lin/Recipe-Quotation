import json
# from .model import Food
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from .db import getFoodPrice


def getQuotationResult(url, driver, notQueryList, foodDict):
    for food in notQueryList:
        driver.get(url)
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "index_search03")),
            "找不到指定的元素"
        )
        search = search_box.find_element(By.ID, "textfield")
        search.clear()
        search.send_keys('蒜頭')
        search.send_keys(Keys.RETURN)
        try:
            name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-left")),
                "找不到指定的元素"
            ).text
            price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-price")),
                "找不到指定的元素"
            ).text
            unit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "vege_chart_th_unit")),
                "找不到指定的元素"
            ).text
            foodDict[food] = [price, unit]
        except:
            print(f"找不到 {food} 的結果")
            continue
    driver.quit()
    return foodDict


def queryFoodPrice(foodList):
    from . import db
    tempDict = dict()  # 蔬菜估價結果
    for food in foodList:
        # result = Food.query.filter_by(name=food).first()
        # if db.cursor == None:
        # db.cursor = db.connect()
        result = db.getFoodPrice(food)
        print(len(result), result)
        if result == []:
            tempDict[food] = '找不到結果'
        else:
            tempDict[food] = [result[0]['price'], result[0]['unit']]
    return tempDict


def getNotQuery(foodDict):
    notQueryList = []
    for key, value in foodDict.items():
        if value == None:
            notQueryList = key
        else:
            continue
    return notQueryList


async def quotation(ingred_dict, url, driver):
    foodList = ingred_dict.keys()
    # 先查資料庫的價格
    foodDict = queryFoodPrice(foodList)
    # 把還沒有查到價格的食材列出來
    notQueryList = getNotQuery(foodDict)
    # 再爬蟲查菜價
    foodDict = getQuotationResult(
        url, driver, notQueryList, foodDict)
    return foodDict
