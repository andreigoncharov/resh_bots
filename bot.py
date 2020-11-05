import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.text_decorations import markdown_decoration
import markup as mk
from config import TOKEN
from db_manager import UsersDbManager
import aiogram.types as tp
from aiogram.types import labeled_price, ChatActions
import requests
import datetime
from io import BytesIO
import re
import author_markup as mk2
import author_bot
import ConfirmationOfOrders_bot

bot = Bot(TOKEN)
dp = Dispatcher(bot)

loop = asyncio.get_event_loop()

'''
Начало работы с ботом и регистрация пользователя
'''


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
    first_name = message.contact.first_name
    username = message["from"].username

    await UsersDbManager.add_user(tel_id, first_name, phone_number, username, loop)

    text = '💥 <b>Ваш профиль успешно подвязан к Вашему номеру телефона!</b> 💥'
    kb = tp.ReplyKeyboardRemove()
    await bot.send_message(tel_id, text=text, reply_markup=kb, disable_notification=True, parse_mode='html')

    text = 'Напечатайте название Вашего университета‍🎓\n' \
           '<i>Это конфиденциальная информация, благодаря этому понимаем требования к работам.</i>'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context(tel_id, 'wait_name', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wait_name')
async def wait_name(message):
    tel_id = message.chat.id
    await UsersDbManager.update_vuz(tel_id, str(message.text), loop)

    text = 'Вы успешно прошли регистрацию! 🎉\n' \
           'Для оформления заказа 📖  или связи с менеджером 🙋 воспользуйтесь главным меню внизу 👇'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True)
    await UsersDbManager.update_context(tel_id, '', loop)


@dp.message_handler(lambda message: message.text == 'Оформление заказа 📖')
async def loc_m(message):
    tel_id = message.chat.id
    text = 'Оформление заказа 📖 '
    text_2 = '❗️ Указывайте информацию о заказе как можно детальнее ❗️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True)
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.cont_1(), disable_notification=True)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('cont_1'))
async def count_yes(call):
    tel_id = call.message.chat.id
    text = '<b>Выберите тип работы</b> 🙂'
    await bot.send_message(tel_id, text=text, reply_markup=mk.types, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Online решение 🚀')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, 'Online решение', loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Тест дистанционно')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'ДЗ')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Эссе')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Реферат')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Презентация')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Перевод')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Лабораторная')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Расчетная работа (РГР)')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Бизнес-план')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Курсовая')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Дипломная')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Магистерская')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Отчет по практике')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Другое')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_type(tel_id, message.text, loop)
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == '⬅️ Назад')
async def loc_m(message):
    tel_id = message.chat.id
    text = '<b>Выберете профиль</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.prof, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Естественные науки ‍🔬🧬')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-2], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Технический профиль 🛠💻')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-2], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text[:-2]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Гуманитарные предметы 👩‍🎓')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-3], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text[:-3]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Экономические дисциплины 📊')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-1], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text[:-1]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Языки 🗣')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-1], loop)
    text = f'<b>Выберете предмет</b> 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text[:-1]), disable_notification=True,
                           parse_mode='html')


@dp.message_handler(lambda message: message.text == 'Языки')
async def loc_m(message):
    tel_id = message.chat.id
    # await UsersDbManager.update_prof(tel_id, message.text[:-1], loop)
    text = f'Выберете язык 👌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.predm(message.text + ' '), disable_notification=True)


