from aiogram.types import reply_keyboard, inline_keyboard
from db_manager import UsersDbManager
import asyncio
import datetime

loop = asyncio.get_event_loop()


start_kb = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(reply_keyboard.KeyboardButton('⬇️ Продолжить ⬇️', request_contact=True))
'''
loc_kb = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Отправить текущую локацию 📍', request_location=True))

loc_menu  = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Отправить текущую локацию 📍', request_location=True))
#.add(reply_keyboard.KeyboardButton('Написать адрес 🖊'))

#main_menu_ru = reply_keyboard.ReplyKeyboardMarkup([['🚕 Заказать такси 🚕'], ['📍 Мои локации 📍'], ['💾 История заказов 💾']])'''

main_menu_ru = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=False).add(reply_keyboard.KeyboardButton('Оформление заказа 📖'))\
    .add(reply_keyboard.KeyboardButton('Связь с менеджером 📱'))\
    .add(reply_keyboard.KeyboardButton('Мои заказы 🛒'))\
    .add(reply_keyboard.KeyboardButton('Мои бонусы 💰'))

otmena = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('❌ Отменить оформление заказа ❌'))

def cont_1():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Продолжить 🚀', callback_data='cont_1'))
    return k

types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Online решение 🚀'))\
    .add(reply_keyboard.KeyboardButton('Тест дистанционно'))       .add(reply_keyboard.KeyboardButton('ДЗ')) \
    .add(reply_keyboard.KeyboardButton('Эссе'))    .add(reply_keyboard.KeyboardButton('Реферат')) \
    .add(reply_keyboard.KeyboardButton('Презентация'))    .add(reply_keyboard.KeyboardButton('Перевод')) \
    .add(reply_keyboard.KeyboardButton('Лабораторная работа'))    .add(reply_keyboard.KeyboardButton('Расчетная работа (РГР)')) \
    .add(reply_keyboard.KeyboardButton('Бизнес-план'))    .add(reply_keyboard.KeyboardButton('Курсовая')) \
    .add(reply_keyboard.KeyboardButton('Дипломная'))    .add(reply_keyboard.KeyboardButton('Магистерская')) \
    .add(reply_keyboard.KeyboardButton('Отчет по практике'))    .add(reply_keyboard.KeyboardButton('Другое'))\
    .add(reply_keyboard.KeyboardButton('❌ Отменить оформление заказа ❌'))


prof = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Естественные науки ‍🔬🧬'))\
    .add(reply_keyboard.KeyboardButton('Технический профиль 🛠💻')) \
    .add(reply_keyboard.KeyboardButton('Гуманитарные предметы 👩‍🎓'))    .add(reply_keyboard.KeyboardButton('Экономические дисциплины 📊')) \
    .add(reply_keyboard.KeyboardButton('Право, юриспруденция ⚖️'))    .add(reply_keyboard.KeyboardButton('Языки 🗣'))

