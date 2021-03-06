import datetime

apiKey = "2126490165:AAH8gD6eC_ZHKexwkDkqF3jQ-guplu9-Rak"
adminID = -1001720096544
volunteers = [-1001720096544, ]
path_userPhoto = "D:/winter40bot/data/photos/"
path_userQRC = "D:/winter40bot/data/qrc/"
path_userTicket = 'D:/winter40bot/data/tickets/'
path_userCheck = 'D:/winter40bot/data/check/'
path_xlsList = 'D:/winter40bot/data/xls/'
previewSource = 'D:/winter40bot/data/preview_photo.jpg'
ticketSource = "D:/winter40bot/data/input_ticket.png"

# database

databaseName = "C:/Users/Lario/Рабочий стол/winter40_event/database.db"
mainTable = "registration"
queueTable = "queue"
participantsLimit = 300 # ограничение количества участников

specialCount = 4  # длина кода для гостей
specialName = "SPECIAL"  # класс для спец гостей
teachers = {

    # grade 10

    "10А": "Березина Людмила Леонтьевна",
    "10Г": "Шевцова Любовь Васильевна",
    "10И": "Аллахвердянц Гаянэ Эдуардовна",
    "10К": "Немченко Елена Владимировна",
    "10Л": "Савенкова Людмила Валерьевна",

    # grade 11

    "11П": "Ащева Снежанна Викторовна",
    "11В": "Кузьмина Лилия Владимировна",
    "11Г": "Джабиев Андрей Тофикович",
    "11М": "Буткевич Ирина Геннадьевна",
    "11С": "Трифонова Александра Евгеньевна",
    "11Е": "Отставных Евгения Анатольевна"}


# arrays

statuses = ['одобрена', 'обрабатывается', 'отклонена']
grades = ["10А", "10Г", "10И", "10К", "10Л", "11М",
          "11В", "11П", "11Г", "11С", "11Е"]

# messages

partyTime = datetime.datetime(2021, 12, 28, hour=17, minute=30)

partyData = "28 декабря с 17:00 до 20:30"

helloMessage = "Привет, этот бот поможет " \
               "тебе попасть на зиминий бал 2021!"

attentionText = "*ВНИМАНИЕ*\nДля того, чтобы попасть на бал, твой " \
                "родитель (или законный представитель) должен написать " \
                "сообщение классному руководителю о том, что он разрешает тебе " \
                "посетить массовое мероприятие." \
                "\n" \
                "\nСообщение от родителя (законного представителя) должно быть " \
                "отправлено не позже дня окончания сбора заявок" \
                "\n" \
                "\nЕсли сообщение не будет отправлено, заявка будет отклонена"

infoText = "Все подробности тут: https://clck.ru/Z5rB5"


nameText = "Как тебя зовут?" \
           "\nНапиши своё полное имя и фамилию (Иван Иванов)"

sendPhotoText = "Тебе осталсь отправить фотографию, " \
            "чтобы на ней было видно твоё лицо" \
            "\n" \
            "\nНа фотографии не должно быть лишних предметов, " \
            "лицо должно быть хорошо освещено и не повёрнуто в сторону"

errorMessage = "Что-то пошло не так, попробуй ещё раз☹"

endRegistrationText = "\nТвоя заявка отправлена на обработку🥳" \
                  "\nЗа несколько дней до бала ты получишь уведомление"

removeText = "Твоя заявка удалена" \
             "\nЕсли передумаешь, то нажми кноку ниже"

highLimitText = "К сожалению, на бал подало заявку максимальное " \
            "количество участников"

enteredText = "Приветствуем тебя на зимнем балу 2021!" \
              "\nВсё начнётся в киноконцертном зале *\"Галактика\"* через {} минут(ы)"
# adminHelp
helpText = "/s <ID> <отклонена, одобрена, обрабатывается>" \
           "\n/r <ID> <ответ на сообщение>" \
           "\n/all <текст сообщения для всех>" \
           "\n/nsp <Имя> <Фамилия> специального гостя" \
           "\n/table <КЛАСС> - таблица на выборку" \
           "\n/allt - все таблицы сразу по классам"

