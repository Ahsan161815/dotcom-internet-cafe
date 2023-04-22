import sqlite3
import datetime
from os import remove, path
from tkinter import messagebox

class pc_data:
    def __init__(self):
        conn = sqlite3.connect('data.db',timeout=60)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS pc_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT(10),
            time TEXT(10),
            pc_name TEXT(10),
            pc_time TEXT(10),
            rate TEXT(10),
            received TEXT(10),
            difference TEXT(10))''')
        conn.commit()
        conn.close()
        
    def insert(self, date, time, pc_name, pc_time, rate, received, difference):
        '''(date, pc_name, time, rate, difference) -> None
        Create pc_data.db if not exists, creates table pc_data1 if not exists and inserts data into it'''
        conn = sqlite3.connect('data.db', timeout=20)
        cur = conn.cursor()
        cur.execute('''INSERT INTO pc_data(
            date,
            time,
            pc_name,
            pc_time,
            rate,
            received,
            difference) VALUES(
            :date,
            :time,
            :pc_name,
            :pc_time,
            :rate,
            :received,
            :difference)''',{'date':date,'time':time,'pc_name':pc_name,
                             'pc_time':pc_time, 'rate':rate,
                             'received':received,
                             'difference':difference})
        conn.commit()
        conn.close()


    def retrive(self, date):
        '''Detailed view of pc data'''
        l = list()
        each = ''
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM pc_data WHERE date=(?)''',(date,))
        for line in cur:
            l.append(line)
         
        conn.commit()
        conn.close()
        return l

    def retrive_today(self, date):
        '''today page view of pc data'''
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('Select received, difference from pc_data where date=(?)',(date,))
        count = 0
        total_rate = 0
        total_difference = 0
        for x in cur:
            total_rate += int(x[0])
            total_difference += int(x[1])
            count += 1
        conn.commit()
        conn.close()
        return {'total_rate':total_rate, 'total_difference':total_difference, 'qty':count}

    def retrive_administrator(self, from_date, to_date):
        '''today page view of pc data'''
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT received, difference
            from pc_data
            where date BETWEEN (?) AND (?)''',(from_date, to_date))
        count = 0
        total_rate = 0
        total_difference = 0
        for x in cur:
            total_rate += int(x[0])
            total_difference += int(x[1])
            count += 1
        conn.commit()
        conn.close()
        return {'total_rate':total_rate, 'total_difference':total_difference, 'qty':count}

    def admin_detail_pc_data(self,  from_date, to_date):
        l = list()
        each = ''
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM pc_data
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date''',(from_date, to_date))
        for line in cur:
            l.append(line)
         
        conn.commit()
        conn.close()
        return l

class expances_and_income:
    def __init__(self):
        with open('final_date','r') as final:
            self.date = final.readline()
        self.today_date = str(datetime.date.today())
        
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS expances(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT(10),
            time TEXT(10),
            description TEXT(20),
            amount TEXT(10))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT(20),
            time TEXT(10),
            description TEXT(20),
            amount TEXT(10))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS monthly_expance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT(20),
            time TEXT(10),
            description TEXT(20),
            amount TEXT(10))''')
        conn.commit()
        conn.close()
    def insert_expances(self, description, amount):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO expances(
        date,
        time,
        description,
        amount) VALUES(
        :date,
        :time,
        :description,
        :amount)''',{'date':self.date,'time':current_time,'description':description,'amount':amount})
        conn.commit()
        conn.close()
        return None
        
    def insert_income(self, description, amount):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO income(
        date,
        time,
        description,
        amount) VALUES(
        :date,
        :time,
        :description,
        :amount)''',{'date':self.date,'time':current_time,'description':description,'amount':amount})
        conn.commit()
        conn.close()
        return None
    
    def insert_monthly(self, description, amount):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO monthly_expance(
        date,
        time,
        description,
        amount) VALUES(
        :date,
        :time,
        :description,
        :amount)''',{'date':self.date,'time':current_time,'description':description,'amount':amount})
        conn.commit()
        conn.close()
        return None

    def retrive_expances(self, date):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount FROM expances WHERE date=(?)''',(date,))
        amount = 0
        for (x, y) in cur:
            amount = amount+int(int(y))
        conn.commit()
        conn.close()
        return amount
    def retrive_income(self, date):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount FROM income WHERE date=(?)''',(date,))
        amount = 0
        for (x, y) in cur:
            amount = amount+int(int(y))
        conn.commit()
        conn.close()
        return amount

    def retrive_administrator_expances(self, from_date, to_date):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount
            FROM expances
            WHERE date BETWEEN (?) AND (?)''',(from_date, to_date))
        amount = 0
        for (x, y) in cur:
            amount = amount+int(int(y))
        conn.commit()
        conn.close()
        return amount

    def retrive_administrator_income(self, from_date, to_date):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount
            FROM income
            WHERE date BETWEEN (?) AND (?)''',(from_date, to_date))
        amount = 0
        for (x, y) in cur:
            amount = amount+int(int(y))
        conn.commit()
        conn.close()
        return amount

    def retrive_administrator_monthly(self, from_date, to_date):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount
            FROM monthly_expance
            WHERE date BETWEEN (?) AND (?)''',(from_date, to_date))
        amount = 0
        for (x, y) in cur:
            amount = amount+int(int(y))
        conn.commit()
        conn.close()
        return amount

    def retrive_income_for_text_box(self, date):
        '''(self)-> list

        Connects to data.db income table and retrives
        all data by date with description and income in list form'''
        l = list()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount FROM income WHERE date=(?)''',(date,))
        amount = 0
        for x in cur:
            l.append(x)
        conn.commit()
        conn.close()
        return l

    def retrive_expances_for_text_box(self, date):
        '''(self)-> list

        Connects to data.db expances table and retrives
        all data by date with description and income in list form'''
        l = list()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT description,amount FROM expances WHERE date=(?)''',(date,))
        for x in cur:
            l.append(x)
        conn.commit()
        conn.close()
        return l
    
    def retrive_income_for_text_box_admin(self, from_date, to_date):
        '''(self)-> list

        Connects to data.db income table and retrives
        all data by date with description and income in list form'''
        l = list()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT date, time, description,amount
            FROM income
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date''',(from_date, to_date))
        amount = 0
        for x in cur:
            l.append(x)
        conn.commit()
        conn.close()
        return l

    def retrive_expances_for_text_box_admin(self, from_date, to_date):
        '''(self)-> list

        Connects to data.db expances table and retrives
        all data by date with description and income in list form'''
        l = list()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT date, time, description, amount
            FROM expances
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date''',(from_date, to_date))
        for x in cur:
            l.append(x)
        conn.commit()
        conn.close()
        return l

    def retrive_monthly_expances_for_text_box_admin(self, from_date, to_date):
        '''(self)-> list

        Connects to data.db expances table and retrives
        all data by date with description and income in list form'''
        l = list()
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''SELECT date, time, description, amount
            FROM monthly_expance
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date''',(from_date, to_date))
        for x in cur:
            l.append(x)
        conn.commit()
        conn.close()
        return l

class restore_pc:
    def __init__(self, location):
        self.location = location

    def create_restore(self):
        conn = sqlite3.connect(self.location, timeout=60)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS restore(
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        s INTEGER(2) NOT NULL,
        m INTEGER(2) NOT NULL,
        h INTEGER(2) NOT NULL,
        time TEXT(10) NOT NULL)''')
        conn.commit()
        conn.close()
        return None

    def restore_insert(self, s, m, h, time):
        conn = sqlite3.connect(self.location, timeout=60)
        cur = conn.cursor()
        cur.execute('''INSERT INTO restore(
        s,
        m,
        h,
        time) VALUES(
        :s,
        :m,
        :h,
        :time)''',{'s':s,'m':m ,'h':h,'time':time})
        conn.commit()
        conn.close()

        return None

    def restore_retrive(self):
        tup = None
        try:
            conn = sqlite3.connect(self.location, timeout=60)
        except:
            restore_error = messagebox.askokcancel('Restore Problem ',
                message='There was a problem connecting to '+self.location)
            return
        try:
            cur = conn.cursor()
            cur.execute('''SELECT s, m, h, time FROM restore WHERE  ID = (
                SELECT MAX(id) FROM restore)''')
            for x in cur:
                tup = x
            conn.commit()
            conn.close()
            return tup
        except:
            restore_error = messagebox.askokcancel('Restore Problem ',
                message='Could not recover data from '+self.location)
            return

    def restore_delete(self):
        if path.exists(self.location):
            try:
                remove(self.location)
            except:
                restore_error = messagebox.askokcancel('Restore Problem ',
                    message='Could not delete '+self.location)
                return
        else:
            return

class customer_debt:
    def __init__(self):
        conn = sqlite3.connect('debt.db',timeout=60)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE if not exists customer_debt(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT(20),
            phone TEXT(11),
            recv_name TEXT(20),
            description TEXT(20),
            amount INTEGER(5),
            received INTEGER(5),
            debt INTEGER(5),
            time TEXT(10),
            date TEXT(10))''')
        conn.commit()
        conn.close()

    def debt_insert(self, name, phone, recv_name, description, amount, received, debt, date, time):
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''INSERT INTO customer_debt(name, phone, recv_name, description, amount, received, debt, date, time) VALUES(
            ?,?,?,?,?,?,?,?,?)''',(name, phone, recv_name, description, amount, received, debt, date, time))
        conn.commit()
        conn.close()

    def debt_retrive_tv(self):
        l = list()
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''  SELECT id,
                                name,
                                phone,
                                recv_name,
                                description,
                                amount,
                                received,
                                debt,
                                date,
                                time from customer_debt''')
        for columns in cur:
            l.append(columns)
        conn.commit()
        conn.close()
        return l

    def search_by_name(self, text):
        l = list()
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute("""  SELECT * from customer_debt
            WHERE name like (?)""", (text,))
        
        for columns in cur:
            l.append(columns)
        conn.commit()
        conn.close()
        return l

    def search_by_phone(self, text):
        l = list()
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute("""  SELECT * from customer_debt
            WHERE phone like (?)""", (text,))
        for columns in cur:
            l.append(columns)
        conn.commit()
        conn.close()
        return l

    def search_by_description(self, text):
        l = list()
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute("""  SELECT * from customer_debt
            WHERE description like (?)""", (text,))
        for columns in cur:
            l.append(columns)
        conn.commit()
        conn.close()
        return l

    def delete_record(self, row_id):
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute("""  DELETE from customer_debt
            WHERE id = (?)""", (row_id,))
        conn.commit()
        conn.close()

    def get_name_debt_from_row(self, row_id):
        conn = sqlite3.connect('debt.db', timeout=60)
        cur = conn.cursor()
        cur.execute("""  SELECT name, debt from customer_debt
            WHERE id = (?)""", (row_id,))
        name, debt = cur.fetchone()
        conn.commit()
        conn.close()
        return (name, debt)

