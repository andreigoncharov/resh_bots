import asyncio

import aiogram.types as tp
import requests
from aiogram import Bot, Dispatcher, executor

import author_markup as mk
import markup as mk1
from config import AuthorTOKEN
from db_manager import UsersDbManager

bot = Bot(AuthorTOKEN)
dp = Dispatcher(bot)

loop = asyncio.get_event_loop()

TOKEN = AuthorTOKEN


@dp.message_handler(commands=['start'])
async def start(message):
    tel_id = message.chat.id

    text = 'Здравствуйте! 🖐\nНажмите кнопку ⬇️ Продолжить ⬇️ и ответьте на пару вопросов для авторизации в боте'
    kb = mk.start_kb
    await bot.send_message(tel_id, text=text, reply_markup=kb, disable_notification=True)


@dp.message_handler(content_types=tp.ContentType.CONTACT)
async def get_contact(message):
    tel_id = message.chat.id

    phone_number = message.contact.phone_number
    username = message["from"].username

    await UsersDbManager.add_author(tel_id, phone_number, username, loop)

    text = '💥 <b>Ваш профиль успешно подвязан к Вашему номеру телефона!</b> 💥'
    kb = tp.ReplyKeyboardRemove()
    await bot.send_message(tel_id, text=text, reply_markup=kb, disable_notification=True, parse_mode='html')

    text = 'Напишите ваше ФИО'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_fio', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context_a(message.chat.id) == 'wait_fio')
async def wait_name(message):
    tel_id = message.chat.id

    text = 'Напечатайте название Вашего университета‍🎓\n\n' \
           '<i>Это конфиденциальная информация, благодаря этому понимаем требования к работам.</i>'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_name_vuz_a', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context_a(message.chat.id) == 'wait_name_vuz_a')
async def wait_name(message):
    tel_id = message.chat.id

    vuz = str(message.text)
    await UsersDbManager.update_vuz_a(tel_id, vuz, loop)

    text = '<b>Укажите ваш курс</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.auth_kurs(), disable_notification=True, parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('kurs_'))
async def process_call(c):
    tel_id = c.message.chat.id
    kurs = str(c.data[5:])

    await UsersDbManager.update_step_a(tel_id, kurs, loop)

    text = '<b>Прикрепите, пожалуйста, Ваш студенческий.</b>\n(Номер документа, серию и штрихкод показывать не нужно)'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_ph_doc', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('aspir'))
async def process_call(c):
    tel_id = c.message.chat.id

    await UsersDbManager.update_step_a(tel_id, 'Аспирант', loop)

    text = '<b>Прикрепите файл-документ об образовании 📖</b>'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_ph_doc', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('prepod'))
async def process_call(c):
    tel_id = c.message.chat.id

    await UsersDbManager.update_step_a(tel_id, 'Преподаватель', loop)

    text = '<b>Прикрепите файл-документ об образовании 📖</b>'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_ph_doc', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('zak'))
async def process_call(c):
    tel_id = c.message.chat.id

    await UsersDbManager.update_step_a(tel_id, 'Закончил', loop)

    text = '<b>Прикрепите файл-документ об образовании 📖</b>'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, 'wait_ph_doc', loop)


@dp.message_handler(content_types=tp.ContentType.PHOTO)
async def sss1(message):
    tel_id = message.chat.id
    photo = None
    context = await UsersDbManager.get_context_a(tel_id, loop)
    if context == 'wait_ph_doc':
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(AuthorTOKEN, file_info.file_path))
        pht = file.content
        await UsersDbManager.insert_ph_img_a(tel_id, pht, loop)

        text = 'Укажите номер карты для оплаты заказов'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
        await UsersDbManager.update_context_a(tel_id, 'wait_card', loop)

    elif context == 'online_work':
        customer = await UsersDbManager.get_cust_id(tel_id, loop)

        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(AuthorTOKEN, file_info.file_path))
        pht = file.content
        await bot.send_photo(chat_id=customer, photo=pht)

    elif context == 'wait_done':
        ord_id = await UsersDbManager.get_num_a(tel_id, loop)

        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
        await UsersDbManager.insert_author_links(ord_id, link, loop)


