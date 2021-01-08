import asyncio
import re

from aiogram import Bot, Dispatcher, executor, types
import bot as cb
import author_bot as ab
import markup as mk1
from config import ConfirmationOfOrders_bot, Owner_id
from db_manager import UsersDbManager

bot = Bot(ConfirmationOfOrders_bot)
dp = Dispatcher(bot)

loop = asyncio.get_event_loop()

TOKEN = ConfirmationOfOrders_bot

owner_id = Owner_id


@dp.message_handler(commands=['start'])
async def start(message):
    tel_id = owner_id

    text = 'Бот готов к использованию. Как только будут заказы - вы их сразу получите!'
    await bot.send_message(tel_id, text)
    await UsersDbManager.author_exist(tel_id, loop)


async def send_ph(order_id, photo):
    cost = await UsersDbManager.get_cost_1(order_id, loop)
    full_cost = int(cost)
    order_id = order_id[1:]
    fifty = round(full_cost * (50 / 100))
    text = f'Заказ №{order_id}\n\n' \
           f'Стоимость: {full_cost}\n' \
           f'50%: {fifty}'
    await bot.send_photo(chat_id=owner_id, photo=photo, caption=text, reply_markup=mk1.fifty_or_all(order_id))


async def send_phtwo(order_id, photo):
    cost = await UsersDbManager.get_cost(order_id, loop)
    full_cost = int(cost)
    order_id = order_id[1:]
    payment = await UsersDbManager.get_costtwo(order_id, loop)
    ost = full_cost - int(payment)
    text = f'<b>Заказ №{order_id}</b><i>(Доплата)</i>\n\n' \
           f'Стоимость: {full_cost}\n' \
           f'Оплачено: {payment}\n' \
           f'Нужно доплатить: {ost}'
    await bot.send_photo(chat_id=owner_id, photo=photo, caption=text, reply_markup=mk1.all(order_id), parse_mode='html')


async def send_ph_full(order_id, photo):
    cost = await UsersDbManager.get_cost(order_id, loop)
    full_cost = int(cost[0])
    text = f'Заказ №{order_id}\n\n' \
           f'Стоимость: {full_cost}\n'
    await bot.send_photo(chat_id=owner_id, photo=photo, caption=text, reply_markup=mk1.all(order_id))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('fifty_'))
async def pp(callback_query: types.CallbackQuery):
    tel_id = callback_query.from_user.id
    ord_id = callback_query.data[5:]
    await bot.answer_callback_query(
        callback_query.id,
        text='50% оплата подтверждена!', show_alert=True)
    pm = await UsersDbManager.get_cost(ord_id, loop)
    c_id, auth_id = await UsersDbManager.get_customer(ord_id, loop)
    p = round(int(pm) * (50 / 100))
    await UsersDbManager.update_payment(ord_id, p, loop)
    await cb.confirm_fifty(c_id, ord_id, p)
    await ab.confirm_order(auth_id, ord_id[1:])
    await UsersDbManager.active_o(ord_id, p, loop)
    try:
        await bot.delete_message(tel_id, callback_query.message.message_id)
    except:
        a = None


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('all_'))
async def pp(callback_query: types.CallbackQuery):
    tel_id = callback_query.from_user.id
    ord_id = callback_query.data[3:]
    await bot.answer_callback_query(
        callback_query.id,
        text='100% оплата подтверждена!', show_alert=True)
    pm = await UsersDbManager.get_cost(ord_id, loop)
    c_id, auth_id = await UsersDbManager.get_customer(ord_id, loop)
    bonuses = int(pm) / (100 * 1)
    await UsersDbManager.update_bonuses(tel_id, bonuses, loop)
    await UsersDbManager.update_payment(ord_id, pm, loop)
    await cb.confirm_all(c_id, ord_id, pm)
    await UsersDbManager.active_o(ord_id, pm, loop)
    await ab.confirm_order(auth_id, ord_id[1:])
    try:
        await bot.delete_message(tel_id, callback_query.message.message_id)
    except:
        a = None


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('more_'))
async def pp(callback_query: types.CallbackQuery):
    tel_id = callback_query.from_user.id
    ord_id = callback_query.data[4:]
    await UsersDbManager.update_num_owner(owner_id, ord_id, callback_query.message.message_id, loop)
    text = 'Сколько клиент заплатил?'
    await bot.send_message(owner_id, text=text, disable_notification=True)
    await UsersDbManager.update_context_owner(owner_id, 'wait_count', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wait_count')
async def wait_name(message):
    count = message.text
    count = re.sub("\D", "", count)
    ord_id, m_id = await UsersDbManager.get_num_owner(owner_id, loop)

    await UsersDbManager.update_payment(ord_id, count, loop)
    c_id, auth_id = await UsersDbManager.get_customer(ord_id, loop)
    price = await UsersDbManager.get_price(ord_id, loop)
    p = int(price) - int(count)

    await UsersDbManager.update_payment(ord_id, count, loop)

    await cb.confirm_fifty(c_id, ord_id, p)
    await ab.confirm_order(auth_id, ord_id[1:])
    await UsersDbManager.active_o(ord_id, count, loop)

    try:
        await bot.delete_message(owner_id, message.message_id)
        await bot.delete_message(owner_id, message.message_id-1)
        await bot.delete_message(owner_id, m_id)
    except:
        a = None


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('oke_'))
async def pp(callback_query: types.CallbackQuery):
    tel_id = callback_query.from_user.id
    ord_id = callback_query.data[4:]
    await bot.answer_callback_query(
        callback_query.id,
        text='100% оплата подтверждена!', show_alert=True)
    pm = await UsersDbManager.get_costt(ord_id, loop)
    bonuses = int(pm) / (100 * 1)
    await UsersDbManager.update_bonuses(tel_id, bonuses, loop)
    c_id = await UsersDbManager.get_customertwo(ord_id, loop)
    await UsersDbManager.update_payment(ord_id, pm, loop)
    await cb.dopl_yes(c_id, ord_id, pm)
    try:
        await bot.delete_message(tel_id, callback_query.message.message_id)
    except:
        a = None

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('moretwo_'))
async def pp(callback_query: types.CallbackQuery):
    ord_id = callback_query.data[7:]
    text = 'Сколько клиент заплатил?'
    await UsersDbManager.update_num_owner(owner_id, ord_id, callback_query.message.message_id, loop)
    await bot.send_message(owner_id, text=text, disable_notification=True)
    await UsersDbManager.update_context_owner(owner_id, 'w_count_two', loop)

@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'w_count_two')
async def wait_name(message):
    count = message.text
    count = re.sub("\D", "", count)
    ord_id, m_id = await UsersDbManager.get_num_owner(owner_id, loop)
    c_id = await UsersDbManager.get_customertwo(ord_id, loop)
    full_cost, payment = await UsersDbManager.get_pricetwo(ord_id, loop)
    dopl = int(full_cost) - int(payment) - int(count)
    await UsersDbManager.update_payment_two(ord_id, count, loop)
    await cb.confirm_np_dopl(c_id, ord_id, count)

    try:
        await bot.delete_message(owner_id, message.message_id)
        await bot.delete_message(owner_id, message.message_id-1)
        await bot.delete_message(owner_id, m_id)
    except:
        a = None



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
