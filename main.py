import telebot
import qrcode
import re
import random
import cv2
import sqlite3
import openpyxl
import xlsxwriter
import time
from constants import *
from buttons import *
from check_functions import *
from PIL import Image, ImageDraw, ImageFont
bot = telebot.TeleBot(apiKey)

db = sqlite3.connect(databaseName, check_same_thread=False)
cur = db.cursor()

temporaryDict = {}

# check functions


def resizePicture(current):
    image_path = current
    fixed_width = 300
    img = Image.open(image_path)
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[0]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    new_image.save(current)


def isRegistered(id):
    cur.execute(f"select firstname from {mainTable} where tID = \"{id}\";")
    lst = cur.fetchall()
    if len(lst) > 0:
        return True
    else:
        return False


def createTable(grade):
    cur.execute(
        f"select tID, firstname, lastname, status, photo from {mainTable} where status = \"обрабатывается\" "
        f"and grade = \"{grade}\"")
    data = cur.fetchall()
    wb = xlsxwriter.Workbook(path_xlsList + grade + ".xlsx")
    ws = wb.add_worksheet()

    format = wb.add_format()
    format.set_align('vcenter')
    format.set_align('center')

    ws.set_column("A2:A5", 20, format)
    ws.set_column("B2:B5", 20, format)
    ws.set_column("C2:C5", 20, format)
    ws.set_column("D2:D5", 20, format)
    ws.set_column("E2:E5", 25, format)
    ws.set_default_row(165)

    names = ['ID', "ИМЯ", "ФАМИЛИЯ", "СТАТУС", "ФОТО"]
    title_col = 0
    for i in names:
        ws.write(0, title_col, i)
        title_col += 1

    photos = []
    row = 1
    for human in range(len(data)):
        col = 0
        photos.append(data[human][4])
        for a in range(len(data[human]) - 1):
            ws.write(row, col, data[human][a])
            col += 1
        row += 1

    img_row = 1
    img_col = 4
    for image in photos:
        ws.insert_image(img_row,
                        img_col,
                        image,
                        {'x_scale': 0.5,
                         'y_scale': 0.5,
                         'x_offset': 5,
                         'y_offset': 5,
                         'positioning': 1})
        img_row += 1
    wb.close()


