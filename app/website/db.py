import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('USER')
passwd = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')


class MyDB:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.db = None

    def connect(self):
        try:
            config = {
                'user': self.user,
                'password': self.passwd,
                'host': self.host,
                'port': self.port,
                'database': self.db_name,
                'auth_plugin': 'mysql_native_password'
            }
            mydb = mysql.connector.connect(**config)
            # 生成一個遊標物件 ( 相當於 cmd 開啟 mysql 中的 mysql> )
            self.db = mydb
            print("連線結果", mydb)  # 印出連線結果
        except:
            print("資料庫連接失敗：")

    def getFoodPrice(self, str):
        # 定義 SQL 語句
        cursor = self.db.cursor(dictionary=True)
        sql = 'select * from foodprice WHERE foodName LIKE \'%{str}%\' '.format(
            str=str)
        cursor.execute(sql)  # 執行 SQL 語句
        result = cursor.fetchall()  # 獲取返回結果
        cursor.close()
        return result