@dp.message_handler(content_types=tp.ContentType.DOCUMENT)
async def sss1(message):
    tel_id = message.chat.id
    doc = None
    context = await UsersDbManager.get_context(tel_id, loop)
    ord_id = await UsersDbManager.get_ord_id(tel_id, loop)

    if context == 'online_work':
        customer = await UsersDbManager.get_cust_id(tel_id, loop)

        doc = message.document.file_id
        file_info = await bot.get_file(doc)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content
        await bot.send_document(chat_id=customer, document=pht)

    ord_id = await UsersDbManager.get_num_a(tel_id, loop)
    if context == 'wait_files':
        doc = message.document.file_id
        file_info = await bot.get_file(doc)
        link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
        await UsersDbManager.insert_author_links(ord_id, link, loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context_a(message.chat.id) == 'wait_card')
async def wait_name(message):
    tel_id = message.chat.id
    await UsersDbManager.update_card_a(tel_id, str(message.text), loop)

    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.prof, disable_notification=True, parse_mode='html')

    await UsersDbManager.update_context_a(tel_id, '', loop)


@dp.message_handler(lambda message: message.text == 'Естественные науки ‍🔬🧬')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-2], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Технический профиль 🛠💻')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-2], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Гуманитарные предметы 👩‍🎓')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-3], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Экономические дисциплины 📊')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-1], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Языки 🗣')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-1], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Право, юриспруденция ⚖️')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof_a(tel_id, message.text[:-1], loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text in mk1.a)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm_a(tel_id, message.text, loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text in mk1.t)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm_a(tel_id, message.text, loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text in mk1.g)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm_a(tel_id, message.text, loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text in mk1.e)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm_a(tel_id, message.text, loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text in mk1.l)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm_a(tel_id, message.text, loop)
    await bot.send_message(tel_id, text=str(message.text), reply_markup=mk1.prof, disable_notification=True)
    await bot.send_message(tel_id, text='<b>Выберете профиль</b>', reply_markup=mk.zav(), disable_notification=True,
                           parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('zaver'))
async def process_call(c):
    tel_id = c.message.chat.id
    text = 'Спасибо, подождите пока модератор даст Вам доступ к заказам'
    await bot.send_message(tel_id, text=text, reply_markup=tp.ReplyKeyboardRemove(), disable_notification=True)
    await send_confirm(tel_id)
    await UsersDbManager.update_context_a(tel_id, 'wait_confirm', loop)


async def send_confirm(tel_id):
    # Подверждение отправляется кому-то там

    text = '🎊 Успешная авторизация 🎊\n\n' \
           '🙌Оценивайте заказы\n' \
           '📝Выполняйте задания\n' \
           '💸Зарабатывайте вместе с нами\n\n' \
           'Если у вас появились вопросы, свяжитесь с менеджером\n' \
           '⌨️ https://t.me/reshalaa_help\n' \
           '📱 +380634690637'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context_a(tel_id, '', loop)


@dp.message_handler(lambda message: message.text == 'Свободные заказы 📝')
async def loc_m(message):
    tel_id = message.chat.id
    orders = await UsersDbManager.get_orders(tel_id, loop)
    if orders is None:
        text = '<b>К сожалению, свободных заказов по Вашему профилю не найдено</b> 🙁\n' \
               'Как только появятся, мы сразу сообщим'
        await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_1,
                               disable_notification=True, parse_mode='html')
    else:
        for order in orders:
            vuz = await UsersDbManager.get_user_vuz(order[1], loop)

            text = f'✨ Заказ №{order[0]} ✨\n\n' \
                   f'<b>{order[4]}</b>\n' \
                   f'<b>{order[2]}</b>\n\n' \
                   f'Срок сдачи: {order[7]} {order[8]}\n' \
                   f'Цена: {order[10]}\n\n' \
                   f'Оформление: {order[6]}\n' \
                   f'Комментарий: {order[5]}\n\n' \
                   f'ВУЗ: {vuz}' \
                   f'\nПрикрипленные файлы:'
            await bot.send_message(tel_id, text=text, reply_markup=mk.ord_1(order[0]), disable_notification=True,
                                   parse_mode='html')
            await send_files(tel_id, order[0])


async def send_files(tel_id, order_id):
    docs = await UsersDbManager.get_docs(order_id, loop)
    ph = []
    if docs == False:
        await bot.send_message(tel_id, text='Нет прикрипленных файлов', disable_notification=True)
    else:
        for doc in docs:
            if doc[2] == 'photto':
                await bot.send_photo(tel_id, photo=doc[1])
            else:
                await bot.send_document(tel_id, document=doc[1])