@bot.message_handler(commands=['start'])
def sendHello(message):
    tID = message.chat.id
    cur.execute(f"select tID from {mainTable}")
    data = cur.fetchall()
    if len(data) < participantsLimit:
        cur.execute(f"select * from {mainTable} where tID = \"{tID}\"")
        data = cur.fetchall()
        if len(data) == 0:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(button_1, button_2)
            bot.send_message(
                message.chat.id,
                helloMessage,
                reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(button_21)
            bot.send_message(
                tID,
                "Твоя заявка уже добавлена",
                reply_markup=markup)
    else:
        bot.send_message(tID, highLimitText)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        try:
            if call.data == "btn_1":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_23)
                bot.send_message(
                    call.message.chat.id,
                    attentionText,
                    parse_mode="Markdown",
                    reply_markup=markup)
            elif call.data == "btn_2":
                bot.send_message(call.message.chat.id, infoText)
            elif call.data == "btn_3":
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    temporaryDict[call.message.chat.id][2] = "10"
                    markup = types.InlineKeyboardMarkup(row_width=3)
                    markup.add(
                        button_5,
                        button_6,
                        button_7,
                        button_8,
                        button_9)
                    bot.send_message(
                        call.message.chat.id,
                        "Выбери букву класса",
                        reply_markup=markup)
                except BaseException:
                    bot.send_message(call.message.chat.id, errorMessage)
            elif call.data == "btn_4":
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    temporaryDict[call.message.chat.id][2] = "11"
                    markup = types.InlineKeyboardMarkup(row_width=3)
                    markup.add(
                        button_6,
                        button_10,
                        button_11,
                        button_12,
                        button_13,
                        button_14)
                    bot.send_message(
                        call.message.chat.id,
                        "Выбери букву класса",
                        reply_markup=markup)
                except BaseException:
                    bot.send_message(call.message.chat.id, errorMessage  + "2")

            elif call.data == "btn_5":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "А"
                checkInfo(call.message)
            elif call.data == "btn_6":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "Г"
                checkInfo(call.message)
            elif call.data == "btn_7":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "И"
                checkInfo(call.message)
            elif call.data == "btn_8":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "К"
                checkInfo(call.message)
            elif call.data == "btn_9":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "Л"
                checkInfo(call.message)
            elif call.data == "btn_10":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "М"
                checkInfo(call.message)
            elif call.data == "btn_11":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "В"
                checkInfo(call.message)
            elif call.data == "btn_12":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "С"
                checkInfo(call.message)
            elif call.data == "btn_13":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "П"
                checkInfo(call.message)
            elif call.data == "btn_14":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                temporaryDict[call.message.chat.id][3] = "Е"
                checkInfo(call.message)
            elif call.data == "btn_15":
                if temporaryDict[call.message.chat.id][0] != "" and temporaryDict[call.message.chat.id][1] != "":
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, sendPhotoText)
                    time.sleep(1)
                    bot.send_message(
                        call.message.chat.id,
                        "Пример хорошей фотографии:")
                    msg = bot.send_photo(
                        call.message.chat.id, open(
                            previewSource, 'rb'))
                    bot.register_next_step_handler(msg, recieve_photo)

            elif call.data == "btn_16":
                if temporaryDict[call.message.chat.id][0] != '':
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    markup.add(button_17, button_18)
                    bot.send_message(
                        call.message.chat.id,
                        "Какую информацию ты хочешь исправить?",
                        reply_markup=markup)
                else:
                    bot.send_message(call.message.chat.id, errorMessage)
            elif call.data == "btn_17":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                msg = bot.send_message(
                    call.message.chat.id,
                    "Введи имя и фамилию по новой"
                    "\nНапиши в формате Иван Иванов")
                bot.register_next_step_handler(msg, inputNameAgain)
            elif call.data == "btn_18":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(button_3, button_4)
                msg = bot.send_message(
                    call.message.chat.id,
                    "В каком классе ты учишься?",
                    reply_markup=markup)
            elif call.data == "btn_19":
                tID = call.message.chat.id
                cur.execute(
                    f"select * from {mainTable} where tID = \"{call.message.chat.id}\"")
                data = cur.fetchall()
                if data[0][6] != 'отклонена':
                    firstname = data[0][1]
                    lastname = data[0][2]
                    grade = data[0][3]
                    ticket = Image.open(ticketSource)
                    idraw = ImageDraw.Draw(ticket)
                    if len(firstname) > 10 or len(lastname) > 10:
                        font_size = 95
                    else:
                        font_size = 120
                    font = ImageFont.truetype("bent.ttf", size=font_size)
                    idraw.text((2000, 490), firstname, font=font)
                    idraw.text((2000, 610), lastname, font=font)
                    idraw.text((2000, 800), grade, font=font)
                    img = qrcode.make(str(tID))
                    img.save(path_userQRC + 'qrcode' + str(tID) + '.png')
                    watermark = Image.open(
                        path_userQRC + 'qrcode' + str(tID) + '.png')
                    ticket.paste(watermark, (2000, 1000), watermark)
                    ticket.save(path_userTicket + 'ticket' + str(tID) + '.png')
                    bot.send_message(
                        tID, "Тебе нужно показать билет при входе в гимназию")
                    bot.send_document(
                        tID,
                        open(
                            path_userTicket +
                            'ticket' +
                            str(tID) +
                            '.png',
                            'rb'))
                else:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    markup.add(button_20)
                    bot.send_message(
                        call.message.chat.id,
                        f"{data[0]['firstname']}, твой билет аннулирован, "
                        f"ты не можешь его скачать или воспользоваться "
                        f"уже скачаным",
                        reply_markup=markup)

            elif call.data == "btn_20":
                cur.execute(
                    f"select question from {mainTable} where tID = {call.message.chat.id}")
                data = cur.fetchall()
                if data[0][0] != 1:
                    msg = bot.send_message(
                        call.message.chat.id, "Задай свой вопрос")
                    bot.register_next_step_handler(msg, sendQuestion)
                else:
                    bot.send_message(
                        call.message.chat.id,
                        "Нельзя задавать больше одного вопроса, дождись ответа "
                        "на предыдущий")

            elif call.data == "btn_21":
                getStatus(call.message)
            elif call.data == "btn_22":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_22_2, button_22_1)
                bot.send_message(
                    call.message.chat.id,
                    "Ты точно хочешь удалить свою заявку?",
                    reply_markup=markup)

            elif call.data == "btn_23":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                msg = bot.send_message(call.message.chat.id, nameText)
                bot.register_next_step_handler(msg, inputName)

            elif call.data == "btn_24":
                cur.execute(
                    f"select * from {mainTable} where tID = \"{call.message.chat.id}\"")
                data = cur.fetchall()
                if len(data) == 0:
                    bot.send_message(call.message.chat.id, errorMessage)
                else:
                    tID = call.message.chat.id
                    cur.execute(
                        f"delete from {mainTable} where tID = \"{tID}\"")
                    db.commit()
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    markup.add(button_1)
                    bot.send_message(tID, removeText, reply_markup=markup)

            elif call.data == "btn_25":
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, "Действие отменено")
                time.sleep(2)
                getStatus(call.message)


        except Exception as e:
            bot.send_message(
                call.message.chat.id,
                errorMessage)


