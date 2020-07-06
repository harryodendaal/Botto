import pymysql
import pandas as pd
class Database:
    def __init__(self,_database, _user, _password):
        self.database = _database
        self.user = _user
        self.password = _password


    def insertBot(self, strategy, trades, wins, losses, profit):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        insert_query = "insert bots (strategy, trades, wins, losses, profit)\
        values({}, {}, {}, {}, {});".format(strategy, trades, wins, losses, profit)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)

    def insertOrdersPlaced(self,botid, initiateOrderData, profittarget, stoplosstarget):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        price = 0
        commission = 0
        qty = 0
        for ele in initiateOrderData["fills"]:
            commission = commission + float(ele['commission'])
            price = price + float(ele['price'])* float(ele['qty'])
            qty = qty + float(ele['qty'])

        price = price/qty
        commission = commission

        insert_query = "insert ordersPlaced (botid, symbol, quantity, price, commission, profittarget, stoplosstarget)\
        values({}, '{}', {}, {}, {}, {}, {});".format(botid, initiateOrderData["symbol"], initiateOrderData["executedQty"], price, commission, profittarget, stoplosstarget)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)

    def insertOrdersEnded(self, botid, exitOrderData):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        
        price = 0
        commission = 0
        qty = 0
        for ele in exitOrderData["fills"]:
            commission = commission + float(ele['commission'])
            price = price + float(ele['price'])* float(ele['qty'])
            qty = qty + float(ele['qty'])

        price = price/qty
        commission = commission

        profit =  self.getData(botid=botid, what="price", where="ordersplaced") - price

        insert_query = "insert ordersEnded (botid, symbol, quantity, price, commission, profit)\
        values({}, {}, {}, {}, {}, {});".format(botid, exitOrderData["symbol"], exitOrderData["executedQty"], price, commission, profit)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)

    def getData(self, botid, what, where):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        insert_query = "select {} from {} where botid = {};".format(what,where, botid)
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()

        if what == "stoplosstarget" or what == "price":
            return answer[len(answer) - 1][0]
        return answer[0][0]


    

def main():
        Data_base = Database(_user="nativeuser", _database='bot_data', _password='365Pass')
        print(Data_base.getData(1, "price", "ordersplaced"))
        #Data_base.insertBot("'beast'", 0,0,0,0)

        
        

if __name__ == "__main__":
    main()