@dp.callback_query_handler(lambda c: c.data.startswith('nint_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = str(c.data[5:])
    text = f'Вы отказались от оценки заказа <b>№{ord_id}</b>'
    await bot.edit_message_text(text=text, message_id=c.message.message_id, parse_mode='html')
    await UsersDbManager.add_pre_order_author(ord_id, tel_id, loop)
    await UsersDbManager.update_ord_price(tel_id, '---', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('otzenit_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = str(c.data[8:])

    text = f'<b>Оцените заказ №{ord_id}</b> 🤩\nУкажите цену, за которую Вы готовы выполнить этот заказ.\n' \
           '❗️ Указывайте только цифры❗️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz, disable_notification=True, parse_mode='html')

    await UsersDbManager.update_context_a(tel_id, 'wait_price_a', loop)
    await UsersDbManager.add_pre_order_author(ord_id, tel_id, loop)


@dp.message_handler(lambda message: message.text == '❌ Отменить оценку ❌')
async def loc_m(message):
    tel_id = message.chat.id
    text = 'Оценка заказа отменена!'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_1, disable_notification=True)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context_a(message.chat.id) == 'wait_price_a')
async def wait_name(message):
    tel_id = message.chat.id
    price = str(message.text)

    await UsersDbManager.update_ord_price(tel_id, price, loop)
    await UsersDbManager.update_context_a(tel_id, 'wait_com_a', loop)

    text = '<b>Ваша оценка принята, можете написать комментарий' \
           ' или задать уточняющий вопрос</b> 😉'
    await bot.send_message(tel_id, text=text, reply_markup=mk.no_com,
                           disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context_a(message.chat.id) == 'wait_com_a')
async def wait_name(message):
    tel_id = message.chat.id
    com = str(message.text)

    await UsersDbManager.update_ord_com(tel_id, com, loop)
    await UsersDbManager.update_context_a(tel_id, '', loop)

    text = '❗️ <b>Не приступайте к выполнению, пока не придёт подтверждение</b>❗️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_2,
                           disable_notification=True, parse_mode='html')


async def confirm_order(tel_id, ord_id):
    order, vuz = await UsersDbManager.get_order_a(ord_id, loop)
    price = await UsersDbManager.get_a_price(ord_id, tel_id, loop)

    text = f'<b>Заказ №{ord_id} ваш!</b> 🚀\n\n' \
           f'✨ Заказ №{order[0]} ✨\n\n' \
           f'<b>{order[4]}</b>\n' \
           f'<b>{order[2]}</b>\n\n' \
           f'Срок сдачи: {order[7]} {order[8]}\n' \
           f'Цена: {price}\n\n' \
           f'Оформление: {order[6]}\n' \
           f'Комментарий: {order[5]}\n\n' \
           f'ВУЗ: {vuz}' \
           f'\nПрикрипленные файлы:'
    await bot.send_message(tel_id, text=text, reply_markup=mk.ord_1(order[0]), disable_notification=True,
                           parse_mode='html')
    await send_files(tel_id, order[0])


async def send_time(tel_id, ord_id):
    text = f'<b>Решение №{ord_id} через 10 мин !</b> 🚀\nНажмите <b>войти в чат с заказчиком</b> и ожидайте работу.\n' \
           'Или же заказчик сам добавит вас в чат, когда будут задания.' \
           '\n\nВыполненные задания скидывайте по мере решения.'
    await bot.send_message(tel_id, text=text, reply_markup=mk.onl(), parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('enter_online'))
async def process_call(c):
    tel_id = c.message.chat.id

    customer = await UsersDbManager.get_cust_id(tel_id, loop)

    text_2 = '<b>Вы вошли в чат с заказчиком.</b>\n' \
             'Можете задавать уточняющие вопросы и когда работа будет закончена, можете покинуть чат.\n' \
             'Если появятся дополнительные задания, можете оценить заказ.'
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.onl_2, parse_mode='html')

    text = '<b>В чат подключен автор</b> 🚀\n' \
           'Скиньте, пожалуйста, фото билета'
    await bot.send_message(customer, text=text, reply_markup=mk1.author_otm, parse_mode='html')

    await UsersDbManager.update_context_a(tel_id, 'online_work', loop)
    await UsersDbManager.update_context(customer, 'online_work', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'online_work')
