import json
from .chinese2Int import chinese2Int


def readJSON(path):
    with open(path, 'r') as f:
        a = json.loads(f.read())
        return a


def divide_Num_Unit(array):  # 把數字和單位分開
    sortArray = []  # 整理後的食材量，使用量和單位分開
    haveNum = False
    for i in range(len(array)):
        num = ''.join([x for x in array[i] if x.isdigit()])
        if (num != ''):
            haveNum = True
        unit = ''.join([i for i in array[i] if not i.isdigit()])
        # 把 中文數字 轉成數字
        tempNum, unit = chinese2Int(unit)  # 都是回傳字串
        if haveNum:
            try:
                if int(tempNum):
                    num += int(tempNum)
            except:
                print(tempNum)
        else:
            num = tempNum
        sortArray.append([num, unit])
        haveNum = False
    return sortArray


def combine_Num_Unit(array):  # 把數字和單位合在一起
    sortArray = []
    for i in range(len(array)):
        element = str(array[i][0]) + " " + array[i][1]
        sortArray.append(element)
    return sortArray


def UpdateIngredUnitArr(originalQuantity, crawlHeadcount, userNum):
    sortArray = divide_Num_Unit(originalQuantity)  # 整理後的食材量，使用量和單位分開
    # 人數轉換
    for i in range(len(sortArray)):
        # 原本食譜的數量
        num = sortArray[i][0]
        if (num == ''):
            continue
        if (num != '' and crawlHeadcount != '' and userNum != ''):
            # 根據使用者輸入的人數作換算
            newNum = round(
                (float(num)/float(crawlHeadcount)*float(userNum)), 1)
            # 更新食譜數量
            sortArray[i][0] = newNum
    # 更新後的食譜
    updateQuantity = combine_Num_Unit(sortArray)
    return updateQuantity


def saveData(foodList, updateQuantity, assign_headcount):
    temp_dict = dict()
    afterUnit = dict(zip(foodList, updateQuantity))
    temp_dict['headcount'] = assign_headcount  # 使用者指定的人數
    temp_dict['ingred_dict'] = afterUnit
    return temp_dict


async def arrangeData(init_headcount, cook_headcount,
                      cook_ingred_dict):
    unitList = list(cook_ingred_dict.values())
    updateQuantity = UpdateIngredUnitArr(
        unitList, cook_headcount, init_headcount)
    foodList = list(cook_ingred_dict.keys())
    result_dict = saveData(foodList, updateQuantity, init_headcount)
    return result_dict
