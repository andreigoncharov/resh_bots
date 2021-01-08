'''
from pymysql import connect

from config import *


def create_sync_con():
    con = connect(host=DB_HOST, user=DB_USER, db=DB_NAME,
                  password=DB_PASSWORD)
    cur = con.cursor()
    return con, cur


def otm_order(ord_id):
    con, cur = create_sync_con()

    all = []

    cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
    context =  cur.fetchall()
    all.append(context)

    cur.execute('select * from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
    context =  cur.fetchall()
    all.append(context)

    cur.execute('select * from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
    context = cur.fetchall()
    all.append(context)

    cur.execute('select * from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
    context = cur.fetchall()
    all.append(context)

    con.close()

    ret_all = []

    for el in all:
        if len(el) is not 0:
            ret_all.append(el[0])

    return ret_all


o = otm_order(61)
'''
a = '_2'
print(a[1:])