@dp.message_handler(lambda message: message.text == 'Право, юриспруденция ⚖️')
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_prof(tel_id, message.text[:-1], loop)
    await UsersDbManager.update_predm(tel_id, message.text[:-1], loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


@dp.message_handler(lambda message: message.text in mk.a)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm(tel_id, message.text, loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


@dp.message_handler(lambda message: message.text in mk.t)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm(tel_id, message.text, loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


@dp.message_handler(lambda message: message.text in mk.g)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm(tel_id, message.text, loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


@dp.message_handler(lambda message: message.text in mk.e)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm(tel_id, message.text, loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


@dp.message_handler(lambda message: message.text in mk.l)
async def loc_m(message):
    tel_id = message.chat.id
    await UsersDbManager.update_predm(tel_id, message.text, loop)
    text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    await UsersDbManager.update_context(tel_id, 'wait_files', loop)


'''
text = '<b>Прикрепите необходимые документы или фото</b> 📎\nПо окончанию нажмите Готово 👌'
    await bot.delete_message(tel_id, call.message.message_id)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena_plus, disable_notification=True, parse_mode='html')
    if str(await UsersDbManager.get_type(tel_id, loop)) == 'Online решение':
        text = '<i>Пришлите пример работы или подобные задания, которые вы выполняли.</i>'
        await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    #await UsersDbManager.update_context(tel_id, 'wait_files', loop)
    
    text = f'<b>Максимально подробно опишите задание</b> 🙃\n<i>Напишите тему, ваш вариант, уникальность, к-во страниц</i>'
    await UsersDbManager.update_context(tel_id, 'wait_info', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')
'''


@dp.message_handler(content_types=tp.ContentType.PHOTO)
async def sss1(message):
    tel_id = message.chat.id
    photo = None
    context = await UsersDbManager.get_context(tel_id, loop)
    ord_id = await UsersDbManager.get_ord_id(tel_id, loop)
    if context == 'wait_files':
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content

        await UsersDbManager.insert_ph_img_1(ord_id, pht, 'photto', loop)

        link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
        await UsersDbManager.update_links(ord_id, link, loop)

    elif context == 'online_work':
        ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
        author = await UsersDbManager.get_ord_auth(ord_id, loop)
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content
        await bot.send_photo(chat_id=author, photo=pht)

    elif context == 'wait_photo_opl':
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content
        num = await UsersDbManager.get_num(tel_id, loop)
        await ConfirmationOfOrders_bot.send_ph(num, pht)
        await UsersDbManager.update_context(tel_id, '', loop)

    elif context == 'wait_photo_opltwo':
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content
        num = await UsersDbManager.get_num(tel_id, loop)
        await ConfirmationOfOrders_bot.send_phtwo(num, pht)
        await UsersDbManager.update_context(tel_id, '', loop)


@dp.message_handler(content_types=tp.ContentType.DOCUMENT)
async def sss1(message):
    tel_id = message.chat.id
    doc = None
    context = await UsersDbManager.get_context(tel_id, loop)
    ord_id = await UsersDbManager.get_ord_id(tel_id, loop)
    if context == 'wait_files':
        doc = message.document.file_id
        file_info = await bot.get_file(doc)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content

        await UsersDbManager.insert_ph_img_1(ord_id, pht, message.document.file_name, loop)

        link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'

        await UsersDbManager.update_links(ord_id, link, loop)


    elif context == 'online_work':
        ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
        author = await UsersDbManager.get_ord_auth(ord_id, loop)
        doc = message.document.file_id
        file_info = await bot.get_file(doc)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        pht = file.content
        await bot.send_document(chat_id=author, document=pht)


@dp.message_handler(lambda message: message.text == 'Готово 👌')
async def loc_m(message):
    tel_id = message.chat.id
    text = '<b>Укажите дату сдачи работы</b> 📆'
    await bot.send_message(tel_id, text=text, reply_markup=mk.datekb(), disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == '❌ Пропустить отправку файлов')
async def loc_m(message):
    tel_id = message.chat.id
    text = '<b>Укажите дату сдачи работы</b> 📆'
    await bot.send_message(tel_id, text=text, reply_markup=mk.datekb(), disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message: message.text == '❌ Отменить оформление заказа ❌')
async def loc_m(message):
    tel_id = message.chat.id
    text = 'Меню'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True)
    await UsersDbManager.update_context(tel_id, '', loop)
    await UsersDbManager.delete_all(tel_id, loop)


monthes = {'1': '31', '2': '28', '3': '31', '4': '30', '5': '31',
           '6': '30',
           '7': '31', '8': '31', '9': '30', '10': '31', '11': '30',
           '12': '31'}


@dp.callback_query_handler(lambda c: c.data.startswith('datev_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])
    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])
    year = str(c.data[-4:])

    m = monthes.get(month)
    if day == m:
        if month == '12':
            month = 1
            year = int(year) + 1
        else:
            await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                                reply_markup=mk.date_2(day=str(int(1)), month=str(int(month) + 1),
                                                                       year=str(int(year))))
    else:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.date_2(day=str(int(day) + 1), month=str(int(month)),
                                                                   year=str(int(year))))


@dp.callback_query_handler(lambda c: c.data.startswith('mnthv_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])

    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])

    year = str(c.data[-4:])
    print('day: ', day, ' month: ', int(month) + 1, ' year: ', year)

    await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                        reply_markup=mk.date_2(day=str(int(day)), month=str(int(month) + 1),
                                                               year=str(int(year))))


@dp.callback_query_handler(lambda c: c.data.startswith('yearv_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])
    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])
    year = str(c.data[-4:])

    await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                        reply_markup=mk.date_2(day=str(int(day)), month=str(int(month)),
                                                               year=str(int(year) + 1)))


@dp.callback_query_handler(lambda c: c.data.startswith('daten_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])
    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])
    year = str(c.data[-4:])

    m = monthes.get(month)
    print(month)
    if int(day) == 1:
        if month == '1':
            month = '12'
            year = int(year) - 1
        else:
            await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                                reply_markup=mk.date_2(day=str(m), month=str(int(month) - 1),
                                                                       year=str(int(year))))
    else:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.date_2(day=str(int(day) - 1), month=str(int(month)),
                                                                   year=str(int(year))))


@dp.callback_query_handler(lambda c: c.data.startswith('mnthn_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])
    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])
    year = str(c.data[-4:])

    await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                        reply_markup=mk.date_2(day=str(int(day)), month=str(int(month) - 1),
                                                               year=str(int(year))))


@dp.callback_query_handler(lambda c: c.data.startswith('yearn_'))
async def process_call(c):
    tel_id = c.message.chat.id
    day = None
    month = None
    year = None
    if str(c.data[7]) == '!':
        day = str(c.data[6])
    elif str(c.data[7]) != '!':
        day = str(c.data[6]) + str(c.data[7])
    if str(c.data[7]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[8]) + str(c.data[9])
    elif str(c.data[8]) == '!' and str(c.data[11]) == '!':
        month = str(c.data[9]) + str(c.data[10])
    elif str(c.data[7]) == '!' and str(c.data[9]) == '!':
        month = str(c.data[8])
    elif str(c.data[8]) == '!' and str(c.data[10]) == '!':
        month = str(c.data[9])
    year = str(c.data[-4:])
    year = int(year) - 1

    curr_year = datetime.datetime.today().year

    if int(year) - 1 < int(curr_year):
        year = str(curr_year)

    try:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.date_2(day=str(int(day)), month=str(int(month)),
                                                                   year=str(int(year))))
    except:
        qwe = None


