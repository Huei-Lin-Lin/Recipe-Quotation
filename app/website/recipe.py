from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def getRecipeData(driver, recipe, url):
    driver.get(url)

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q")),
        "找不到指定的元素"
    )
    search.clear()
    search.send_keys(recipe)
    search.send_keys(Keys.RETURN)

    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "browse-recipe-link")),
        "找不到指定的元素"
    )
    link.click()

    headcount = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "num")),
        "找不到指定的元素"
    ).text
    ingredients = driver.find_elements(By.CLASS_NAME, "ingredient-name")
    ingredients_unit = driver.find_elements(By.CLASS_NAME, "ingredient-unit")
    ingred_dict = organize_data(ingredients, ingredients_unit)
    return headcount, ingred_dict


def organize_data(ingredients, ingredients_unit):
    ingredList = []  # 食譜的食材
    unitList = []  # 食譜食材的數量
    for ingredient in ingredients:
        ingredList.append(ingredient.text)
    for u in ingredients_unit:
        unitList.append(u.text)
    ingredient_dict = dict(zip(ingredList, unitList))
    return ingredient_dict