def check_face(tID):
    face_cascade_db = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml")
    img = cv2.imread(path_userPhoto + str(tID) + ".jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    if len(faces) == 0:
        return 0
    elif len(faces) == 1:
        return 1
    elif len(faces) > 1:
        return 2


def recieve_photo(message):
    tID = message.chat.id
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = path_userPhoto + str(tID) + '.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        temporaryDict[message.chat.id][4] = src
        isFaceOnPhoto = check_face(tID)
        if isFaceOnPhoto == 1:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(button_21, button_22)
            bot.send_message(tID, endRegistrationText, reply_markup=markup)

            sendData(message)
        elif isFaceOnPhoto == 2:
            msg = bot.send_message(
                tID, "Кажется на этой фотографии больше 1 лица, попробуй другую фотографию")
            bot.register_next_step_handler(msg, recieve_photo)
        elif isFaceOnPhoto == 0:
            msg = bot.send_message(
                tID, "Я не смог разглядеть тут тебя, попробуй другую фотографию")
            bot.register_next_step_handler(msg, recieve_photo)
        resizePicture(src)

    except Exception as e:
        msg = bot.send_message(tID, errorMessage + "\nОтравь свою фотографию")
        bot.register_next_step_handler(msg, recieve_photo)


def final(message):
    bot.send_message(message.chat.id, sendPhotoText)

    msg = bot.send_photo(message.chat.id, open(previewSource, 'rb'))
    bot.register_next_step_handler(msg, recieve_photo)


def inputNameAgain(message):
    try:
        tID = message.chat.id
        temporaryDict[tID][0] = ""
        temporaryDict[tID][1] = ""
        if checkInputName(message.text):
            temporaryDict[message.chat.id][0], temporaryDict[message.chat.id][1] = \
                message.text.split(" ")[0].title().replace("ё", "е").replace("Ё", "Е"), \
                message.text.split(" ")[1].title().replace("ё", "е").replace("Ё", "Е")
            msg = bot.send_message(message.chat.id, "Имя и фамилия исправлены")
            time.sleep(1)
            checkInfo(message)
        else:
            msg = bot.send_message(message.chat.id, errorMessage)
            bot.register_next_step_handler(msg, inputNameAgain)
    except BaseException:
        bot.send_message(message.chat.id, errorMessage)


def inputName(message):
    if checkInputName(message.text):
        tID = message.chat.id
        firstname, lastname = message.text.split(
            " ")[0].title(), message.text.split(" ")[1].title()
        temporaryDict[tID] = ["", "", "", "", ""]
        temporaryDict[tID][0] = firstname.replace("ё", "е").replace("Ё", "Е")
        temporaryDict[tID][1] = lastname.replace("ё", "е").replace("Ё", "Е")
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(button_3, button_4)
        msg = bot.send_message(
            tID,
            "В каком классе ты учишься?",
            reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, errorMessage + "\nТакого учащегося нет в школе")
        bot.register_next_step_handler(msg, inputName)


def checkInfo(message):
    tID = message.chat.id
    firstname = temporaryDict[tID][0]
    lastname = temporaryDict[tID][1]
    grade = temporaryDict[tID][2] + temporaryDict[tID][3]
    teacher = teachers[grade]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(button_15, button_16)
    bot.send_message(
        message.chat.id,
        f"Проверим информацию"
        f"\nИмя и фамилия: *{firstname} {lastname}*"
        f"\nКласс: *{grade}*"
        f"\nКлассный руководитель: *{teacher}*", parse_mode="Markdown")
    bot.send_message(message.chat.id, "Проверь правильность и выбери нужную кнопку", reply_markup = markup)


def sendData(message):
    tID = message.chat.id
    cur.execute(
        f"insert into {mainTable} (tID, firstname, lastname, grade, teacher, photo) "
        f"values (\"{str(tID)}\",\"{temporaryDict[tID][0]}\","
        f"\"{temporaryDict[tID][1]}\",\"{temporaryDict[tID][2]+temporaryDict[tID][3]}\","
        f"\"{teachers[temporaryDict[tID][2]+temporaryDict[tID][3]]}\","
        f"\"{temporaryDict[tID][4]}\")")
    db.commit()
    del temporaryDict[tID]


def sendQuestion(message):
    tID = message.chat.id
    try:
        cur.execute(f"update {mainTable} set question = 1 where tID = {tID}")
        db.commit()
        bot.send_message(
            tID, "Твой вопрос отправлен, и совсем скоро тебе придёт ответ")
        bot.send_message(adminID, f"Вопрос от {tID}:"
                         f"\n{message.text}")
    except BaseException:
        bot.send_message(tID, errorMessage)


@bot.message_handler(commands=["status"])
def getStatus(message):
    tID = message.chat.id
    cur.execute(f"select * from {mainTable} where tID = \"{tID}\"")
    data = cur.fetchall()
    try:
        if data == "()":
            bot.send_message(tID, errorMessage)
        else:

            firstname = data[0][1]
            status = data[0][6]
            if status == statuses[1]:
                bot.send_message(
                    tID,
                    f"{firstname}, текущий статус твоей заявки: *{status}*",
                    parse_mode="Markdown")
                bot.send_message(
                    tID, "Нужно ещё немного времени, чтобы обработать твою заявку")
            elif status == statuses[2]:
                bot.send_message(
                    tID,
                    f"{firstname}, текущий статус твоей заявки: *{status}*",
                    parse_mode="Markdown")
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_20)
                bot.send_message(
                    tID,
                    "К сожалению, ты не сможешь попасть на зимний бал."
                    "\nЕсли ты считаешь, что произошла ошибка, обратись в поддержку",
                    reply_markup=markup)

            elif status == statuses[0]:
                bot.send_message(
                    tID,
                    f"{firstname}, текущий статус твоей заявки: *{status}*",
                    parse_mode="Markdown")
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_22, button_19)
                bot.send_message(
                    tID, f"Ура, теперь нас станет на 1 больше! Ждём тебя *{partyData}*."
                    "\nДо встречи!", reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(tID, errorMessage)

@bot.message_handler(content_types=['text'])
def adminCommands(message):
    tID = message.chat.id
    if tID in volunteers:
        if re.match('/s', message.text) and len(message.text.split()) == 3:
            try:
                cur.execute(
                    f"update {mainTable} set status = \"{message.text.split()[2]}\" where tID = {message.text.split()[1]};")
                db.commit()
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_21)
                bot.send_message(
                    message.text.split()[1],
                    "Твой статус заявки изменился",
                    reply_markup=markup)
                bot.send_message(tID, "Статус участника изменён")
            except BaseException:
                bot.reply_to(tID, errorMessage)
        elif re.match('/r', message.text) and len(message.text.split()) > 2:
            bot.send_message(
                message.text.split()[1],
                f"Ответ на твой вопрос:"
                f"\n{' '.join(message.text.split()[2:])}")
            cur.execute(
                f"update {mainTable} set question = 0 where tID = {message.text.split()[1]}")
            db.commit()
            bot.send_message(tID, "сообщние отправлено")
        elif re.match('/all', message.text) and len(message.text.split()) > 2:
            try:
                cur.execute(f"select tID from {mainTable}")
                data = cur.fetchall()
                for i in range(len(data)):
                    if len(str(data[i][0])) > specialCount:
                        bot.send_message(
                            data[i][0], f"*Новое сообщение от администрации*"
                            f"\n{' '.join(message.text.split()[1:])}", parse_mode="Markdown")
                bot.send_message(tID, "сообщние отправлено")
            except Exception as e:
                bot.send_message(tID, errorMessage + f"\nОшибка: {e}" + "13")
        elif re.match('/h', message.text):
            bot.send_message(tID, helpText)

        elif re.match('/nsp', message.text) and len(message.text.split()) == 3:
            ID = random.randint(
                int("1" + "0" * (specialCount - 1)), int("9" * specialCount))
            cur.execute(
                f"insert into registration (tID, firstname, lastname, grade, status) "
                f"VALUES ({ID}, \"{message.text.split()[1]}\", \"{message.text.split()[2]}\","
                f"\"{specialName}\", \"одобрена\")")
            db.commit()
            bot.send_message(tID, f"Гость добавлен с ID {ID}")

        elif re.match('/table', message.text) and len(message.text.split()) == 2:
            if message.text.split()[1] in grades:
                createTable(message.text.split()[1])
                bot.send_document(
                    tID,
                    open(
                        path_xlsList +
                        message.text.split()[1] +
                        ".xlsx",
                        'rb'))
            else:
                bot.send_message(tID, "Такого класса нет")
        elif re.match('/allt', message.text):
            for grade in grades:
                createTable(grade)

                bot.send_document(
                    tID,
                    open(
                        path_xlsList +
                        grade +
                        ".xlsx",
                        'rb'))

    else:
        if re.match(
                '/special',
                message.text) and len(
                message.text.split()[1]) == specialCount:
            cur.execute(f"select firstname, lastname from "
                        f"{mainTable} where tID = \"{message.text.split()[1]}\"")
            data = cur.fetchall()
            firstname = data[0][0]
            lastname = data[0][1]
            grade = "SPECIAL"
            ticket = Image.open(ticketSource)
            idraw = ImageDraw.Draw(ticket)
            if len(firstname) > 10 or len(lastname) > 10:
                font_size = 95
            else:
                font_size = 120
            font = ImageFont.truetype("bent.ttf", size=font_size)
            idraw.text((2000, 490), firstname, font=font)
            idraw.text((2000, 610), lastname, font=font)
            idraw.text((2000, 800), grade, font=font)
            img = qrcode.make(str(message.text.split()[1]))
            img.save(
                path_userQRC +
                'qrcode' +
                message.text.split()[1] +
                '.png')
            watermark = Image.open(
                path_userQRC +
                'qrcode' +
                message.text.split()[1] +
                '.png')
            ticket.paste(watermark, (2000, 1000), watermark)
            ticket.save(
                path_userTicket +
                'ticket' +
                message.text.split()[1] +
                '.png')
            bot.send_message(
                tID,
                f"{firstname}, ты - наш специальный гость. Покажи этот билет при входе в гимназию")
            bot.send_document(
                tID,
                open(
                    path_userTicket +
                    'ticket' +
                    message.text.split()[1] +
                    '.png',
                    'rb'))


