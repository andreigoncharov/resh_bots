import asyncio
import author_bot
import bot
from datetime import datetime, timedelta

from db_manager import UsersDbManager

loop = asyncio.get_event_loop()

async def func():
    all_orders = await UsersDbManager.get_all_order_for_time(loop)

    '''
    ["[1,2,3]", "[4,5,6]"]
    '''

    for order in all_orders:
        order = order.replace('"', '')
        order = order.replace('[', '')
        order = order.replace(']', '')
        order = order.split(',')
        ord_id = order[0]
        date = order[1]
        time = order[2]
        tel_id = order[3]
        curr_time = datetime.now() - timedelta(minutes=10)
        curr_time = curr_time.time()
        curr_time = curr_time.strftime('%H:%M')
        curr = datetime.strptime(time, '%H:%M').time()
        curr_time = datetime.strptime(curr_time, '%H:%M').time()
        if curr == curr_time:
            auth_id = await UsersDbManager.get_ord_auth(ord_id, loop)
            await author_bot.send_time(auth_id, ord_id)
        curr_time = datetime.now() - timedelta(minutes=20)
        curr_time = curr_time.time()
        curr_time = curr_time.strftime('%H:%M')
        curr_time = datetime.strptime(curr_time, '%H:%M').time()
        if curr == curr_time:
            await bot.send_time(tel_id)
    return


while(True):
    await func()
