import sqlite3
import pandas as pd


class Tables:
    def __init__(self, _database, _user, _password):
        self.database = _database
        self.user = _user
        self.password = _password

    def creatBotTable(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "CREATE TABLE IF NOT EXISTS bots (\
        botid INTEGER PRIMARY KEY AUTOINCREMENT,\
        strategy text,\
        intrade text,\
        trades INT,\
        wins INT,\
        losses INT,\
        profit REAL\
        );"
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close()
        print(table)

    def createOrdersPlacedTable(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "CREATE TABLE IF NOT EXISTS ordersPlaced (\
        orderid INTEGER PRIMARY KEY AUTOINCREMENT,\
        botid interger,\
        timetaken text,\
        symbol text,\
        quantity real,\
        price real,\
        commission real,\
        profittarget real,\
        stoplosstarget real, \
        FOREIGN KEY (botid) references bots(botid)\
        ); "
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close()
        print(table)

    def createOrdersEndedTable(self):
        conn = sqlite3.connect('bots.db')
        cursor = conn.cursor()
        insert_query = "CREATE TABLE IF NOT EXISTS ordersEnded(\
        orderid INTEGER PRIMARY KEY AUTOINCREMENT,\
        botid interger,\
        timetaken text,\
        symbol text,\
        quantity real,\
        price real,\
        commission real,\
        profit real,\
        FOREIGN KEY (botid) REFERENCES bots(botid)\
        ); "
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        conn.close()
        print(table)


def main():
    Table = Tables(_user="nativeuser", _database='bot_data',
                   _password='365Pass')

    Table.creatBotTable()
    Table.createOrdersEndedTable()
    Table.createOrdersPlacedTable()


if __name__ == "__main__":
    main()