def predm(prof):
    types = []
    if types != []:
        poi = None
    elif prof == 'Естественные науки ':
        types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(
            reply_keyboard.KeyboardButton('Астрономия')) \
            .add(reply_keyboard.KeyboardButton('БЖД')) \
            .add(reply_keyboard.KeyboardButton('География'))\
            .add(reply_keyboard.KeyboardButton('Геология')) \
            .add(reply_keyboard.KeyboardButton('Химия'))\
            .add(reply_keyboard.KeyboardButton('Биология'))\
            .add(reply_keyboard.KeyboardButton('Физика'))\
            .add(reply_keyboard.KeyboardButton('Экология'))\
            .add(reply_keyboard.KeyboardButton('Медицина'))\
            .add(reply_keyboard.KeyboardButton('Фармация')) \
            .add(reply_keyboard.KeyboardButton('Другое'))\
            .add(reply_keyboard.KeyboardButton('⬅️ Назад'))

    elif prof == 'Технический профиль ':
        types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(
            reply_keyboard.KeyboardButton('Математика')) \
            .add(reply_keyboard.KeyboardButton('Высшая математика')) \
            .add(reply_keyboard.KeyboardButton('Дискретная математика')).add(reply_keyboard.KeyboardButton('Теория вероятности')) \
            .add(reply_keyboard.KeyboardButton('Статистика')).add(reply_keyboard.KeyboardButton('Информатика')) \
            .add(reply_keyboard.KeyboardButton('Программирование')).add(reply_keyboard.KeyboardButton('Гидравлика')) \
            .add(reply_keyboard.KeyboardButton('Компьютерная графика')).add(reply_keyboard.KeyboardButton('Черчение')) \
            .add(reply_keyboard.KeyboardButton('Метрология')).add(reply_keyboard.KeyboardButton('Сопромат')) \
            .add(reply_keyboard.KeyboardButton('Строймех')).add(reply_keyboard.KeyboardButton('Теормех'))\
            .add(reply_keyboard.KeyboardButton('Физика')).add(reply_keyboard.KeyboardButton('Электротехника')) \
            .add(reply_keyboard.KeyboardButton('Другое')) \
            .add(reply_keyboard.KeyboardButton('⬅️ Назад'))
    elif prof == 'Гуманитарные предметы ':
        types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(
            reply_keyboard.KeyboardButton('История')) \
            .add(reply_keyboard.KeyboardButton('Литература')) \
            .add(reply_keyboard.KeyboardButton('Психология')).add(reply_keyboard.KeyboardButton('Социлогия')) \
            .add(reply_keyboard.KeyboardButton('Философия')).add(reply_keyboard.KeyboardButton('Логика')) \
            .add(reply_keyboard.KeyboardButton('Реклама')).add(reply_keyboard.KeyboardButton('Маркетинг')) \
            .add(reply_keyboard.KeyboardButton('Педагогика')).add(reply_keyboard.KeyboardButton('Языки')) \
            .add(reply_keyboard.KeyboardButton('Другое')) \
            .add(reply_keyboard.KeyboardButton('⬅️ Назад'))
    elif prof == 'Экономические дисциплины ':
        types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(
            reply_keyboard.KeyboardButton('Бух учет')) \
            .add(reply_keyboard.KeyboardButton('Менеджмент')) \
            .add(reply_keyboard.KeyboardButton('Маркетинг')).add(reply_keyboard.KeyboardButton('Статистика')) \
            .add(reply_keyboard.KeyboardButton('Макроэкономика')).add(reply_keyboard.KeyboardButton('Микроэкономика')) \
            .add(reply_keyboard.KeyboardButton('Экономика предприятия')).add(reply_keyboard.KeyboardButton('Экономика')) \
            .add(reply_keyboard.KeyboardButton('Управление эффективностью')).add(reply_keyboard.KeyboardButton('Другое'))\
            .add(reply_keyboard.KeyboardButton('⬅️ Назад'))
    elif prof == 'Языки ':
        types = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(
            reply_keyboard.KeyboardButton('Английский')) \
            .add(reply_keyboard.KeyboardButton('Украинский')) \
            .add(reply_keyboard.KeyboardButton('Русский')).add(reply_keyboard.KeyboardButton('Испанский')) \
            .add(reply_keyboard.KeyboardButton('Итальянский')).add(reply_keyboard.KeyboardButton('Китайский')) \
            .add(reply_keyboard.KeyboardButton('Немецкий')).add(reply_keyboard.KeyboardButton('Французский')) \
            .add(reply_keyboard.KeyboardButton('Другое')) \
            .add(reply_keyboard.KeyboardButton('⬅️ Назад'))
    return types



a = ['Астрономия','БЖД','География','Геология','Химия','Биология','Физика','Экология','Медицина','Фармация', 'Другое', '⬅️ Назад']
t = ['Математика', 'Высшая математика', 'Дискретная математика', 'Теория вероятности', 'Статистика', 'Информатика', 'Программирование',
     'Гидравлика', 'Метрология', 'Сопромат', 'Строймех', 'Теормех', 'Физика', 'Электротехника', 'Другое', '⬅️ Назад']
g = ['История', 'Литература', 'Психология', 'Социлогия', 'Философия', 'Логика', 'Реклама', 'Маркетинг', 'Педагогика', 'Языки', 'Другое', '⬅️ Назад']
e = ['Бух учет', 'Менеджмент', 'Маркетинг', 'Статистика', 'Макроэкономика', 'Микроэкономика', 'Экономика предприятия', 'Экономика', 'Управление эффективностью', 'Другое', '⬅️ Назад']
l = ['Английский', 'Украинский', 'Русский', 'Испанский', 'Итальянский', 'Китайский', 'Немецкий', 'Французский', 'Другое', '⬅️ Назад']

def otr():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('От руки 📝', callback_data='ruk'))
    k.add(inline_keyboard.InlineKeyboardButton('Электронный вид ⌨️', callback_data='elect'))
    k.add(inline_keyboard.InlineKeyboardButton('Не принципиально', callback_data='ne_prcpl'))
    return k

def ready():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Готово 👌', callback_data='ready'))
    k.add(inline_keyboard.InlineKeyboardButton('❌ Пропустить отправку файлов ', callback_data='prop'))
    return k

otmena_plus = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Готово 👌'))\
                                            .add(reply_keyboard.KeyboardButton('❌ Пропустить отправку файлов'))\
                                            .add(reply_keyboard.KeyboardButton('❌ Отменить оформление заказа ❌'))



