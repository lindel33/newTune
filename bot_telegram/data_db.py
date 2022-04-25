# -*- coding: utf-8 -*-
import MySQLdb

connect = MySQLdb.connect('TuneApple.mysql.pythonanywhere-services.com', 'TuneApple', 'I1QEvAR503', 'TuneApple$TuneData')
cursor = connect.cursor()


def get_category():
    sql = "SELECT * FROM tune_admin_category"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_products(category_name):

    sql = f"SELECT tune_admin_seriescategory.id, tune_admin_product.name" \
          f" FROM tune_admin_seriescategory, tune_admin_product" \
          f" WHERE tune_admin_seriescategory.category = '{category_name}'" \
          f" AND tune_admin_product.series_id = tune_admin_seriescategory.id" \
          f" AND sell != 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_products_a(category_name):

    sql = f"SELECT tune_admin_seriescategory.id, tune_admin_product.name" \
          f" FROM tune_admin_seriescategory, tune_admin_product" \
          f" WHERE tune_admin_seriescategory.category LIKE '%{category_name}%'" \
          f" AND tune_admin_product.series_id = tune_admin_seriescategory.id" \
          f" AND sell != 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
# pprint(get_products_a('iPhone 8'))
def get_current_product():
    sql = f"SELECT tune_admin_product.series_id, tune_admin_seriescategory.category " \
          f" FROM tune_admin_product, tune_admin_seriescategory " \
          f"WHERE tune_admin_product.series_id = tune_admin_seriescategory.id AND sell != 1;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_series(name_series):
    sql = f"SELECT category FROM tune_admin_seriescategory WHERE category LIKE '%{name_series}%';"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_detail_product(name_product):

    sql = f"SELECT * FROM tune_admin_product WHERE name = '{name_product}'"
    cursor.execute(sql)

    return cursor.fetchall()[0]
# pprint(get_detail_product('iPhone 7 Plus 128 Space gray - 15.990'))

def get_models(name_model):
    sql = f"SELECT * FROM tune_admin_product WHERE name = '{name_model}'"
    cursor.execute(sql)

    return cursor.fetchall()[0]

def get_not_category():
    sql = f"SELECT name FROM tune_admin_product WHERE category_id = 12"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = [x[0].split()[0] for x in result]
    return result


def filter_price(price_min, price_max):
    sql = f"SELECT name FROM tune_admin_product" \
          f" WHERE price >= '{price_min}' AND price <= '{price_max}'"
    cursor.execute(sql)

    return cursor.fetchall()


def get_actual_price(name_type):
    sql = f"SELECT * FROM tune_admin_actualprice WHERE type = '{name_type}'"
    cursor.execute(sql)

    return cursor.fetchall()


def get_all_products():
    sql = f"SELECT name FROM tune_admin_product WHERE sell != 1"
    cursor.execute(sql)

    return cursor.fetchall()


# text = '⬅️  Назад к б\у iPhone 7 / 7+'
# # xxx = text.split()
# # xxx.remove('⬅️Назад')
# # xxx.remove('к')
# # print(" ".join(xxx))
# print(" ".join(text.split()[1:5]))