async def wait_name(message):
    tel_id = message.chat.id
    customer = await UsersDbManager.get_cust_id(tel_id, loop)
    await bot.send_message(customer, text=message.text)


@dp.message_handler(lambda message: message.text == 'Онлайн работа закончена  ❌')
async def loc_m(message):
    tel_id = message.chat.id

    customer = await UsersDbManager.get_cust_id(tel_id, loop)

    text = 'oko'
    await bot.send_message(tel_id, text=text)
    await UsersDbManager.update_context(customer, '', loop)

    await UsersDbManager.update_context_a(tel_id, '', loop)


async def send_new_order(ord_id):
    order = await UsersDbManager.get_new_order(ord_id, loop)
    tel_id = order[1]
    user = await UsersDbManager.get_user(tel_id, loop)
    text = f'✨ Заказ №{order[0]} ✨\n\n' \
           f'<b>{order[4]}</b>\n' \
           f'<b>{order[2]}</b>\n\n' \
           f'Срок сдачи: {order[7]} {order[8]}\n' \
           f'Цена: {order[10]}\n\n' \
           f'Оформление: {order[6]}\n' \
           f'Комментарий: {order[5]}\n\n' \
           f'ВУЗ: {user[3]}' \
           f'\nПрикрипленные файлы:'
    authors = await UsersDbManager.get_authors(ord_id, loop)
    for author in authors:
        await bot.send_message(author[0], text=text, reply_markup=mk.ord_1(order[0]), disable_notification=True,
                               parse_mode='html')
        await send_files(tel_id, order[0])


async def confirm_order(tel_id, ord_id):
    order = await UsersDbManager.get_active_order(ord_id, loop)
    print('order:', order)
    author_price = await UsersDbManager.get_author_price(ord_id, loop)
    print('ap:', author_price)

    vuz = await UsersDbManager.get_user_vuz(order[1], loop)
    print('vuz:', vuz)
    if str(order[2]) == 'Online решение' or str(order[2]) == 'Тест дистанционно':
        text = f'<b>Заказ №{ord_id} ваш!</b> 🚀\n\n' \
               f'✨ Заказ №{ord_id} ✨ \n\n' \
               f'<b>Предмет:</b> {order[4]}\n' \
               f'<b>Тип работы:</b> {order[2]}\n\n' \
               f'Срок сдачи: {order[7]}\n' \
               f'\n{order[8]}-{order[9]}\n' \
               f'Цена: {author_price}\n\n' \
               f'Оформление:{order[6]}\n' \
               f'Комментарий: {order[5]}\n\n' \
               f'Вуз: {vuz}\n' \
               f'Прикрепленные файлы:'
    else:
        text = f'<b>Заказ №{ord_id} ваш!</b> 🚀\n\n' \
               f'✨ Заказ №{ord_id} ✨ \n\n' \
               f'<b>Предмет:</b> {order[4]}\n' \
               f'<b>Тип работы:</b> {order[2]}\n\n' \
               f'Срок сдачи: {order[7]} {order[8]}\n' \
               f'Цена: {author_price}\n\n' \
               f'Оформление:{order[6]}\n' \
               f'Комментарий: {order[5]}\n\n' \
               f'Вуз: {vuz}\n' \
               f'Прикрепленные файлы:'
    await bot.send_message(tel_id, text=text, reply_markup=mk.ready(ord_id), parse_mode='html')
    await send_files(tel_id, ord_id)


@dp.callback_query_handler(lambda c: c.data.startswith('done_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = str(c.data[5:])
    text = 'Пришлите фотографии или файлы с выполненным заданием. Когда отправите все необходимые файлы, нажмите Готово'
    await bot.send_message(tel_id, text=text, reply_markup=mk1.ok)
    await UsersDbManager.update_context_a(tel_id, 'wait_done', loop)
    #await UsersDbManager.add_num_a(tel_id, ord_id, loop)
    await UsersDbManager.waito(ord_id, loop)

@dp.message_handler(lambda message: message.text == 'Готово')
async def loc_m(message):
    tel_id = message.chat.id

    text = 'Решение отправлено на проверку!'
    await bot.send_message(tel_id, text=text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