@dp.callback_query_handler(lambda c: c.data.startswith('podtv_'))
async def process_call(c):
    tel_id = c.message.chat.id
    date = str(c.data[5:])
    dot = date.find('.')
    if date[int(dot) + 1] == '1':
        date = date
    else:
        p = date[:-6]
        date_2 = '0' + date[dot + 1:]
        date = p + date_2
    await UsersDbManager.update_date(tel_id, date, loop)
    text = '<b>Укажите время сдачи</b> ⏰'
    await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                reply_markup=mk.timekb(tel_id, 2), parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('hourp_'))
async def process_call(c):
    tel_id = c.message.chat.id
    hour = None
    minutes = None

    if str(c.data[7]) == '!':
        hour = str(c.data[6])

    elif str(c.data[7]) != '!':
        hour = str(c.data[6]) + str(c.data[7])

    if str(c.data[8]) == '!':
        try:
            minutes = str(c.data[9]) + str(c.data[10])
        except:
            minutes = str(c.data[9])
    elif str(c.data[7]) == '!':
        try:
            minutes = str(c.data[8]) + str(c.data[9])
        except:
            minutes = str(c.data[8])

    if int(hour) + 1 >= 23:
        hour = 23
    else:
        hour = int(hour) + 1

    s = str(await UsersDbManager.get_type(tel_id, loop))
    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False
    time = UsersDbManager.get_time(tel_id)
    print('htime:', time)
    if time is None:
        print(None)
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=2,
                                                                     tel_id=tel_id))
    elif time is not None and s is True:
        text = 'Во сколько закончиться контроль?'
        await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                    reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=3,
                                                             tel_id=tel_id))


@dp.callback_query_handler(lambda c: c.data.startswith('minut_'))
async def process_call(c):
    tel_id = c.message.chat.id
    hour = None
    minutes = None

    if str(c.data[7]) == '!':
        hour = str(c.data[6])
    elif str(c.data[7]) != '!':
        hour = str(c.data[6]) + str(c.data[7])

    if str(c.data[8]) == '!':
        try:
            minutes = str(c.data[9]) + str(c.data[10])
        except:
            minutes = str(c.data[9])
    elif str(c.data[7]) == '!':
        try:
            minutes = str(c.data[8]) + str(c.data[9])
        except:
            minutes = str(c.data[8])

    if int(minutes) + 15 >= 60:
        minutes = (int(minutes) + 15) - 60
        if int(hour) + 1 >= 23:
            hour = 23
        else:
            hour = int(hour) + 1
    else:
        minutes = int(minutes) + 15

    s = str(await UsersDbManager.get_type(tel_id, loop))
    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False
    time = UsersDbManager.get_time(tel_id)
    if time is None:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=2,
                                                                     tel_id=tel_id))
    elif time is not None and s is True:
        text = 'Во сколько закончиться контроль?'
        await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                    reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=3,
                                                             tel_id=tel_id))


@dp.callback_query_handler(lambda c: c.data.startswith('hourm_'))
async def process_call(c):
    tel_id = c.message.chat.id
    hour = None
    minutes = None

    if str(c.data[7]) == '!':
        hour = str(c.data[6])

    elif str(c.data[7]) != '!':
        hour = str(c.data[6]) + str(c.data[7])

    if str(c.data[8]) == '!':
        try:
            minutes = str(c.data[9]) + str(c.data[10])
        except:
            minutes = str(c.data[9])
    elif str(c.data[7]) == '!':
        try:
            minutes = str(c.data[8]) + str(c.data[9])
        except:
            minutes = str(c.data[8])

    if int(hour) - 1 < 1:
        hour = 1
    else:
        hour = int(hour) - 1

    s = str(await UsersDbManager.get_type(tel_id, loop))
    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False
    time = UsersDbManager.get_time(tel_id)
    if time is None:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=2,
                                                                     tel_id=tel_id))
    elif time is not None and s is True:
        text = 'Во сколько закончиться контроль?'
        await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                    reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=3,
                                                             tel_id=tel_id))


