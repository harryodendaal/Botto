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

    def insertOrdersPlaced(self, botid, initiateOrderData, profittarget, stoplosstarget):
       
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()

        price = 0
        commission = 0
        qty = 0

        for ele in initiateOrderData["fills"]:
            commission = commission + float(ele['commission'])
            price = price + float(ele['price']) * float(ele['qty'])
            qty = qty + float(ele['qty'])

        price = price/qty
        commission = commission


        insert_query = "insert into ordersPlaced (botid, timetaken, symbol, quantity, price, commission, profittarget, stoplosstarget)\
        values({}, {}, '{}', {}, {}, {}, {}, {});".format(botid, "'{}'".format(datetime.datetime.now()),  initiateOrderData["symbol"], initiateOrderData["executedQty"], price, commission, profittarget, stoplosstarget)
        print(insert_query)
        table = cursor.execute(insert_query)

        conn.commit()
        conn.close()

        #executes that trade occured if not errors
        state = "true"
        transactionType = 'orderplaced'
        self.changebotstate(botid, state, transactionType)

    def insertOrdersEnded(self, botid, exitOrderData):

        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()

        price = 0
        commission = 0
        qty = 0

        for ele in exitOrderData["fills"]:
            commission = commission + float(ele['commission'])
            price = price + float(ele['price']) * float(ele['qty'])
            qty = qty + float(ele['qty'])

        price = price/qty
        commission = commission

        profit = (price - self.getData(botid=botid, what="price",where="ordersplaced"))/price

        insert_query = "insert into ordersEnded (botid, timetaken, symbol, quantity, price, commission, profit)\
        values({}, {}, '{}', {}, {}, {}, {});".format(botid, "'{}'".format(datetime.datetime.now()), exitOrderData["symbol"], exitOrderData["executedQty"], price, commission, profit)
        print(insert_query)
        table = cursor.execute(insert_query)

        conn.commit()
        conn.close

        #executes that trade occured if not errors
        state = "false"
        transactionType = 'orderended'
        self.changebotstate(botid, state, transactionType)


    def changebotstate(self, botid, state, transactionType):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "update bots set intrade={} where botid = {};".format(state, botid)
        cursor.execute(insert_query)



        if transactionType == 'orderplaced':
            
            trades = self.getData(botid, what='trades', where='bots') + 1
            insert_query = 'update bots set trades={} where botid = {};'.format(trades, botid)
            cursor.execute(insert_query)

        if transactionType == 'orderended':

            newprofit = self.getData(botid, what='profit', where='ordersEnded')
            oldprofit = self.getData(botid, what='profit', where='bots')
            
            profit = oldprofit + newprofit
            if newprofit > 0:
                winloss = 'wins'
                amount = self.getData(botid, what='wins', where='bots') + 1
            else:
                winloss = 'losses'
                amount = self.getData(botid, what='losses', where='bots') + 1
            

            insert_query = 'update bots set profit = {}, {}={} where botid = {};'.format(profit, winloss, amount, botid)
            cursor.execute(insert_query)

        conn.commit()
        conn.close

    def getData(self, botid, what, where):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "select {} from {} where botid = {};".format(what, where, botid)
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()
        conn.close()

        if what == "stoplosstarget" or what == "price":
            return answer[len(answer) - 1][0]
        return answer[0][0]

    def allBotData(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "select * from bots;"
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()
        conn.close()
        print(answer)

    def allOrderPlaceData(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "select * from ordersPlaced;"
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()
        conn.close()
        print(answer)

    def allOrderEndedData(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "select * from ordersEnded;"
        cursor.execute(insert_query)
        answer = cursor.fetchall()
        conn.commit()
        conn.close()
        print(answer)
        
    def test(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()


        insert_query = "insert into ordersEnded (botid, timetaken, symbol, quantity, price, commission, profit)        values(1, '2020-08-07 19:27:16.774309', 'ETHUSDT', 0.05250000, 372.32, 0.0195468, 4.7900000000000205);"
        table = cursor.execute(insert_query)

        conn.commit()
        conn.close

        #executes that trade occured if not errors
        state = "false"


# def insertBot(self, strategy, trades, wins, losses, profit):

def main():
    conn = Database()
    #insert initial bot


    # conn.insertBot(intrade='0', strategy='rsi',trades=0, wins=0, losses=0, profit=0)

    #conn.test()
    #get tables data

    print("Trade end data")
    conn.allOrderEndedData()
    print("Trade place data")
    conn.allOrderPlaceData()
    print("Trade bot data")
    conn.allBotData()

    # conn.changebotstate(botid=1, state='false')
    # print(conn.getData(1, 'intrade', 'bots'))
    # this is the initializing of the bot

if __name__ == "__main__":
    main()
