from aiogram.types import reply_keyboard, inline_keyboard
import asyncio

loop = asyncio.get_event_loop()

start_kb = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add(reply_keyboard.KeyboardButton('⬇️ Продолжить ⬇️', request_contact=True))

main_menu = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('Свободные заказы 📝')) \
    .add(reply_keyboard.KeyboardButton('Мои заказы 🙏')) \
    .add(reply_keyboard.KeyboardButton('Связь с менеджером 📱')) \
    .add(reply_keyboard.KeyboardButton('Редактировать профиль 🙌')) \
    .add(reply_keyboard.KeyboardButton('Мои средства 💸'))

main_menu_1 = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('Свободные заказы 📝')) \
    .add(reply_keyboard.KeyboardButton('Мои заказы 🙏')) \
    .add(reply_keyboard.KeyboardButton('Связь с менеджером 📱')) \
    .add(reply_keyboard.KeyboardButton('Редактировать профиль 🙌'))

main_menu_2 = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('Свободные заказы 📝')) \
    .add(reply_keyboard.KeyboardButton('Мои заказы 🙏')) \
    .add(reply_keyboard.KeyboardButton('Связь с менеджером 📱'))

otm_otz = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('❌ Отменить оценку ❌'))

no_com = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('❌ Не оставлять комментарий'))


def auth_kurs():
    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('1', callback_data=f'kurs_{1}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('2', callback_data=f'kurs_{2}')
    inline_btn_2 = inline_keyboard.InlineKeyboardButton('3', callback_data=f'kurs_{3}')
    inline_btn_3 = inline_keyboard.InlineKeyboardButton('4', callback_data=f'kurs_{4}')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton('5', callback_data=f'kurs_{5}')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton('6', callback_data=f'kurs_{6}')

    inline_kb_full.row(inline_btn_0, inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton('Аспирант', callback_data='aspir')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton('Перподаватель', callback_data='prepod')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton('Закончил', callback_data='zak')

    inline_kb_full.add(inline_btn_3)
    inline_kb_full.add(inline_btn_4)
    inline_kb_full.add(inline_btn_5)

    return inline_kb_full


def zav():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('⬇️ Завершить ⬇️', callback_data='zaver'))
    return k


def ord_1(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Оценить 💰', callback_data=f'otzenit_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Не интересно 🗑', callback_data=f'nint_{ord_id}'))

    return k

def onl():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Войти в чат с заказчиком', callback_data=f'enter_online'))
    k.add(inline_keyboard.InlineKeyboardButton('Связь с менеджером', callback_data=f'manager'))
    return k

onl_2 = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False) \
    .add(reply_keyboard.KeyboardButton('Оценить 💸')) \
    .add(reply_keyboard.KeyboardButton('Онлайн работа закончена❌')) \
    .add(reply_keyboard.KeyboardButton('Свободные заказы 📖 '))

def ready(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('✅ Заказ готов', callback_data=f'done_{ord_id}'))
    return k