@dp.callback_query_handler(lambda c: c.data.startswith('minum_'))
async def process_call(c):
    tel_id = c.message.chat.id
    hour = None
    minutes = None

    if str(c.data[7]) == '!':
        hour = str(c.data[6])
    elif str(c.data[7]) != '!':
        hour = str(c.data[6]) + str(c.data[7])

    if str(c.data[8]) == '!':
        try:
            minutes = str(c.data[9]) + str(c.data[10])
        except:
            minutes = str(c.data[9])
    elif str(c.data[7]) == '!':
        try:
            minutes = str(c.data[8]) + str(c.data[9])
        except:
            minutes = str(c.data[8])

    if int(minutes) - 15 < 0:
        minutes = (int(minutes) - 15)
        mint = int(minutes)
        minutes = 60 + int(mint)
        if int(hour) - 1 < 1:
            hour = 1
        else:
            hour = int(hour) - 1
    else:
        minutes = int(minutes) - 15

    s = str(await UsersDbManager.get_type(tel_id, loop))
    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False
    time = UsersDbManager.get_time(tel_id)
    t = UsersDbManager.get_time_t(tel_id)
    if time is None:
        await bot.edit_message_reply_markup(tel_id, c.message.message_id,
                                            reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=2,
                                                                     tel_id=tel_id))
    elif time is not None and s is True and t is False:
        text = 'Во сколько закончиться контроль?'
        await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                    reply_markup=mk.timekb_2(hour=str(hour), minutes=str(minutes), num=3,
                                                             tel_id=tel_id))


@dp.callback_query_handler(lambda c: c.data.startswith('podtv2_'))
async def process_call(c):
    tel_id = c.message.chat.id
    date = str(c.data[6:])
    print('podtv_2')
    await UsersDbManager.update_time(tel_id, date, loop)
    s = str(await UsersDbManager.get_type(tel_id, loop))
    if s == 'Online решение' or s == 'Тест дистанционно':
        s = True
    else:
        s = False
    t = UsersDbManager.get_time_t(tel_id)

    if s is True and t is False:
        text = '<b>Во сколько закончиться контроль?</b>'
        await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                    reply_markup=mk.timekb(num=3, tel_id=tel_id), parse_mode='html')
    else:
        await bot.delete_message(tel_id, c.message.message_id)
        text = f'<b>Максимально подробно опишите задание</b> 🙃\n<i>Напишите тему, ваш вариант, уникальность, к-во страниц</i>'
        await UsersDbManager.update_context(tel_id, 'wait_info', loop)
        await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('podtv3_'))
async def process_call(c):
    tel_id = c.message.chat.id
    date = str(c.data[6:])
    await UsersDbManager.update_end_contr(tel_id, date, loop)
    await bot.delete_message(tel_id, c.message.message_id)

    text = f'<b>Максимально подробно опишите задание</b> 🙃\n<i>Напишите тему, ваш вариант, уникальность, к-во страниц</i>'
    await UsersDbManager.update_context(tel_id, 'wait_info', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wait_info')
async def wait_name(message):
    tel_id = message.chat.id
    await UsersDbManager.update_info(tel_id, message.text, loop)
    text = '<b>Оформление в электронном виде или от руки?</b>\n\n<i>Чаще всего от руки дешевле, но не всегда</i> 😉'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otr(), disable_notification=True, parse_mode='html')


@dp.callback_query_handler(lambda call:
                           call.data.startswith('ruk'))
async def count_yes(call):
    tel_id = call.message.chat.id
    text = '<b>Пришлите цену за задание</b> 💸'
    text_2 = '<i>Если не можете оценить заказ нажмите ↓</i>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.dogov(), disable_notification=True, parse_mode='html')
    await UsersDbManager.update_oforml(tel_id, 'От руки', loop)
    await UsersDbManager.update_context(tel_id, 'wait_price', loop)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('elect'))
async def count_yes(call):
    tel_id = call.message.chat.id
    await UsersDbManager.update_oforml(tel_id, 'Электронный вид', loop)
    text = '<b>Пришлите цену за задание</b> 💸'
    text_2 = '<i>Если не можете оценить заказ нажмите ↓</i>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.dogov(), disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context(tel_id, 'wait_price', loop)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('ne_prcpl'))
