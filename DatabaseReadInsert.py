import sqlite3
import pandas as pd
import datetime
class Database:
    def insertBot(self, intrade, strategy, trades, wins, losses, profit):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "insert into bots (intrade, strategy, trades, wins, losses, profit)\
        values('{}', '{}', {}, {}, {}, {});".format(intrade, strategy, trades, wins, losses, profit)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close()

        print(table)

    def insertOrdersPlaced(self,botid, initiateOrderData, profittarget, stoplosstarget):
        state = "true"
        self.changebotstate(botid, state)
        conn = sqlite3.connect('bots.db')
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

        insert_query = "insert into ordersPlaced (botid, timetaken, symbol, quantity, price, commission, profittarget, stoplosstarget)\
        values({}, {}, '{}', {}, {}, {}, {}, {});".format(botid, datetime.datetime.now(),  initiateOrderData["symbol"], initiateOrderData["executedQty"], price, commission, profittarget, stoplosstarget)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close()
        print(table)

    def insertOrdersEnded(self, botid, exitOrderData):
        state = "false"
        self.changebotstate(botid, state)
        conn = sqlite3.connect('bots.db')
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

        insert_query = "insert into ordersEnded (botid, timetaken, symbol, quantity, price, commission, profit)\
        values({}, {}, {}, {}, {}, {}, {});".format(botid, datetime.datetime.now(), exitOrderData["symbol"], exitOrderData["executedQty"], price, commission, profit)
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close
        print(table)

    def changebotstate(self, botid, state):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "update bots set intrade {} where botid = {};".format(state, botid)
        cursor.execute(insert_query)
        conn.commit()
        conn.close

    def getData(self, botid, what, where):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "select {} from {} where botid = {};".format(what,where, botid)
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()
        conn.close()


        if what == "stoplosstarget" or what == "price":
            return answer[len(answer) - 1][0]
        return answer[0][0]


    
#def insertBot(self, strategy, trades, wins, losses, profit):

def main():
        conn = Database()
        conn.insertBot(intrade='false' , strategy='beast', trades=0, wins=0, losses=0, profit=0)

        print(conn.getData(1, 'intrade', 'bots'))
        #this is the initializing of the bot
        print('yes')
        

        
        

if __name__ == "__main__":
    main()