@bot.message_handler(content_types=['document'])
def upload(message):
    if message.chat.id in volunteers:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = path_xlsList + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "Таблица загружена")
            wb = openpyxl.reader.excel.load_workbook(src)
            wb.active = 0
            sheet = wb.active
            i = 2
            while True:
                if str(type(sheet[f'A{i}'].value)) == "<class 'NoneType'>":
                    break
                tID = sheet[f'A{i}'].value
                status = sheet[f'D{i}'].value
                cur.execute(
                    f"update registration set status = \"{str(status)}\" where tID = {tID}")
                db.commit()
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(button_21)
                bot.send_message(
                    tID,
                    "Твой статус заявки изменился",
                    reply_markup=markup)
                i += 1
        except BaseException:
            bot.send_message(message.chat.id, errorMessage)


@bot.message_handler(content_types=['photo'])
def checkReg(message):
    if message.chat.id in volunteers:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = path_userCheck + str(random.randint(123456, 999999 + 1)) + '.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        img = cv2.imread(src)
        detector = cv2.QRCodeDetector()
        data, bbox, clearQR = detector.detectAndDecode(img)
        try:
            cur.execute(f"select * from {mainTable} where tID = {data}")
            dataUser = cur.fetchall()
            if len(dataUser[0]) != 0:
                if dataUser[0][8] == 1:
                    isInto = "🚨 Билет был использован 🚨"
                else:
                    isInto = "✅ Билет используется в первый раз ✅"
                    cur.execute(
                        f"update {mainTable} set isInto = {1} where tID = {data}")
                    db.commit()
                bot.send_message(
                    message.chat.id,
                    f"Имя: {dataUser[0][1]} {dataUser[0][2]}"
                    f"\nКласс: {dataUser[0][3]}"
                    f"\nСтатус: {dataUser[0][6]}"
                    f"\n{isInto}")
                if dataUser[0][3] != specialName:
                    bot.send_photo(
                        message.chat.id,
                        open(
                            path_userPhoto +
                            f"{dataUser[0][0]}.jpg",
                            'rb'))
                    if dataUser[0][6] == 'одобрена' and isInto == "✅ Билет используется в первый раз ✅":
                        now = datetime.datetime.today()
                        d = partyTime - now
                        mm, ss = divmod(d.seconds, 60)
                        hh, mm = divmod(mm, 60)
                        bot.send_message(
                            data, enteredText.format(mm), parse_mode="Markdown")
            else:
                bot.send_message(
                    message.chat.id,
                    f"Билета с ID {data} не существует")
        except Exception as e:
            bot.send_message(adminID, errorMessage + f"\nОшибка: {e}" + "15")


bot.polling(non_stop=True)
