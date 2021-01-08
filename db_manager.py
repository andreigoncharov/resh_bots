import re
import string

import aiomysql
from pymysql import connect
from config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
import asyncio
import datetime
import random

'''
SET SQL_SAFE_UPDATES = 0;
для того, чтоб удалять можно было
'''


async def create_con(loop):
    con = await aiomysql.connect(host=DB_HOST, user=DB_USER, db=DB_NAME, password=DB_PASSWORD, loop=loop)
    cur = await con.cursor()
    return con, cur


def create_sync_con():
    con = connect(host=DB_HOST, user=DB_USER, db=DB_NAME,
                  password=DB_PASSWORD)
    cur = con.cursor()
    return con, cur


class UsersDbManager:
    @staticmethod
    def clear():
        con, cur = create_sync_con()
        cur.execute('delete from users')
        con.commit()
        con.close()

    @staticmethod
    async def user_exist(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from users where tel_id = %s', tel_id)
        r = await cur.fetchone()
        count = r[0]
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    async def add_user(tel_id, name, phone_number, username, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into reshalaa_bot.user values(%s, %s, %s, %s, %s, %s, %s)',
                          (tel_id, name, phone_number, '', '', username, ''))
        await con.commit()
        await cur.execute('insert into reshalaa_bot.bonuses values(%s, %s)',
                          (tel_id, 0))
        await con.commit()

        con.close()

    @staticmethod
    async def get_user(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from user where tel_id = %s', (tel_id))
        user = await cur.fetchone()
        con.close()

        if user is None:
            return None

        return user

    @staticmethod
    async def update_context(tel_id, context, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.user set context = %s where tel_id = %s', (context, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_vuz(tel_id, vuz, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.user set name_vuz = %s where tel_id = %s', (vuz, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_type(tel_id, type, loop):
        con, cur = await create_con(loop)
        await cur.execute('select username from user where tel_id = %s', (tel_id))
        username = await cur.fetchone()
        await cur.execute(
            'insert into reshalaa_bot.db_manager_order values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (None, tel_id, type, '', '', '', '', '', '', '', '', '', username[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_prof(tel_id, prof, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.db_manager_order set prof = %s where tel_id = %s', (prof, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_predm(tel_id, predm, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.db_manager_order set predm = %s where tel_id = %s', (predm, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_info(tel_id, info, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set info = %s where ord_id = %s', (info, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_oforml(tel_id, oforml, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set oforml = %s where ord_id = %s', (oforml, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_date(tel_id, date, loop):
        con, cur = await create_con(loop)
        date = date.replace('_', '')
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set date = %s where ord_id = %s', (date, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_time(tel_id, time, loop):
        con, cur = await create_con(loop)
        time = time.replace('_', '')
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set time = %s where ord_id = %s', (time, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_end_contr(tel_id, time, loop):
        con, cur = await create_con(loop)
        time = time.replace('_', '')
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set end_contr = %s where ord_id = %s',
                          (time, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def update_price(tel_id, price, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_order set price = %s where ord_id = %s', (price, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def delete_all(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('delete from reshalaa_bot.db_manager_order where ord_id=%s', (ord_id[0]))
        await con.commit()
        try:
            await cur.execute('delete from reshalaa_bot.files where ord_id=%s', (ord_id[0]))
            await con.commit()
        except:
            sd = None
        con.close()

    @staticmethod
    async def get_order(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        await cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(context[0]))
        order = await cur.fetchone()
        con.close()
        return order

    @staticmethod
    async def get_type(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('select type from reshalaa_bot.db_manager_order where ord_id={0}'.format(ord_id[0]))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_context(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select context from reshalaa_bot.user where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    def sync_get_context(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from user where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    async def insert_ph_img_1(ord_id, photo, name, loop):
        con, cur = await create_con(loop)
        await cur.execute('Insert into reshalaa_bot.files values(%s, %s, %s)', (ord_id, photo, name))
        await con.commit()
        await cur.close()
        con.close()

    @staticmethod
    async def update_links(ord_id, photo, tel_id, loop):
        con, cur = await create_con(loop)
        link = ' , ' + photo
        try:
            await cur.execute('update reshalaa_bot.db_manager_order set links = CONCAT(links, %s) where ord_id = %s',
                              (link, ord_id))
            await con.commit()

            return True

        except aiomysql.connection.Error as error:
            return False

        finally:
            await cur.close()
            con.close()

    @staticmethod
    async def get_ord_id(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_docs(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from reshalaa_bot.files where ord_id = {0}'.format(ord_id))
        context = await cur.fetchall()
        con.close()
        if len(context) < 1:
            return False
        return context

    @staticmethod
    async def get_o_orders(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from reshalaa_bot.db_manager_doneo where tel_id = {0}'.format(tel_id))
        context = await cur.fetchall()
        con.close()
        if len(context) < 1:
            return False
        return context

    @staticmethod
    async def get_act_orders(tel_id, loop):
        con, cur = await create_con(loop)
        all = []

        await cur.execute('select * from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        context = await cur.fetchall()
        all.append(context)

        await cur.execute('select * from reshalaa_bot.db_manager_priceo where tel_id = {0}'.format(tel_id))
        context = await cur.fetchall()
        all.append(context)

        await cur.execute('select * from reshalaa_bot.db_manager_activeo where tel_id = {0}'.format(tel_id))
        context = await cur.fetchall()
        all.append(context)

        await cur.execute('select * from reshalaa_bot.db_manager_waito where tel_id = {0}'.format(tel_id))
        context = await cur.fetchall()
        all.append(context)

        con.close()

        ret_all = []

        for el in all:
            if len(el) is not 0:
                ret_all.append(el[0])

        if len(ret_all) < 1:
            return False
        return ret_all

    @staticmethod
    def sync_get_type(tel_id):
        con, cur = create_sync_con()
        cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        cur.execute(
            'select type from reshalaa_bot.db_manager_order where ord_id={0}'.format(context[0]))
        context = cur.fetchone()

        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    def get_time_t(tel_id):
        con, cur = create_sync_con()
        cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = cur.fetchone()
        cur.execute('select end_contr from reshalaa_bot.db_manager_order where ord_id={0}'.format(ord_id[0]))
        context = cur.fetchone()
        con.close()
        if len(context[0]) == 0:
            return False

        return context[0]

    @staticmethod
    def get_time(tel_id):
        con, cur = create_sync_con()
        cur.execute('select max(ord_id) from reshalaa_bot.db_manager_order where tel_id = {0}'.format(tel_id))
        ord_id = cur.fetchone()
        cur.execute('select time from reshalaa_bot.db_manager_order where ord_id={0}'.format(ord_id[0]))
        context = cur.fetchone()
        con.close()
        if len(context[0]) == 0:
            return None
        return context[0]

    '''
    AUTHORS
    '''

    @staticmethod
    async def add_author(tel_id, phone_number, username, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into reshalaa_bot.authors values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                          (str(tel_id), str(phone_number), '', '', '', None, '', '', '', str(username), '0', '', '0'))
        await con.commit()
        con.close()

    @staticmethod
    async def update_context_a(tel_id, context, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.authors set context = %s where tel_id = %s', (context, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_context_a(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select context from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    def sync_get_context_a(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from authors where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    async def update_vuz_a(tel_id, vuz, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.authors set vuz = %s where tel_id = %s', (vuz, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_step_a(tel_id, vuz, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.authors set step = %s where tel_id = %s', (vuz, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def insert_ph_img_a(tel_id, photo, loop):
        con, cur = await create_con(loop)
        try:
            await cur.execute('update reshalaa_bot.authors set vuz_ph = %s where tel_id = %s', (photo, tel_id))
            await con.commit()
            return True

        except aiomysql.connection.Error as error:
            return False

        finally:
            await cur.close()
            con.close()

    @staticmethod
    async def update_card_a(tel_id, vuz, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.authors set card_num = %s where tel_id = %s', (vuz, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_prof_a(tel_id, prof, loop):
        con, cur = await create_con(loop)
        prof = '.' + prof
        await cur.execute('update reshalaa_bot.authors set prof = CONCAT(prof, %s) where tel_id = %s', (prof, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_predm_a(tel_id, predm, loop):
        con, cur = await create_con(loop)
        predm = ',' + predm
        await cur.execute('update reshalaa_bot.authors set predm = CONCAT(predm, %s) where tel_id = %s',
                          (predm, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_orders(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select predm from reshalaa_bot.authors where tel_id = %s', (tel_id))
        predm = await cur.fetchone()

        tab = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

        text = predm[0]

        res = text.translate(tab).split()

        await cur.execute('select * from reshalaa_bot.db_manager_order')
        predm1 = await cur.fetchall()

        ord_ = []
        for pr in predm1:
            if pr[4] in res:
                ord_.append(pr)

        con.close()

        if ord_ == []:
            return None
        return ord_

    @staticmethod
    async def add_pre_order_author(ord_id, tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select reshalaa_bot.authors.username from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        username = await cur.fetchone()
        await cur.execute('insert into reshalaa_bot.db_manager_ord_auth_price values(%s, %s, %s, %s, %s, %s)',
                          (ord_id, tel_id, '', '', username, None))
        await con.commit()

        await cur.execute('update reshalaa_bot.authors set num = %s where tel_id=%s',
                          (ord_id, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_ord_price(tel_id, price, loop):
        con, cur = await create_con(loop)
        await cur.execute('select num from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()

        await cur.execute('update reshalaa_bot.db_manager_ord_auth_price set price = %s where ord_id=%s',
                          (price, ord_id[0]))
        await con.commit()

        con.close()

    @staticmethod
    async def update_ord_com(tel_id, com, loop):
        con, cur = await create_con(loop)
        await cur.execute('select num from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute('update reshalaa_bot.db_manager_ord_auth_price set com = %s where ord_id=%s',
                          (com, ord_id[0]))
        await con.commit()
        con.close()

    @staticmethod
    async def get_user_vuz(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select name_vuz from reshalaa_bot.user where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_order_a(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
        context = await cur.fetchone()
        context = context[0]
        await cur.execute('select name_vuz from reshalaa_bot.user where tel_id = {0}'.format(context[1]))
        vuz = await cur.fetchone()
        con.close()
        return context, vuz

    @staticmethod
    async def get_a_price(ord_id, tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select price from reshalaa_bot.db_manager_ord_auth_price where tel_id = %s and ord_id = %s',
                          (tel_id, ord_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_all_order_for_time(loop):
        con, cur = await create_con(loop)
        curr_date = datetime.date.today()
        await cur.execute(
            f'select * from reshalaa_bot.db_manager_order where type = "Online решение" and date = {curr_date}')
        orders = await cur.fetchall()

        full = []
        small = []
        for order in orders:
            small.append(order[0])

            date = order[7]
            small.append(date)

            start_time = order[8]
            small.append(start_time)

            tel_id = order[1]
            small.append(tel_id)

            full.append(str(small))
            small.clear()

        con.close()
        return full

    @staticmethod
    async def get_ord_auth(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select tel_id from reshalaa_bot.order_author where ord_id = %s',
                          ord_id)
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_ord_auth_2(tel_id, loop):
        con, cur = await create_con(loop)
        date = datetime.date.today()
        await cur.execute(
            'select ord_id from reshalaa_bot.db_manager_order where ord_id = %s and type = "Online решение" and '
            'date = %s',
            (tel_id, date))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_cust_id(tel_id, loop):
        con, cur = await create_con(loop)
        date = datetime.date.today()

        await cur.execute('select ord_id from reshalaa_bot.order_author where tel_id = %s',
                          tel_id)
        ord_id = await cur.fetchone()

        await cur.execute(
            'select tel_id from reshalaa_bot.db_manager_order where ord_id = %s and type = "Online решение" and '
            'date = %s',
            (ord_id, date))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def delete_order(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('delete from reshalaa_bot.db_manager_order where ord_id = %s',
                          (ord_id))
        await con.commit()

        await cur.execute('delete from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s',
                          (ord_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_all_orders(loop):
        con, cur = await create_con(loop)

        await cur.execute('select * from reshalaa_bot.db_manager_order')
        orders = await cur.fetchall()

        con.close()
        return orders

    @staticmethod
    async def get_username(tel_id, loop):
        con, cur = await create_con(loop)

        await cur.execute('select username from reshalaa_bot.user where tel_id = %s', tel_id)
        orders = await cur.fetchone()

        con.close()
        return orders[0]

    @staticmethod
    async def get_username_a(tel_id, loop):
        con, cur = await create_con(loop)

        await cur.execute('select username from reshalaa_bot.authors where tel_id = %s', tel_id)
        orders = await cur.fetchone()

        con.close()
        return orders[0]

    @staticmethod
    async def get_vuz(tel_id, loop):
        con, cur = await create_con(loop)

        await cur.execute('select name_vuz from reshalaa_bot.user where tel_id = %s', tel_id)
        orders = await cur.fetchone()

        con.close()
        return orders[0]

    @staticmethod
    async def get_order_author_pre(ord_id, loop):
        con, cur = await create_con(loop)

        await cur.execute('select * from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s', ord_id)
        orders = await cur.fetchone()

        con.close()
        return orders[0]

    @staticmethod
    def sync_get_context_a(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from authors where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    async def get_new_order(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
        order = await cur.fetchone()
        con.close()
        return order

    @staticmethod
    async def get_authors(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select predm from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
        predm = await cur.fetchone()
        predm = '%' + predm[0] + '%'
        c = 'wait_confirm'
        await cur.execute(f'SELECT tel_id FROM reshalaa_bot.authors where predm like "{predm}" and context != "{c}"')
        authors = await cur.fetchall()
        if predm == 'Другое':
            await cur.execute(f'SELECT tel_id FROM reshalaa_bot.authors')
            authors = await cur.fetchall()
        con.close()
        return authors

    @staticmethod
    async def get_cost_1(ord_id, loop):
        ord_id = ord_id[1:]
        con, cur = await create_con(loop)
        await cur.execute('select customer_pr from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost[0]

    @staticmethod
    async def update_and_get_cost(tel_id, ord_id, loop):
        ord_id = ord_id[1:]
        con, cur = await create_con(loop)

        await cur.execute('select count_b from reshalaa_bot.bonuses where tel_id = {0}'.format(tel_id))
        bonuses = await cur.fetchone()

        await cur.execute('select customer_pr from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()

        await cur.execute('update reshalaa_bot.db_manager_cust_pri set customer_pr = %s where ord_id=%s',
                          (int(cost[0]) - int(bonuses[0]), tel_id))
        await con.commit()

        await cur.execute('select customer_pr from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        new_cost = await cur.fetchone()

        await cur.execute('update reshalaa_bot.bonuses set count_b = count_b - %s  where ord_id=%s',
                          (int(bonuses[0]), tel_id))
        await con.commit()

        con.close()
        return new_cost[0]

    @staticmethod
    async def get_cost(ord_id, loop):
        ord_id = ord_id[1:]
        con, cur = await create_con(loop)
        await cur.execute('select customer_pr from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost[0]

    @staticmethod
    async def get_costt(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select customer_pr from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost[0]

    @staticmethod
    async def get_costtwo(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select payment from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost[0]

    @staticmethod
    async def add_num(tel_id, num, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.user set num = %s where tel_id=%s',
                          (num, tel_id))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_num(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select num from reshalaa_bot.user where tel_id = {0}'.format(tel_id))
        cost = await cur.fetchone()
        con.close()
        return cost[0]

    @staticmethod
    async def update_payment(ord_id, payment, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.db_manager_priceo set payment = %s where ord_id=%s',
                          (ord_id, payment))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_priceo_order(ord_id, loop):
        con, cur = await create_con(loop)
        ord_id = ord_id[1:]
        await cur.execute(
            'select * from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost

    @staticmethod
    async def get_customer(ord_id, loop):
        con, cur = await create_con(loop)
        ord_id = ord_id[1:]
        await cur.execute(
            'select tel_id from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        tel_id = await cur.fetchone()
        await cur.execute(
            'select tel_id from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        auth_id = await cur.fetchone()
        con.close()
        return tel_id[0], auth_id[0]

    @staticmethod
    async def get_customertwo(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select tel_id from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        tel_id = await cur.fetchone()
        con.close()
        return tel_id[0]

    @staticmethod
    async def active_o(ord_id, payment, loop):
        con, cur = await create_con(loop)
        ord_id = str(ord_id)
        ord_id = ord_id.replace('_', '')

        await cur.execute(
            'select * from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        info = await cur.fetchone()

        await cur.execute(
            'select auth_username from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        author = await cur.fetchone()

        await cur.execute('insert into reshalaa_bot.db_manager_activeo values (%s, %s, %s, %s, %s, %s, %s,'
                          '%s, %s, %s, %s, %s, %s, %s, %s)',
                          (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
                           info[9], info[10], info[11], info[12], payment, author))
        await con.commit()

        await cur.execute(
            'select * from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        pr_info = await cur.fetchone()

        await cur.execute('insert into reshalaa_bot.db_manager_customer_price values (%s, %s, %s, %s, %s, %s, %s)',
                          (pr_info[0], pr_info[1], pr_info[2], pr_info[3], pr_info[4], pr_info[5], pr_info[6]))
        await con.commit()

        await cur.execute('delete from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        await con.commit()
        await cur.execute('delete from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
        await con.commit()
        await cur.execute('delete from reshalaa_bot.db_manager_ord_auth_price where ord_id = {0}'.format(ord_id))
        await con.commit()
        await cur.execute('delete from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        await con.commit()

        con.close()
        return

    @staticmethod
    async def waito(ord_id, loop):
        con, cur = await create_con(loop)
        ord_id = ord_id[0:]

        await cur.execute(
            'select * from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
        info = await cur.fetchone()

        await cur.execute('insert into reshalaa_bot.db_manager_waito values (%s, %s, %s, %s, %s, %s, %s,'
                          '%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                          (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
                           info[9], info[10], info[11], info[12], info[13], info[14], ''))
        await con.commit()

        await cur.execute('delete from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def insert_author_links(ord_id, link, loop):
        con, cur = await create_con(loop)
        link = ' , ' + link
        await cur.execute(
            'update reshalaa_bot.db_manager_waito set author_links = CONCAT(author_links, %s) where ord_id=%s',
            (link, ord_id))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_links(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select author_links from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        tel_id = await cur.fetchone()
        con.close()
        return tel_id[0]

    @staticmethod
    async def doneo(ord_id, otz, loop):
        con, cur = await create_con(loop)

        await cur.execute(
            'select * from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        info = await cur.fetchone()

        await cur.execute(
            'select customer_pr from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        price = await cur.fetchone()



        await cur.execute('insert into reshalaa_bot.db_manager_doneo values (%s, %s, %s, %s, %s, %s, %s,'
                          '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                          (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
                           info[9], price, info[11], info[12], info[13], info[14], info[15], otz, ''))
        await con.commit()

        await cur.execute('delete from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
        await con.commit()
        await cur.execute('delete from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def update_com(ord_id, payment, loop):
        con, cur = await create_con(loop)

        await cur.execute('update reshalaa_bot.db_manager_doneo set com = %s where ord_id=%s',
                          (payment, ord_id[1:]))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_active_order(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
        order = await cur.fetchone()
        con.close()
        return order

    @staticmethod
    async def get_author_price(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select price from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        order = await cur.fetchone()
        con.close()
        return order[0]

    @staticmethod
    async def add_num_a(tel_id, num, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update reshalaa_bot.authors set num = {str(num)} where tel_id={tel_id}')
        await con.commit()
        con.close()
        return

    @staticmethod
    async def update_bonuses(tel_id, bonuses, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update reshalaa_bot.bonuses set count_b = count_b + {int(bonuses)} where tel_id = {tel_id}')
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_bonuses(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count_b from reshalaa_bot.bonuses where tel_id=%s',
                          (tel_id))
        num = await cur.fetchone()
        con.close()
        return num[0]

    @staticmethod
    async def get_num_a(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select num from reshalaa_bot.authors where tel_id=%s',
                          (tel_id))
        num = await cur.fetchone()
        con.close()
        return num[0]

    @staticmethod
    async def get_wait_order(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select * from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        cost = await cur.fetchone()
        con.close()
        return cost

    @staticmethod
    async def otmo(ord_id, otz, loop):
        con, cur = await create_con(loop)

        await cur.execute(
            'select * from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        info = await cur.fetchone()

        await cur.execute(
            'select customer_pr from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        price = await cur.fetchone()

        await cur.execute('insert into reshalaa_bot.db_manager_canceledo values (%s, %s, %s, %s, %s, %s, %s,'
                          '%s, %s, %s, %s, %s, %s, %s, %s)',
                          (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
                           price, info[10], info[11], info[12], info[13], otz))
        await con.commit()

        await cur.execute('delete from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        await con.commit()
        await cur.execute('delete from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        await con.commit()
        con.close()
        return

    @staticmethod
    async def get_author(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select * from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        author = await cur.fetchone()
        con.close()
        return author

    @staticmethod
    async def get_rate(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select username from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        username = await cur.fetchone()
        await cur.execute(
            f'select AVG(otz) from reshalaa_bot.db_manager_doneo where author = "{username[0]}"')
        otz = await cur.fetchone()
        con.close()
        return otz

    @staticmethod
    async def delete_author(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'delete from reshalaa_bot.authors where tel_id = {tel_id}')
        await con.commit()
        con.close()
        return

    @staticmethod
    async def otm_order(ord_id, loop):
        ord_id = re.sub("\D", "", ord_id)
        con, cur = await create_con(loop)
        dthc = ''

        all = []

        await cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
        context = await cur.fetchall()
        all.append(context)
        if len(all) is not 0:
            dthc = 'db_manager_order'

        await cur.execute('select * from reshalaa_bot.db_manager_priceo where ord_id = {0}'.format(ord_id))
        context = await cur.fetchall()
        all.append(context)
        if len(all) is not 0:
            dthc = 'db_manager_priceo'

        await cur.execute('select * from reshalaa_bot.db_manager_activeo where ord_id = {0}'.format(ord_id))
        context = await cur.fetchall()
        all.append(context)
        if len(all) is not 0:
            dthc = 'db_manager_activeo'

        await cur.execute('select * from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        context = await cur.fetchall()
        all.append(context)
        if len(all) is not 0:
            dthc = 'db_manager_waito'

        ret_all = []
        for el in all:
            if len(el) is not 0:
                ret_all.append(el[0])

        pr_info = ret_all[0]

        await cur.execute('insert into reshalaa_bot.db_manager_canceledo values (%s, %s, %s, %s, %s, %s, %s, %s, %s, '
                          '%s, %s, %s, %s, %s, %s)',
                          (pr_info[0], pr_info[1], pr_info[2], pr_info[3], pr_info[4], pr_info[5], pr_info[6],
                           pr_info[7], pr_info[8], pr_info[9], pr_info[10], pr_info[11], pr_info[12], '',
                           ''))
        await con.commit()

        await cur.execute(f'delete from reshalaa_bot.{dthc} where ord_id = {ord_id}')
        await con.commit()

        con.close()
        return

    @staticmethod
    async def get_balance(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select balance from reshalaa_bot.authors where tel_id = {0}'.format(tel_id))
        bal = await cur.fetchone()
        con.close()
        return bal

    @staticmethod
    async def get_count(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select countt from reshalaa_bot.count_files where tel_id = {0}'.format(tel_id))
        bal = await cur.fetchone()
        con.close()
        return bal[0]

    @staticmethod
    async def author_exist(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from user where tel_id = %s', tel_id)
        r = await cur.fetchone()
        count = r[0]
        if count > 0:
            con.close()
            return True
        else:
            await cur.execute(
                'insert into reshalaa_bot.owner values (%s, %s, %s, %s)',
                (tel_id, '', '', ''))
            await con.commit()
            con.close()
            return

    @staticmethod
    async def update_context_owner(tel_id, context, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.owner set context = %s where tel_id = %s', (context, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    def sync_get_context_owner(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from owner where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()
        if context is None:
            return None

        return context[0]

    @staticmethod
    async def update_num_owner(tel_id, ord_id, m_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update reshalaa_bot.owner set ord_id = %s where tel_id = %s', (ord_id, tel_id))
        await con.commit()
        await cur.execute('update reshalaa_bot.owner set m_id = %s where tel_id = %s', (m_id, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_num_owner(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select ord_id from reshalaa_bot.owner where tel_id = {0}'.format(tel_id))
        ord_id = await cur.fetchone()
        await cur.execute(
            'select m_id from reshalaa_bot.owner where tel_id = {0}'.format(tel_id))
        m_id = await cur.fetchone()
        con.close()
        return ord_id[0], m_id[0]

    @staticmethod
    async def get_price(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select customer_pr from reshalaa_bot.db_manager_cust_pri where ord_id = {0}'.format(ord_id))
        ord_id = await cur.fetchone()
        con.close()
        return ord_id[0]

    @staticmethod
    async def get_pricetwo(ord_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select customer_pr from reshalaa_bot.db_manager_customer_price where ord_id = {0}'.format(ord_id))
        ord_id = await cur.fetchone()
        await cur.execute(
            'select payment from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        payment = await cur.fetchone()
        con.close()
        return ord_id[0], payment[0]

    @staticmethod
    async def update_payment_two(ord_id, pmt, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select payment from reshalaa_bot.db_manager_waito where ord_id = {0}'.format(ord_id))
        payment = await cur.fetchone()
        dopl = int(payment[0]) + int(pmt)
        await cur.execute(f'update reshalaa_bot.db_manager_waito set payment = {dopl} where ord_id = {pmt}')
        await con.commit()
        con.close()
        return

    @staticmethod
    async def insert_pays(ord_id, loop):
        con, cur = await create_con(loop)

        await cur.execute('insert into reshalaa_bot.db_manager_pays values (%s, %s, %s)',
                          (ord_id, 0, ''))
        await con.commit()
        con.close()
        return