async def count_yes(call):
    tel_id = call.message.chat.id
    await UsersDbManager.update_oforml(tel_id, 'Не принципиально', loop)
    text = '<b>Пришлите цену за задание</b> 💸'
    text_2 = '<i>Если не можете оценить заказ нажмите ↓</i>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otmena, disable_notification=True, parse_mode='html')
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.dogov(), disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context(tel_id, 'wait_price', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wait_price')
async def wait_name(message):
    tel_id = message.chat.id
    await UsersDbManager.update_price(tel_id, message.text, loop)
    await bot.delete_message(tel_id, message.message_id)
    text = 'Для завершения <i>нажмите</i> Готово 🙌'
    await bot.send_message(tel_id, text=text, reply_markup=mk.got(), disable_notification=True, parse_mode='html')
    await UsersDbManager.update_context(tel_id, '', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('dogov'))
async def process_call(c):
    tel_id = c.message.chat.id
    await UsersDbManager.update_price(tel_id, 'Договорная', loop)
    text = 'Для завершения <i>нажмите</i> Готово 🙌'
    await bot.edit_message_text(text=text, chat_id=tel_id, message_id=c.message.message_id,
                                reply_markup=mk.got(), parse_mode='html')


def detect_numbers(text):
    l = []
    phone_regex = re.compile(r"(\+380)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})")
    groups = phone_regex.findall(text)
    for g in groups:
        l.append(g)
    a = ''
    try:
        a = re.search("(?P<url>t.me?/[^\s]+)", text).group("url")
    except:
        a = ''
    if len(a) != 0:
        l.append(a)
    sob = text.find('@')
    if sob != -1:
        l.append(sob)
    return l


@dp.callback_query_handler(lambda c: c.data.startswith('got'))
async def process_call(c):
    tel_id = c.message.chat.id
    # await bot.delete_message(tel_id, c.message.message_id-1)
    order_info = await UsersDbManager.get_order(tel_id, loop)
    user_info = await UsersDbManager.get_user(tel_id, loop)
    n = detect_numbers(order_info[5])
    if len(n) > 0:
        await bot.send_message(tel_id, text='Пост был забракован ботом и отправлен на модерацию 😳',
                               reply_markup=mk.main_menu_ru)
    else:
        s = str(await UsersDbManager.get_type(tel_id, loop))
        if s == 'Online решение' or s == 'Тест дистанционно':
            s = True
        else:
            s = False
        if s is True:
            text = f'✨ Заказ №{order_info[0]} ✨\n\n' \
                   f'<b>{order_info[4]}</b>\n' \
                   f'<b>{order_info[2]}</b>\n\n' \
                   f'Срок сдачи: {order_info[7]}\n{order_info[8]}-{order_info[9]}\n' \
                   f'Цена: {order_info[10]}\n\n' \
                   f'Оформление: {order_info[6]}\n' \
                   f'Комментарий: {order_info[5]}' \
                   f'\n\nПрикрипленные файлы: '
            kb = tp.ReplyKeyboardRemove()
            await bot.delete_message(tel_id, c.message.message_id)
            await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True,
                                   parse_mode='html', )
            await send_files(tel_id, order_info[0])

            text = '<b>Постараемся как можно быстрее оценить ваш заказ</b> 🚀\n' \
                   '<i>Оцениваем в течении 2 часов. Вы оплачиваете предоплату и только после этого мы приступаем к работе.</i>\n' \
                   '<b>Есть вопросы или Вы хотите изменить заказ?</b> Отпишите менеджеру ⬇️'
            await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), disable_notification=True,
                                   parse_mode='html')
        else:
            text = f'✨ Заказ №{order_info[0]} ✨\n\n' \
                   f'<b>{order_info[4]}</b>\n' \
                   f'<b>{order_info[2]}</b>\n\n' \
                   f'Срок сдачи: {order_info[7]} {order_info[8]}\n' \
                   f'Цена: {order_info[10]}\n\n' \
                   f'Оформление: {order_info[6]}\n' \
                   f'Комментарий: {order_info[5]}' \
                   f'\n\nПрикрипленные файлы: '
            kb = tp.ReplyKeyboardRemove()
            await bot.delete_message(tel_id, c.message.message_id)
            await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True,
                                   parse_mode='html')
            await send_files(tel_id, order_info[0])

            text = '<b>Постараемся как можно быстрее оценить ваш заказ</b> 🚀\n' \
                   '<i>Оцениваем в течении 2 часов. Вы оплачиваете предоплату и только после этого мы приступаем к работе.</i>\n' \
                   '<b>Есть вопросы или Вы хотите изменить заказ?</b> Отпишите менеджеру ⬇️'
            await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), disable_notification=True,
                                   parse_mode='html')
    await UsersDbManager.update_context(tel_id, '', loop)
    await author_bot.send_new_order(order_info[0])


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


@dp.message_handler(lambda message: message.text == 'Мои заказы 🛒')
async def loc_m(message):
    tel_id = message.chat.id
    orders = await UsersDbManager.get_o_orders(tel_id, loop)
    active_ord = await UsersDbManager.get_act_orders(tel_id, loop)
    user_info = await UsersDbManager.get_user(tel_id, loop)

    if active_ord == False:
        if orders == False:
            text = 'Вы ещё ничего не заказывали 😁'
            await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True)
        else:
            for order in orders:
                text = f'✨ Заказ №{order[0]} ✨\n\n' \
                       f'<b>{order[4]}</b>\n' \
                       f'<b>{order[2]}</b>\n\n' \
                       f'Срок сдачи: {order[7]} {order[8]}\n' \
                       f'Цена: {order[10]}\n\n' \
                       f'Оформление: {order[6]}\n' \
                       f'Комментарий: {order[5]}' \
                       f'\n\nПрикрипленные файлы:'
                await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True,
                                       parse_mode='html')
                await send_files(tel_id, order[0])
    else:
        order_info = await UsersDbManager.get_order(tel_id, loop)
        text = f'✨ Заказ №{order_info[0]} ✨\n\n' \
               f'<b>{order_info[4]}</b>\n' \
               f'<b>{order_info[2]}</b>\n\n' \
               f'Срок сдачи: {order_info[7]} {order_info[8]}\n' \
               f'Цена: {order_info[10]}\n\n' \
               f'Оформление: {order_info[6]}\n' \
               f'Комментарий: {order_info[5]}' \
               f'\n\nПрикрипленные файлы: '
        await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True,
                               parse_mode='html')
        await send_files(tel_id, order_info[0])


@dp.message_handler(lambda message: message.text == 'Связь с менеджером 📱')
async def loc_m(message):
    tel_id = message.chat.id
    text = 'Выберите способ связи с менеджером ⬇️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.get_sv(), disable_notification=True)


@dp.callback_query_handler(lambda c: c.data.startswith('manager'))
async def process_call(c):
    tel_id = c.message.chat.id
    text = 'Выберите способ связи с менеджером ⬇️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.get_sv(), disable_notification=True)


@dp.callback_query_handler(lambda c: c.data.startswith('call_man'))
async def process_call(c):
    tel_id = c.message.chat.id
    text = '+380634690637'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True)


@dp.callback_query_handler(lambda c: c.data.startswith('textman'))
async def process_call(c):
    tel_id = c.message.chat.id
    text = 'В чат подключен менеджер 🚀'
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_manager, disable_notification=True)


@dp.message_handler(lambda message: message.text == '❌ Отменить связь с менеджером❌')
async def loc_m(message):
    tel_id = message.chat.id
    text = 'Менеджер покинул чат 👋\n\n❗️Бот не воспринимает никакие комментарии❗️ \n\nЕсли появились вопросы, свяжитесь с нами'
    await bot.send_message(tel_id, text=text,
                           reply_markup=mk.main_menu_ru, disable_notification=True)


async def send_time(tel_id):
    text = '<b>До онлайн работы осталось 20 мин.</b>\n' \
           'Не скидывайте в чат ничего до того момента, пока вы не подключите автора'
    await bot.send_message(tel_id, text=text, reply_markup=mk.online_kb(), parse_mode='html')


@dp.callback_query_handler(lambda c: c.data.startswith('get_author'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
    author = await UsersDbManager.get_ord_auth(ord_id, loop)
    text = '<b>В чат подключен автор</b> 🚀\n' \
           'Скиньте, пожалуйста, фото билета'
    await bot.send_message(tel_id, text=text, reply_markup=mk.author_otm, parse_mode='html')

    text_2 = '<b>Вы вошли в чат с заказчиком.</b>\n' \
             'Можете задавать уточняющие вопросы и когда работа будет закончена, можете покинуть чат.\n' \
             'Если появятся дополнительные задания, можете оценить заказ.'
    await bot.send_message(author, text=text_2, parse_mode='html', reply_markup=mk2.onl_2)
    await UsersDbManager.update_context_a(author, 'online_work', loop)
    await UsersDbManager.update_context(tel_id, 'online_work', loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'online_work')
async def wait_name(message):
    tel_id = message.chat.id
    ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
    author = await UsersDbManager.get_ord_auth(ord_id, loop)
    await bot.send_message(author, text=message.text)


@dp.callback_query_handler(lambda c: c.data.startswith('no_online'))
async def process_call(c):
    tel_id = c.message.chat.id
    text = 'Спасибо, что предупредили. Удачи!'
    text_2 = 'По любым вопросам пишите менеджеру⬇️'
    await bot.send_message(tel_id, text=text, reply_markup=mk.main_menu_ru, disable_notification=True)
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.send_man(), disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'context', loop)

    ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
    await UsersDbManager.delete_order(ord_id, loop)


@dp.message_handler(lambda message: message.text == 'Онлайн работа закончена  ❌')
async def loc_m(message):
    tel_id = message.chat.id
    ord_id = await UsersDbManager.get_ord_auth_2(tel_id, loop)
    author = await UsersDbManager.get_ord_auth(ord_id, loop)

    text = 'oko'
    await bot.send_message(tel_id, text=text)
    await UsersDbManager.update_context(tel_id, '', loop)

    await UsersDbManager.update_context_a(author, '', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('pay_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[3:]
    await UsersDbManager.add_num(tel_id, ord_id, loop)

    text = '<b>Оплатить можно:</b>\n' \
           '✔️ <b>Приватбанк</b> (Огинская Анна)\n' \
           '4149 6293 1543 9281\n\n' \
           'После оплаты отправьте скрин с оплатой заказа'
    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html', disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'wait_photo_opl', loop)

@dp.callback_query_handler(lambda c: c.data.startswith('payb_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[4:]
    cost = await UsersDbManager.update_and_get_cost(tel_id, ord_id, loop)
    await UsersDbManager.add_num(tel_id, ord_id, loop)
    text_0 = f'Вы добавили бонусы к оплате.\n' \
             f'Вам необходимо заплатить <i>{cost}</i> грн.'

    text = '<b>Оплатить можно:</b>\n' \
           '✔️ <b>Приватбанк</b> (Огинская Анна)\n' \
           '4149 6293 1543 9281\n\n' \
           'После оплаты отправьте скрин с оплатой заказа'
    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html', disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'wait_photo_opl', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('paytwo_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[6:]
    await UsersDbManager.add_num(tel_id, ord_id, loop)

    text = '<b>Оплатить можно:</b>\n' \
           '✔️ <b>Приватбанк</b> (Огинская Анна)\n' \
           '4149 6293 1543 9281\n\n' \
           'После оплаты отправьте скрин с оплатой заказа'
    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html', disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'wait_photo_opltwo', loop)


async def confirm_fifty(tel_id, ord_id, money):
    order_info = await UsersDbManager.get_priceo_order(ord_id, loop)
    text = f'<b>Мы получили предоплату в размере</b> 💵 <b>{money} грн</b> 💵 \n\n' \
           f'<b>по заказу №{ord_id}</b> 🚀\n' \
           f'<b>Тип работы: </b>{order_info[2]}\n' \
           f'<b>Предмет:</b> {order_info[4]}\n' \
           f'💵 <b>К оплате еще <i>{money}</i> грн</b> 💵'
    await bot.send_message(tel_id, text=text, reply_markup=mk.pay(ord_id[1:]), parse_mode='html')

    text_2 = f'<b>Специалист приступил к выполнению заказа №{ord_id[1:]}</b>🚀'
    await bot.send_message(tel_id, text=text_2, parse_mode='html')
    await UsersDbManager.active_o(ord_id[1:], money, loop)


async def confirm_fifty_2(tel_id, ord_id, money):
    order_info = await UsersDbManager.get_wait_order(ord_id, loop)
    ord_id = ord_id[1:]
    print(ord_id)
    print(order_info)
    text = f'<b>Мы получили оплату в размере</b> 💵 <b>{money} грн</b> 💵 \n\n' \
           f'<b>по заказу №{ord_id}</b> 🚀\n' \
           f'<b>Тип работы: </b>{order_info[2]}\n' \
           f'<b>Предмет:</b> {order_info[4]}\n'
    await bot.send_message(tel_id, text=text, reply_markup=mk.pay(ord_id), parse_mode='html')

    text_2 = f'🎊 <b>Ваша робота готова!</b> 🎊\n<b>Заказ №{ord_id}</b>'
    await bot.send_message(tel_id, text=text_2, parse_mode='html')
    links = await UsersDbManager.get_links(ord_id, loop)
    links = str(links)
    links = links.split(' , ')
    text_l = None
    for link in links:
        text_l += f'{link}\n\n'
    await bot.send_message(tel_id, text=text_l, parse_mode='html')

    text_3 = '❤️ Спасибо, что вы с Reshalla ❤️' \
             '\nЖелаем удачи со сдачей работы!' \
             '\nЕсть вопросы? 👇'
    await bot.send_message(tel_id, text=text_3, reply_markup=mk.manager(), parse_mode='html')

    text_4 = '<b>Насколько Вы довольны нашей работой?</b>\n' \
             'Выберите цифру от 1 до 5	🙌'
    await bot.send_message(tel_id, text=text_4, reply_markup=mk.otz(ord_id), parse_mode='html')
    await UsersDbManager.add_num(tel_id, ord_id, loop)


async def confirm_all(tel_id, ord_id, money):
    bonuses = int(money) / (100 * 1)
    order_info = await UsersDbManager.get_priceo_order(ord_id, loop)
    ord_id = ord_id[1:]
    text = f'<b>Мы получили оплату</b> 💵 <b>{money} грн</b> 💵 \n\n' \
           f'<b>по заказу №{ord_id}</b> 🚀\n' \
           f'<b>Тип работы: </b>{order_info[2]}\n' \
           f'<b>Предмет:</b> {order_info[4]}\n' \
           f'<b>Вам начислены бонусы в размере <i>{bonuses}</i> грн.</b>'

    await bot.send_message(tel_id, text=text, parse_mode='html')

    text_2 = f'<b>Специалист приступил к выполнению заказа №{ord_id}</b>🚀'
    await bot.send_message(tel_id, text=text_2, parse_mode='html')


async def dopl_yes(tel_id, ord_id, money):
    order_info = await UsersDbManager.get_wait_order(ord_id, loop)
    bonuses = int(money) / (100 * 1)

    text = f'<b>Мы получили оплату</b> 💵 <b>{money} грн</b> 💵 \n\n' \
           f'<b>по заказу №{ord_id}</b> 🚀\n' \
           f'<b>Тип работы: </b>{order_info[2]}\n' \
           f'<b>Предмет:</b> {order_info[4]}\n' \
           f'<b>Вам начислены бонусы в размере <i>{bonuses}</i> грн.</b>'
    await bot.send_message(tel_id, text=text, parse_mode='html')

    text_2 = f'🎊 <b>Ваша робота готова!</b> 🎊\n<b>Заказ №{ord_id}</b>'
    await bot.send_message(tel_id, text=text_2, parse_mode='html')
    links = await UsersDbManager.get_links(ord_id, loop)
    links = str(links)
    links = links.split(' , ')
    text_l = ''
    for link in links:
        text_l = str(text_l) +  str(f'{link}\n\n')
    await bot.send_message(tel_id, text=text_l, parse_mode='html')

    text_3 = '❤️ Спасибо, что вы с Reshalla ❤️' \
             '\nЖелаем удачи со сдачей работы!' \
             '\nЕсть вопросы? 👇'
    await bot.send_message(tel_id, text=text_3, reply_markup=mk.manager(), parse_mode='html')

    text_4 = '<b>Насколько Вы довольны нашей работой?</b>\n' \
             'Выберите цифру от 1 до 5	🙌'
    await bot.send_message(tel_id, text=text_4, reply_markup=mk.otz(ord_id), parse_mode='html')
    await UsersDbManager.add_num(tel_id, ord_id, loop)



@dp.callback_query_handler(lambda c: c.data.startswith('one_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[4:]
    text = '<b>Ваш выбор: 1</b>\n' \
           '<b>Нам очень важно Ваше мнение!</b>\n' \
           'Напишите, пожалуйста, отзыв 🙏'
    await UsersDbManager.update_context(tel_id, 'wait_com_ord', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz(), disable_notification=True, parse_mode='html')
    await UsersDbManager.doneo(ord_id, 1, loop)


@dp.callback_query_handler(lambda c: c.data.startswith('two_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[4:]
    text = '<b>Ваш выбор: 2</b>\n' \
           '<b>Нам очень важно Ваше мнение!</b>\n' \
           'Напишите, пожалуйста, отзыв 🙏'
    await UsersDbManager.update_context(tel_id, 'wait_com_ord', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz(), disable_notification=True, parse_mode='html')
    await UsersDbManager.doneo(ord_id, 2, loop)


@dp.callback_query_handler(lambda c: c.data.startswith('three_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[6:]
    text = '<b>Ваш выбор: 3</b>\n' \
           '<b>Нам очень важно Ваше мнение!</b>\n' \
           'Напишите, пожалуйста, отзыв 🙏'
    await UsersDbManager.update_context(tel_id, 'wait_com_ord', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz(), disable_notification=True, parse_mode='html')
    await UsersDbManager.doneo(ord_id, 3, loop)


@dp.callback_query_handler(lambda c: c.data.startswith('four_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[5:]
    text = '<b>Ваш выбор: 4</b>\n' \
           '<b>Нам очень важно Ваше мнение!</b>\n' \
           'Напишите, пожалуйста, отзыв 🙏'
    await UsersDbManager.update_context(tel_id, 'wait_com_ord', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz(), disable_notification=True, parse_mode='html')
    await UsersDbManager.doneo(ord_id, 4, loop)


@dp.callback_query_handler(lambda c: c.data.startswith('five_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[5:]
    text = '<b>Ваш выбор: 5</b>\n' \
           '<b>Нам очень важно Ваше мнение!</b>\n' \
           'Напишите, пожалуйста, отзыв 🙏'
    await UsersDbManager.update_context(tel_id, 'wait_com_ord', loop)
    await bot.send_message(tel_id, text=text, reply_markup=mk.otm_otz(), disable_notification=True, parse_mode='html')
    await UsersDbManager.doneo(ord_id, 5, loop)


@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wait_com_ord')
async def wait_name(message):
    tel_id = message.chat.id
    text = message.text
    ord_id = await UsersDbManager.get_num(tel_id, loop)
    await UsersDbManager.update_com(ord_id, text, loop)
    text_2 = 'Спасибо!'
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.main_menu_ru)
    await UsersDbManager.update_context(tel_id, '', loop)


@dp.callback_query_handler(lambda c: c.data.startswith('otm_otz'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = await UsersDbManager.get_num(tel_id, loop)
    await UsersDbManager.update_context(tel_id, '', loop)
    text_2 = 'Спасибо!'
    await bot.send_message(tel_id, text=text_2, reply_markup=mk.main_menu_ru)

@dp.callback_query_handler(lambda c: c.data.startswith('otmena_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[7:]
    text = '<b>Укажите, пожалуйста, причину</b>'
    await bot.send_message(tel_id, text=text, reply_markup=mk.why_otm(ord_id), parse_mode='html')

@dp.callback_query_handler(lambda c: c.data.startswith('exp_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[4:]
    text = '<b>Напишите, пожалуйста, цену, на которую вы рассчитываете</b>'
    await bot.send_message(tel_id, text=text, parse_mode='html')
    await UsersDbManager.otmo(ord_id, 'Дорого', loop)

@dp.callback_query_handler(lambda c: c.data.startswith('myself_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[7:]
    text = f'<b>Заказ №{ord_id} отменен 😢</b>\n' \
           f'Если вам нужна будет помощь, обязательно обращайтесь!\n' \
           f'По любым вопросам пишите менеджеру 📱'

    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html')
    await UsersDbManager.otmo(ord_id, 'Сделал сам', loop)

@dp.callback_query_handler(lambda c: c.data.startswith('other_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[6:]
    text = f'<b>Заказ №{ord_id} отменен 😢</b>\n' \
           f'Если вам нужна будет помощь, обязательно обращайтесь!\n' \
           f'По любым вопросам пишите менеджеру 📱'

    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html')
    await UsersDbManager.otmo(ord_id, 'Заказал у других людей', loop)

@dp.callback_query_handler(lambda c: c.data.startswith('another_'))
async def process_call(c):
    tel_id = c.message.chat.id
    ord_id = c.data[8:]
    text = f'<b>Заказ №{ord_id} отменен 😢</b>\n' \
           f'Если вам нужна будет помощь, обязательно обращайтесь!\n' \
           f'По любым вопросам пишите менеджеру 📱'

    await bot.send_message(tel_id, text=text, reply_markup=mk.manager(), parse_mode='html')
    await UsersDbManager.otmo(ord_id, 'Другое', loop)

@dp.message_handler(lambda message: message.text == 'Мои бонусы 💰')
async def loc_m(message):
    tel_id = message.chat.id
    bonuses = await UsersDbManager.get_bonuses(tel_id, loop)
    text = f'На ваше счету <i>{bonuses}</i> гривен.\n\n' \
           f'Вы можете использовать их при оплате заказа!'
    await bot.send_message(tel_id, text=text, disable_notification=True, parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

'''
    n = detect_numbers(order_info[5])
    if len(n) > 0:
        await bot.send_message(tel_id, text='Пост был забракован ботом и отправлен на модерацию 😳',
                               reply_markup=mk.main_menu_ru)
'''
