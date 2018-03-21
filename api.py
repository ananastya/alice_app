# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
# Импортируем подмодули Flask для запуска веб-сервиса.
from random import randint

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
questions = [{"country": "Соединенные Штаты Америки", "capital": "Вашингтон"},
             {"country": "Япония", "capital": "Токио"}, {"country": "Великобритания", "capital": "Лондон"},
             {"country": "Германия", "capital": "Берлин"}, {"country": "Нидерланды", "capital": "Амстердам"},
             {"country": "Франция", "capital": "Париж"}, {"country": "Италия", "capital": "Рим"},
             {"country": "Люксембург", "capital": "Люксембург"}, {"country": "Испания", "capital": "Мадрид"},
             {"country": "Швейцария", "capital": "Берн"}, {"country": "Австралия", "capital": "Канберра"},
             {"country": "Бельгия", "capital": "Брюссель"}, {"country": "Канада", "capital": "Оттава"},
             {"country": "Сингапур", "capital": "Сингапур"}, {"country": "Швеция", "capital": "Стокгольм"},
             {"country": "Австрия", "capital": "Вена"}, {"country": "Китай", "capital": "Пекин"},
             {"country": "Норвегия", "capital": "Осло"}, {"country": "Финляндия", "capital": "Хельсинки"},
             {"country": "Дания", "capital": "Копенгаген"}, {"country": "Греция", "capital": "Афины"},
             {"country": "Россия", "capital": "Москва"}, {"country": "Португалия", "capital": "Лиссабон"},
             {"country": "Бразилия", "capital": "Бразилиа"}, {"country": "Северная Корея", "capital": "Пхеньян"},
             {"country": "Индия", "capital": "Нью-Дели"}, {"country": "Польша", "capital": "Варшава"},
             {"country": "Турция", "capital": "Анкара"}, {"country": "Мексика", "capital": "Мехико"},
             {"country": "Индонезия", "capital": "Джакарта"}, {"country": "Венгрия", "capital": "Будапешт"},
             {"country": "Объединенные Арабские Эмираты", "capital": "Абу-Даби"},
             {"country": "Казахстан", "capital": "Астана"}, {"country": "Саудовская Аравия", "capital": "Эр-Рияд"},
             {"country": "Катар", "capital": "Доха"}, {"country": "Южно-Африканская Республика", "capital": "Претория"},
             {"country": "Румыния", "capital": "Бухарест"}, {"country": "Украина", "capital": "Киев"},
             {"country": "Чили", "capital": "Сантьяго"}, {"country": "Аргентина", "capital": "Буэнос-Айрес"},
             {"country": "Чехия", "capital": "Прага"}, {"country": "Исландия", "capital": "Рейкьявик"},
             {"country": "Малайзия", "capital": "Куала-Лумпур"}, {"country": "Израиль", "capital": "Иерусалим"},
             {"country": "Кипр", "capital": "Никосия"}, {"country": "Таиланд", "capital": "Бангкок"},
             {"country": "Колумбия", "capital": "Санта-Фе-де-Богота"},
             {"country": "Новая Зеландия", "capital": "Веллингтон"}, {"country": "Венесуэла", "capital": "Каракас"},
             {"country": "Филиппины", "capital": "Манила"}, {"country": "Словакия", "capital": "Братислава"},
             {"country": "Вьетнам", "capital": "Ханой"}, {"country": "Пакистан", "capital": "Исламабад"},
             {"country": "Хорватия", "capital": "Загреб"}, {"country": "Ирак", "capital": "Багдад"},
             {"country": "Словения", "capital": "Любляна"}, {"country": "Перу", "capital": "Лима"},
             {"country": "Египет", "capital": "Каир"}, {"country": "Мальта", "capital": "Валлетта"},
             {"country": "Судан", "capital": "Хартум"}, {"country": "Латвия", "capital": "Рига"},
             {"country": "Белоруссия", "capital": "Минск"}, {"country": "Болгария", "capital": "София"},
             {"country": "Марокко", "capital": "Рабат"}, {"country": "Кувейт", "capital": "Эль-Кувейт"},
             {"country": "Бангладеш", "capital": "Дакка"}, {"country": "Литва", "capital": "Вильнюс"},
             {"country": "Сербия", "capital": "Белград"}, {"country": "Бахрейн", "capital": "Манама"},
             {"country": "Шри-Ланка", "capital": "Коломбо"}, {"country": "Тунис", "capital": "Тунис"},
             {"country": "Эстония", "capital": "Таллин"}, {"country": "Ливан", "capital": "Бейрут"},
             {"country": "Куба", "capital": "Гавана"}, {"country": "Ангола", "capital": "Луанда"},
             {"country": "Иордания", "capital": "Амман"}, {"country": "Эквадор", "capital": "Кито"},
             {"country": "Доминиканская Республика", "capital": "Санто-Доминго"},
             {"country": "Гватемала", "capital": "Гватемала"}, {"country": "Уругвай", "capital": "Монтевидео"},
             {"country": "Нигерия", "capital": "Абуджа"}, {"country": "Иран", "capital": "Тегеран"},
             {"country": "Панама", "capital": "Панама"}, {"country": "Коста-Рика", "capital": "Сан-Хосе"},
             {"country": "Гана", "capital": "Аккра"}, {"country": "Сальвадор", "capital": "Сан-Сальвадор"},
             {"country": "Грузия", "capital": "Тбилиси"}, {"country": "Танзания", "capital": "Додома"},
             {"country": "Ямайка", "capital": "Кингстон"}, {"country": "Новая Гвинея", "capital": "Порт-Морсби"},
             {"country": "Эфиопия", "capital": "Аддис-Абеба"}, {"country": "Кения", "capital": "Найроби"},
             {"country": "Босния и Герцеговина", "capital": "Сараево"}, {"country": "Оман", "capital": "Маскат"},
             {"country": "Кот-д’Ивуар", "capital": "Ямусукро"},
             {"country": "Демократическая Республика Конго", "capital": "Киншаса"},
             {"country": "Армения", "capital": "Ереван"}, {"country": "Сирия", "capital": "Дамаск"},
             {"country": "Мьянма", "capital": "Найпьидо"}, {"country": "Ливия", "capital": "Триполи"},
             {"country": "Йемен", "capital": "Сана"}, {"country": "Азербайджан", "capital": "Баку"},
             {"country": "Зимбабве", "capital": "Хараре"}, {"country": "Македония", "capital": "Скопье"},
             {"country": "Боливия", "capital": "Сукре"}, {"country": "Республика Конго", "capital": "Браззавиль"},
             {"country": "Туркмения", "capital": "Ашхабад"}, {"country": "Никарагуа", "capital": "Манагуа"},
             {"country": "Маврикий", "capital": "Порт-Луи"}, {"country": "Непал", "capital": "Катманду"},
             {"country": "Мозамбик", "capital": "Мапуту"}, {"country": "Камбоджа", "capital": "Пномпень"},
             {"country": "Молдавия", "capital": "Кишинев"}, {"country": "Узбекистан", "capital": "Ташкент"},
             {"country": "Киргизия", "capital": "Бишкек"}, {"country": "Алжир", "capital": "Алжир"},
             {"country": "Гондурас", "capital": "Тегусигальпа"}, {"country": "Замбия", "capital": "Лусака"},
             {"country": "Парагвай", "capital": "Асунсьон"}, {"country": "Либерия", "capital": "Монровия"},
             {"country": "Лаос", "capital": "Вьентьян"}, {"country": "Гвинея", "capital": "Конакри"},
             {"country": "Габон", "capital": "Либревиль"}, {"country": "Сомали", "capital": "Могадишо"},
             {"country": "Южная Корея", "capital": "Сеул"}, {"country": "Камерун", "capital": "Яунде"},
             {"country": "Мали", "capital": "Бамако"}, {"country": "Сенегал", "capital": "Дакар"},
             {"country": "Афганистан", "capital": "Кабул"}, {"country": "Таджикистан", "capital": "Душанбе"},
             {"country": "Нигер", "capital": "Ниамей"}, {"country": "Тринидад и Тобаго", "capital": "Порт-оф-Спейн"},
             {"country": "Мадагаскар", "capital": "Антананариву"}, {"country": "Уганда", "capital": "Кампала"},
             {"country": "Монголия", "capital": "Улан-Батор"}, {"country": "Буркина-Фасо", "capital": "Уагадугу"},
             {"country": "Ботсвана", "capital": "Габороне"}, {"country": "Сьерра-Леоне", "capital": "Фритаун"},
             {"country": "Чад", "capital": "Нджамена"}, {"country": "Албания", "capital": "Тирана"},
             {"country": "Сейшельские Острова", "capital": "Виктория"}, {"country": "Бенин", "capital": "Порто-Ново"},
             {"country": "Бурунди", "capital": "Бужумбура"}, {"country": "Намибия", "capital": "Виндхук"},
             {"country": "Центрально-Африканская Республика", "capital": "Банги"},
             {"country": "Малави", "capital": "Лилонгве"}, {"country": "Белиз", "capital": "Бельмопан"},
             {"country": "Гвинея-Бисау", "capital": "Бисау"}, {"country": "Бутан", "capital": "Тхимпху"},
             {"country": "Гайана", "capital": "Джорджтаун"}, {"country": "Барбадос", "capital": "Бриджтаун"},
             {"country": "Черногория", "capital": "Подгорица"}, {"country": "Гамбия", "capital": "Банжул"},
             {"country": "Мальдивы", "capital": "Мале"}, {"country": "Лесото", "capital": "Масеру"},
             {"country": "Свазиленд", "capital": "Мбабане"}, {"country": "Суринам", "capital": "Парамарибо"},
             {"country": "Джибути", "capital": "Джибути"}, {"country": "Гаити", "capital": "Порт-о-Пренс"},
             {"country": "Антигуа и Барбуда", "capital": "Сент-Джонс"},
             {"country": "Гренада", "capital": "Сент-Джорджес"}, {"country": "Кабо-Верде", "capital": "Прая"},
             {"country": "Сан-Томе и Принсипи", "capital": "Сан-Томе"},
             {"country": "Сент-Китс и Невис", "capital": "Бастер"}, {"country": "Эритрея", "capital": "Асмэра"},
             {"country": "Сент-Люсия", "capital": "Кастри"}, {"country": "Коморы", "capital": "Морони"},
             {"country": "Сент-Винсент и Гренадины", "capital": "Кингстаун"},
             {"country": "Доминика", "capital": "Розо"}, {"country": "Самоа", "capital": "Апиа"},
             {"country": "Экваториальная Гвинея", "capital": "Малабо"},
             {"country": "Соломоновы Острова", "capital": "Хониара"}, {"country": "Фиджи", "capital": "Сува"},
             {"country": "Маршалловы Острова", "capital": "Маджуро"}, {"country": "Вануату", "capital": "Порт-Вила"},
             {"country": "Тонга", "capital": "Нукуалофа"},
             {"country": "Федеративные Штаты Микронезии", "capital": "Паликир"},
             {"country": "Науру", "capital": "официальной столицы не имеет"},
             {"country": "Кирибати", "capital": "Южная Тарава"},
             {"country": "Бруней", "capital": "Бандар-Сери-Багаван"}, {"country": "Палау", "capital": "Мелекеок"}]


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ],
            'questions': questions[:10]
        }
        q_index = randint(0, 9)
        sessionStorage[user_id]['wait_answer'] = sessionStorage[user_id]['questions'][q_index]
        del sessionStorage[user_id]['questions'][q_index]

        res['response']['text'] = sessionStorage[user_id]['wait_answer'].country
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() == sessionStorage[user_id]['wait_answer']['capital'].lower():
        # Пользователь согласился, прощаемся.
        if len(sessionStorage[user_id]['questions']) > 0:
            q_index = randint(0, len(sessionStorage[user_id]['questions']))
            sessionStorage[user_id]['wait_answer'] = sessionStorage[user_id]['questions'][q_index]
            del sessionStorage[user_id]['questions'][q_index]
            res['response']['text'] = 'Верно! ' + sessionStorage[user_id]['wait_answer'].country
            return
        res['response']['text'] = 'Молодец, вопросов больше не имею! '
        return

    # Если нет, то убеждаем его купить слона!
    if len(sessionStorage[user_id]['questions']) > 0:
        wait_answer = sessionStorage[user_id]['wait_answer']
        q_index = randint(0, len(sessionStorage[user_id]['questions']))
        sessionStorage[user_id]['wait_answer'] = sessionStorage[user_id]['questions'][q_index]
        del sessionStorage[user_id]['questions'][q_index]
        sessionStorage[user_id]['questions'].append(wait_answer)
        res['response']['text'] = 'Неверно, попробуем еще раз' + sessionStorage[user_id]['wait_answer'].country
        res['response']['buttons'] = getSuggests(user_id)
        return
    res['response']['text'] = 'Неверно, но вопросов больше нет'

# Функция возвращает две подсказки для ответа.
def getSuggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests
