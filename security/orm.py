from security import db,api_prog
from security.models import User, Portfolio_main, Portfolio_second
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,update,column, Integer, String, Table, select, delete
import sqlite3
from flask_login import login_user, current_user


def get_tuples(username1):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM Portfolio_second WHERE username = '{}';""".format(username1))

    positions_query = cursor.fetchall()
    if (positions_query) == None:
        return False
    else:
        final_query_list = []
        for tups in positions_query:
            l = []
            for items in tups:
                l.append(items)
            final_query_list.append(l)
        return final_query_list



def update_port_sec(username,symbol,name,quantity,price):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()
    sec_type='Share'

    # get primary key from users first
    cursor.execute("""SELECT quantity,pur_price FROM Portfolio_second WHERE username = '{}' AND sec_symbol= '{}';""".format(username, symbol))
    fetch = cursor.fetchall()


    # if VWAP doesn't exist in positions list then add to positions
    if len(fetch) == 0:
        # check if initial commit of symbol to position - if so we can add to position'
        cursor.execute("""
                INSERT INTO Portfolio_second(username,sec_symbol,sec_name, sec_type, quantity, pur_price)
                VALUES('{}','{}','{}','{}','{}','{}')
                ;""".format(username, str(symbol),str(name),str(sec_type), quantity, float(price)))
        connection.commit()
    else:
    	admin = Portfolio_second.query.filter_by(username=username , sec_symbol=symbol).first()   	
    	admin.quantity = int(admin.quantity) + int(quantity)
    	admin.pur_price = price
    	db.session.commit()



def update_port_main(username, net):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()
    admin = Portfolio_main.query.filter_by(username=username).first()
    admin.buy_pow-=net
    db.session.commit() 

def validate_quantity(username, symbol, quantity_required):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT quantity FROM Portfolio_second WHERE username = '{}' AND sec_symbol= '{}';""".format(username, symbol))
    fetch_quantity = cursor.fetchone()
    if fetch_quantity == None or int(fetch_quantity[0])<int(quantity_required):
        return False


def update_port_sec_on_sell(username,symbol,quantity_required,price):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""SELECT quantity,pur_price FROM Portfolio_second WHERE username = '{}' AND sec_symbol= '{}';""".format(username, symbol))
    fetch = cursor.fetchone()
    admin1 = Portfolio_main.query.filter_by(username=username).first()
    admin1.acc_value+=(float(price-fetch[1])*float(quantity_required))

    if int(fetch[0])==int(quantity_required):
        update_port_main(username, float(-(int(quantity_required)*float(price))))
        Portfolio_second.query.filter_by(username=username, sec_symbol=symbol).delete()
        db.session.commit()
    else:
        admin = Portfolio_second.query.filter_by(username=username , sec_symbol=symbol).first()     
        admin.quantity -=int(quantity_required)
        update_port_main(username, float(-(int(quantity_required)*float(price))))
        db.session.commit()


# def find_acc_val(username):
#     connection = sqlite3.connect('/home/niskarsh321/Desktop/dbms_env/market/security/proj_database.db')
#     cursor = connection.cursor()
#     cursor.execute("""SELECT sec_symbol,quantity FROM Portfolio_second WHERE username = '{}';""".format(username))

#     positions_query = cursor.fetchall()
#     acc_v=0.0
#     temp=0.0
#     if (positions_query) == None:
#         return 200000
#     else:
#         for tups in positions_query:
#             name, price = api_prog.get_stock_price(tups[0])
#             temp+=(price*tups[1])
#     temp+=current_user.portfolio_main.buy_pow
#     acc_v = "%.2f" % temp
#     return acc_v

def find_acc_val(username):
    connection = sqlite3.connect('/home/ravi/Desktop/project/market/security/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT sec_symbol,quantity,pur_price FROM Portfolio_second WHERE username = '{}';""".format(username))

    positions_query = cursor.fetchall()
    acc_v=0.0
    temp=0.0
    if (positions_query) == None:
        return 200000
    else:
        for tups in positions_query:
            name, cur_price = api_prog.get_stock_price(tups[0].upper())
            temp += (cur_price-tups[2])*tups[1] ;
    temp+=current_user.portfolio_main.acc_value
    acc_v = "%.2f" % temp
    return acc_v