def get_month():
    day = datetime.datetime.today().date().day
    day = str(day)

    month = datetime.datetime.now().month
    month = str(month)

    year = datetime.datetime.today().date().year
    year = str(year)

    monthes = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май',
               '6': 'Июнь',
               '7': 'Июль', '8': 'Август', '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь',
               '12': 'Декабрь'}

    return day, monthes.get(str(month)), year, month

def datekb():
    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()
    day, month, year, num_month = get_month()
    print(day, month, year, num_month)

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'datev_{day}!{num_month}!{year}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'mnthv_{day}!{num_month}!{year}')
    inline_btn_2 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'yearv_{day}!{num_month}!{year}')

    inline_kb_full.row(inline_btn_0, inline_btn_1, inline_btn_2)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(day, callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(month, callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(year, callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'daten_{day}!{num_month}!{year}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'mnthn_{day}!{num_month}!{year}')
    inline_btn_8 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'yearn_{day}!{num_month}!{year}')

    inline_kb_full.row(inline_btn_6, inline_btn_7, inline_btn_8)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv_{day}.{num_month}.{year}')
    inline_kb_full.add(inline_btn_9)

    return inline_kb_full

def date_2(day=None, month=None, year=None):
    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()
    num_month = datetime.datetime.now().month

    if day == None:
        day = datetime.datetime.today().date().day
        day = str(day)

    month = str(month)

    num_month = month

    monthes = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май',
                   '6': 'Июнь',
                   '7': 'Июль', '8': 'Август', '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь',
                   '12': 'Декабрь'}
    month = monthes.get(str(month))

    print('day: ', day, ' month: ', month, ' year: ', year)

    if year == None:
        year = datetime.datetime.today().date().year
        year = str(year)

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'datev_{day}!{num_month}!{year}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'mnthv_{day}!{num_month}!{year}')
    inline_btn_2 = inline_keyboard.InlineKeyboardButton('⬆️', callback_data=f'yearv_{day}!{num_month}!{year}')

    inline_kb_full.row(inline_btn_0, inline_btn_1, inline_btn_2)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(day, callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(month, callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(year, callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'daten_{day}!{num_month}!{year}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'mnthn_{day}!{num_month}!{year}')
    inline_btn_8 = inline_keyboard.InlineKeyboardButton('⬇️', callback_data=f'yearn_{day}!{num_month}!{year}')

    inline_kb_full.row(inline_btn_6, inline_btn_7, inline_btn_8)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv_{day}.{num_month}.{year}')
    inline_kb_full.add(inline_btn_9)


    return inline_kb_full

def timekb(tel_id, num):
    time = UsersDbManager.get_time_t(tel_id)
    s = str(UsersDbManager.sync_get_type(tel_id))
    t = UsersDbManager.get_time(tel_id)

    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False

    if s is True and num == 3 and time is False:
        hour = '10'
        minutes = '00'
    elif s is True and num == 2 and time is False and t is None:
        hour = '9'
        minutes = '00'
    else:
        hour = '19'
        minutes = '00'

    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('➕ 1 час', callback_data=f'hourp_{hour}!{minutes}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('➕ 15 минут', callback_data=f'minut_{hour}!{minutes}')

    inline_kb_full.row(inline_btn_0, inline_btn_1)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(str(hour), callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(':', callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(str(minutes), callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('➖ 1 час', callback_data=f'hourm_{hour}!{minutes}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('➖ 15 минут', callback_data=f'minum_{hour}!{minutes}')


    inline_kb_full.row(inline_btn_6, inline_btn_7)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv{num}_{hour}:{minutes}')
    inline_kb_full.add(inline_btn_9)

    return inline_kb_full

def timekb_2(hour=None, minutes= None, num=None, tel_id=None):

    print('numt2:', num)

    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('➕ 1 час', callback_data=f'hourp_{hour}!{minutes}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('➕ 15 минут', callback_data=f'minut_{hour}!{minutes}')

    inline_kb_full.row(inline_btn_0, inline_btn_1)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(str(hour), callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(':', callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(str(minutes), callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('➖ 1 час', callback_data=f'hourm_{hour}!{minutes}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('➖ 15 минут', callback_data=f'minum_{hour}!{minutes}')


    inline_kb_full.row(inline_btn_6, inline_btn_7)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv{num}_{hour}:{minutes}')
    inline_kb_full.add(inline_btn_9)

    return inline_kb_full

'''def ontimekb(num):

    hour = '10'
    minutes = '00'

    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('➕ 1 час', callback_data=f'hourp_{hour}!{minutes}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('➕ 15 минут', callback_data=f'minut_{hour}!{minutes}')

    inline_kb_full.row(inline_btn_0, inline_btn_1)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(str(hour), callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(':', callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(str(minutes), callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('➖ 1 час', callback_data=f'hourm_{hour}!{minutes}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('➖ 15 минут', callback_data=f'minum_{hour}!{minutes}')


    inline_kb_full.row(inline_btn_6, inline_btn_7)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv3_{hour}:{minutes}')
    inline_kb_full.add(inline_btn_9)

    return inline_kb_full

def ontimekb_2(hour=None, minutes= None):

    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()

    inline_btn_0 = inline_keyboard.InlineKeyboardButton('➕ 1 час', callback_data=f'hourp_{hour}!{minutes}')
    inline_btn_1 = inline_keyboard.InlineKeyboardButton('➕ 15 минут', callback_data=f'minut_{hour}!{minutes}')

    inline_kb_full.row(inline_btn_0, inline_btn_1)

    inline_btn_3 = inline_keyboard.InlineKeyboardButton(str(hour), callback_data='0')
    inline_btn_4 = inline_keyboard.InlineKeyboardButton(':', callback_data='0')
    inline_btn_5 = inline_keyboard.InlineKeyboardButton(str(minutes), callback_data='0')

    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)

    inline_btn_6 = inline_keyboard.InlineKeyboardButton('➖ 1 час', callback_data=f'hourm_{hour}!{minutes}')
    inline_btn_7 = inline_keyboard.InlineKeyboardButton('➖ 15 минут', callback_data=f'minum_{hour}!{minutes}')


    inline_kb_full.row(inline_btn_6, inline_btn_7)

    inline_btn_9 = inline_keyboard.InlineKeyboardButton('Подтвердить', callback_data=f'podtv3_{hour}:{minutes}')
    inline_kb_full.add(inline_btn_9)

    return inline_kb_full'''

def dogov():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Договорная', callback_data='dogov'))
    return k

def got():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Готово 🙌', callback_data='got'))
    return k

def manager():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Связь с менеджером 📱', callback_data='manager'))
    return k

def get_sv():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Написать ⌨️', callback_data='textman'))
    k.add(inline_keyboard.InlineKeyboardButton('Позвонить 📱️', callback_data='call_man'))
    return k

def online_kb():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Подключить автора в чат', callback_data='get_author'))
    k.add(inline_keyboard.InlineKeyboardButton('Онлайн работы не будет ❌', callback_data='no_online'))
    return k

otm_manager = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('❌ Отменить связь с менеджером❌'))

author_otm = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Онлайн работа закончена  ❌'))

def send_man():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Написать ⌨️', callback_data='send_manager'))
    return k

async def orders_keyboard(ord_id):
    inline_kb_full = inline_keyboard.InlineKeyboardMarkup()
    inline_btn_01 = inline_keyboard.InlineKeyboardButton(f'Оценка 💰', callback_data=f'')
    inline_btn_02 = inline_keyboard.InlineKeyboardButton(f' Отказались 🗑', callback_data=f'')
    inline_kb_full.row(inline_btn_01, inline_btn_02)

    prices = await UsersDbManager.get_order_author_pre(ord_id, loop)
    for price in prices:
        username = await UsersDbManager.get_username_a(price[1], loop)
        inline_btn_0 = inline_keyboard.InlineKeyboardButton(f'@{username} - {price[2]}', callback_data=f'author_{price[1]}')
        inline_btn_1 = inline_keyboard.InlineKeyboardButton(f'@{username}', callback_data=f'')
        inline_kb_full.row(inline_btn_0, inline_btn_1)

    return inline_kb_full

def pay_or_not(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить 💰', callback_data=f'pay_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('❌ Отменить заказ ❌', callback_data=f'otmena_{ord_id}'))
    return k

def pay(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить 💰', callback_data=f'pay_{ord_id}'))
    return k

def fifty_or_all(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Оплатил 50%', callback_data=f'fifty_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Оплатил 100%', callback_data=f'all_{ord_id}'))
    return k

def all(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('100%', callback_data=f'oke_{ord_id}'))
    return k

def otm_otz():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('❌ Отменить оценку заказа ❌', callback_data=f'otm_otz'))
    return k

def otz(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    one = inline_keyboard.InlineKeyboardButton('1️⃣', callback_data=f'one_{ord_id}')
    two = inline_keyboard.InlineKeyboardButton('2️⃣', callback_data=f'two_{ord_id}')
    three = inline_keyboard.InlineKeyboardButton('3️⃣', callback_data=f'three_{ord_id}')
    four = inline_keyboard.InlineKeyboardButton('4️⃣', callback_data=f'four_{ord_id}')
    five = inline_keyboard.InlineKeyboardButton('5️⃣', callback_data=f'five_{ord_id}')
    k.row(one, two, three, four, five)
    return k

ok = reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True).add(reply_keyboard.KeyboardButton('Готово'))

def why_otm(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Дорого', callback_data=f'exp_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Сделал сам', callback_data=f'myself_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Заказал у других людей', callback_data=f'other_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Другое', callback_data=f'another_{ord_id}'))

    return k