class cold_corner:
    def __init__(self):
        with open('final_date','r') as final:
            self.date = final.readline()
        self.today_date = str(datetime.date.today())

        conn = sqlite3.connect('cold.db',timeout=60)
        cur = conn.cursor()
        cur.executescript('''

            CREATE TABLE if not exists purchase(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20),
                qty INTEGER(5),
                totalprice INTEGER(5),
                sellprice INTEGER(5),
                time TEXT(10),
                date TEXT(10)
                );

            CREATE TABLE if not exists sell(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20),
                qty INTEGER(5),
                price INTEGER(5),
                profit INTEGER(5),
                discount INTEGER(5),
                time TEXT(10),
                date TEXT(10)
                );

            CREATE TABLE if not exists stock(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20) NOT NULL UNIQUE,
                qty INTEGER(5),
                price INTEGER(5)
                );

            CREATE TABLE if not exists invest(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20) NOT NULL UNIQUE,
                description TEXT(20),
                amount INTEGER(5)
                );

            CREATE TABLE if not exists totalinvest(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20) NOT NULL UNIQUE,
                description TEXT(20),
                amount INTEGER(5)
                );

            CREATE TABLE if not exists cashamount(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(20) NOT NULL UNIQUE,
                description TEXT(20),
                amount INTEGER(5)
                );

            ''')
        conn.commit()
        conn.close()

    def purchase_insert(self, name, qty, totalprice, sellprice):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''INSERT INTO purchase(name, qty, totalprice, sellprice, date, time) VALUES(
            ?,?,?,?,?,?)''',(name, qty, totalprice, sellprice, self.date, current_time))
        print(name, qty, totalprice, sellprice)
        conn.commit()
        conn.close()
        self.stock_insert(name, qty, sellprice)

    def product_retrive(self):
        # returns list or tuples
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT name, qty, totalprice, sellprice, time, date FROM purchase''')
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data


    def purchase_price_profit(self, name):

        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT qty, totalprice FROM  purchase
         where name==(?) ORDER BY date DESC''',(name,))
        qt_total_price = cur.fetchone()
        print(qt_total_price)
        conn.commit()
        conn.close()
        
        price = self.product_price_from_stock(name)
        qty = qt_total_price[0]
        total_price = qt_total_price[1]
        return (qty, total_price, price)

    def product_price_from_stock(self, name):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT price FROM stock
         where name==(?)''',(name,))
        price = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return price

        


    def stock_insert(self, name, qty, sellprice):
        new_purchase_name = name
        new_purchase_qty = qty
        new_purchase_sellprice = sellprice

        def select_old():
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                SELECT name, qty from stock WHERE name==(?)
                ''',(new_purchase_name,))
            old = cur.fetchone()
            print(old)
            conn.commit()
            conn.close()

            add_and_insert(old)

        def add_and_insert(old):
            if old != None:
                update_qty = int(new_purchase_qty) + int(old[1])


                conn = sqlite3.connect('cold.db', timeout=60)
                cur = conn.cursor()
                cur.execute('''
                    INSERT OR REPLACE INTO stock(name, qty, price) VALUES( ?, ?, ?)
                    ''',(name, update_qty, new_purchase_sellprice))
                conn.commit()
                conn.close()

            else:
                conn = sqlite3.connect('cold.db', timeout=60)
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO stock(name, qty, price) VALUES( ?, ?, ?)
                    ''',(new_purchase_name, new_purchase_qty, new_purchase_sellprice))
                conn.commit()
                conn.close()


        select_old()



    def sell_insert(self, name, qty, price, profit, discount):
        time = datetime.datetime.now().strftime('%I:%M %p')
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''INSERT INTO sell(name, qty, price, profit, discount, date, time) VALUES(
            ?,?,?,?,?,?,?)''',(name, qty, price, profit, discount, self.date, time))
        conn.commit()
        conn.close()


    def sell_retrive(self):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT id, name, qty, price, profit, discount, time, date FROM sell''')
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def total_sell_price_profit_retrive(self):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT price, profit FROM sell''')
        data = cur.fetchall()
        conn.commit()
        conn.close()

        total_price = 0
        total_profit = 0
        for tup in data:
            total_price += tup[0]
            total_profit += tup[1]

        print(total_price, total_profit)
        return (total_price, total_profit)


    def total_cold_sell_get(self):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT price from sell WHERE
                date=(?) ''',(self.date, ))

        list_tup_prices = cur.fetchall()
        conn.commit()
        conn.close()
        total = 0
        for price in list_tup_prices:
            total += price[0]

        return total

    def total_cold_sell_get_administrator(self, from_date, to_date):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''SELECT price
            FROM sell
            WHERE date BETWEEN (?) AND (?)''',(from_date, to_date))
        amount = 0
        for x in cur:
            amount = amount+int(x[0])
        conn.commit()
        conn.close()
        print(amount)
        return amount


    def stock_retrive(self):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            SELECT name, qty, price from stock
            ''')
        all_stock_list = cur.fetchall()
        conn.commit()
        conn.close()
        return all_stock_list

    def stock_retrive_qty_bt_name(self, name):
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            SELECT qty from stock
            WHERE name==(?)
            ''',(name, ))
        stock_qty = cur.fetchone()
        conn.commit()
        conn.close()
        return stock_qty[0]

    def stock_update_decrease(self, name, qty, price):

        def get_old_stock_qty(name):
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                SELECT qty from stock WHERE name==(?)
                ''',(name,))
            old_qty = cur.fetchone()
            conn.commit()
            conn.close()
            print(old_qty[0])
            return old_qty[0]

        def new_qty(old_qty, qty):
            return (old_qty - qty)

        def stock_update(name, new_qty, price):
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                INSERT OR REPLACE INTO stock(name, qty, price) VALUES(?, ?, ?)
                ''',(name, new_qty, price))
            conn.commit()
            conn.close()

        old_qty = get_old_stock_qty(name)
        new_qty = new_qty(old_qty, qty)
        stock_update(name, new_qty, price)


    def add_investment_database(self, description, amount):
        name = 'invest'
        def get_old_amount():
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                SELECT amount from invest WHERE
                name==(?)
                ''',(name,))
            old_qty = cur.fetchone()
            conn.commit()
            conn.close()
            if old_qty == None:
                return 0
            else:
                return old_qty[0] #1000

        def new_amount(old_amount, amount):
            return (old_amount + amount)

        def amount_update(name, description, new_amount):
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                INSERT OR REPLACE INTO invest(name, description, amount)
                VALUES(?, ?, ?)
                ''',(name, description, new_amount))
            conn.commit()
            conn.close()

        old_amount = get_old_amount()
        new_amount = new_amount(old_amount, amount)
        amount_update(name, description, new_amount)
        #self.add_investment_count(description, amount)

    def add_cashamount(self, description, amount):
        name = 'cashamount'
        def get_old_amount():
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                SELECT amount from cashamount WHERE
                name==(?)
                ''',(name,))
            old_qty = cur.fetchone()
            conn.commit()
            conn.close()
            if old_qty == None:
                return 0
            else:
                return old_qty[0] #1000

        def new_amount(old_amount, amount):
            return (old_amount + amount)

        def amount_update(name, description, new_amount):
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                INSERT OR REPLACE INTO cashamount(name, description, amount)
                VALUES(?, ?, ?)
                ''',(name, description, new_amount))
            conn.commit()
            conn.close()

        old_amount = get_old_amount()
        new_amount = new_amount(old_amount, amount)
        amount_update(name, description, new_amount)

    def subtract_cashamount(self, description, amount):
        name = 'cashamount'
        def get_old_amount():
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                SELECT amount from cashamount WHERE
                name==(?)
                ''',(name,))
            old_qty = cur.fetchone()
            conn.commit()
            conn.close()
            if old_qty == None:
                return 0
            else:
                return old_qty[0] #1000

        def new_amount(old_amount, amount):
            return (old_amount - int(amount))

        def amount_update(name, description, new_amount):
            conn = sqlite3.connect('cold.db', timeout=60)
            cur = conn.cursor()
            cur.execute('''
                INSERT OR REPLACE INTO cashamount(name, description, amount)
                VALUES(?, ?, ?)
                ''',(name, description, new_amount))
            conn.commit()
            conn.close()

        old_amount = get_old_amount()
        new_amount = new_amount(old_amount, amount)
        amount_update(name, description, new_amount)



    def invest_retrive(self):
        name='invest'
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            SELECT amount from invest WHERE
            name==(?)
            ''',(name,))
        old_qty = cur.fetchone()
        conn.commit()
        conn.close()
        if old_qty == None:
            return 0
        else:
            return old_qty[0]

    def cash_amount_retrive(self):
        name='cashamount'
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            SELECT amount from cashamount WHERE
            name==(?)
            ''',(name,))
        old_qty = cur.fetchone()
        conn.commit()
        conn.close()
        if old_qty == None:
            return 0
        else:
            return old_qty[0]

    def invest_insert(self, name, description, amount):
        name = 'invest'
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO invest(name, description, amount)
            VALUES(?,?,?)
            ''',(name, description, amount))
        conn.commit()
        conn.close()

    def change_product_name(self, newname, currentname):
        print("not")
        conn = sqlite3.connect('cold.db', timeout=60)
        cur = conn.cursor()
        cur.execute('''
            UPDATE stock SET name =(?) WHERE name=(?)
            ''',(newname, currentname))
        conn.commit()
        cur.execute('''
            UPDATE purchase SET name =(?) WHERE name=(?)
            ''',(newname, currentname))
        conn.commit()
        conn.close()
        print("done")









    # def stock_insert(self, name, qty, totalprice, date, time):
    #     conn = sqlite3.connect('cold.db', timeout=60)
    #     cur = conn.cursor()
    #     cur.execute('''INSERT INTO sell(name, qty, totalprice, date, time) VALUES(
    #         ?,?,?,?,?)''',(name, qty, totalprice, date, time))
    #     conn.commit()
    #     conn.close()

# d = customer_debt()
# t = d.search('name', '%300%')
# print(t)
