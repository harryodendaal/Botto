import pymysql
import pandas as pd
class Tables:
    def __init__(self,_database, _user, _password):
        self.database = _database
        self.user = _user
        self.password = _password

    def creatBotTable(self):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        insert_query = "CREATE TABLE bots (\
        botid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        strategy VARCHAR(20),\
        intrade varchar(5) default 'false',\
        trades INT,\
        wins INT,\
        losses INT,\
        profit decimal(8,3)\
        );"
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)

    def createOrdersPlacedTable(self):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        insert_query = "CREATE TABLE ordersPlaced (\
        orderid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        botid INT,\
        timetaken timestamp default now(),\
        symbol VARCHAR(20) NOT NULL,\
        quantity DECIMAL(16,8) NOT NULL,\
        price DECIMAL(16, 8) NOT NULL,\
        commission DECIMAL(16, 8) NOT NULL,\
        profittarget DECIMAL(16, 8) NOT NULL,\
        stoplosstarget DECIMAL(16, 8) NOT NULL, \
        FOREIGN KEY (botid) references bots(botid)\
        ); "
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)
    def createOrdersEndedTable(self):
        conn = pymysql.connect(database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()
        insert_query = "CREATE TABLE ordersEnded(\
        orderid int not null auto_increment primary key,\
        botid INT,\
        timetaken timestamp default now(),\
        symbol varchar(20) not null,\
        quantity DECIMAL(16, 8) NOT NULL,\
        price DECIMAL(16, 8) NOT NULL,\
        commission DECIMAL(16, 8) NOT NULL,\
        profit DECIMAL(16,8) NOT NULL,\
        FOREIGN KEY (botid) REFERENCES bots(botid)\
        ); "
        print(insert_query)
        table = cursor.execute(insert_query)
        conn.commit()
        print(table)

    
def main():
        Table = Tables(_user="nativeuser", _database='bot_data', _password='365Pass')
        
        Table.creatBotTable()
        Table.createOrdersEndedTable()
        Table.createOrdersPlacedTable()




if __name__ == "__main__":
    main()
