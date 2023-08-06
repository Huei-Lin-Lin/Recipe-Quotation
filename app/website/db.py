import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')


# def connect(user, password, host, port, db_name):
#     try:
#         config = {
#             'user': user,
#             'password': password,
#             'host': host,
#             'port': port,
#             'database': db_name,
#             'auth_plugin': 'mysql_native_password'
#         }
#         mydb = mysql.connector.connect(**config)
#         if mydb.is_connected():
#             print("資料庫連線成功")
#             # 生成一個遊標物件 ( 相當於 cmd 開啟 mysql 中的 mysql> )
#             return mydb
#         else:
#             print("資料庫連接失敗 1")
#     except Error as e:
#         print("資料庫連接失敗 2", e)


# def getFoodPrice(self, str):
#     # 定義 SQL 語句
#     cursor = self.db.cursor(dictionary=True)
#     sql = 'select * from food WHERE name = "{str}" '.format(
#         str=str)
#     cursor.execute(sql)  # 執行 SQL 語句
#     result = cursor.fetchall()  # 獲取返回結果
#     cursor.close()
#     return result

def connect(user, password, host, port, database):
    try:
        config = {
            'user': user,
            'password': password,
            'host': host,
            'port': port,
            'database': database,
            'auth_plugin': 'mysql_native_password'
        }
        mydb = mysql.connector.connect(**config)
        if mydb.is_connected():
            print("資料庫連線成功")
        # 生成一個遊標物件 ( 相當於 cmd 開啟 mysql 中的 mysql> )
        # self.db = mydb
            return mydb
        else:
            print("資料庫連接失敗 1")
    except Error as e:
        print("資料庫連接失敗 2", e)


def getFoodPrice(str):
    # 定義 SQL 語句
    try:
        mydb = connect(user, password, host, port, db_name)  # 連接 DB，讓資料自動組織成字典
        cursor = mydb.cursor(dictionary=True)
        sql = 'select * from food WHERE name = "{str}" '.format(
            str=str)
        cursor.execute(sql)  # 執行 SQL 語句
        result = cursor.fetchall()  # 獲取返回結果
        cursor.close()
        mydb.close()
        return result
    except Error as e:
        print("資料庫連接失敗 2", e)
