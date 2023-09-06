from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from ..model import Food
from .. import db


def element_exists(driver, mode, str):
    try:
        driver.find_element(mode, str)
        return True
    except:
        return False


def getQuotationResult(url, driver, notQueryList, foodDict):
    for food in notQueryList:
        driver.get(url)
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "index_search03")),
            "找不到指定的元素"
        )
        search = search_box.find_element(By.ID, "textfield")
        search.clear()
        search.send_keys(food)
        search.send_keys(Keys.RETURN)
        try:
            name = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-left")),
                "找不到指定的元素"
            )
            if name and element_exists(driver, By.CLASS_NAME, "text-price") == False:
                name.find_element(By.TAG_NAME, "a").click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "text-left")),
                    "找不到指定的元素"
                )
            price = driver.find_element(By.CLASS_NAME, "text-price").text
            unit = driver.find_element(
                By.CLASS_NAME, "vege_chart_th_unit").text
            foodDict[food] = [price, unit]
            insert_food = Food(food, price, unit)
            db.session.add(insert_food)
            db.session.commit()
        except:
            foodDict[food] = "找不到結果"
            continue
    driver.quit()
    return foodDict


def queryFoodPrice(foodList):
    tempDict = dict()  # 蔬菜估價結果
    for food in foodList:
        result = Food.query.filter_by(name=food).first()
        if result == None:
            tempDict[food] = None
        else:
            tempDict[food] = [result.price, result.unit]
    return tempDict


def getNotQuery(foodDict):
    notQueryList = []
    for key, value in foodDict.items():
        if value == None:
            notQueryList.append(key)
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
