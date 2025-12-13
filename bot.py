import telebot 
from telebot import types

TOKEN = '8295881899:AAGZ3IFDRKXMkPo9r814IfcgMmnZBdx0RJs'
ADMIN_ID = 1967263018  # твой Telegram ID

bot = telebot.TeleBot(TOKEN)
pending_forms = {}

# функция для отправки главного меню
def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rules_btn = types.KeyboardButton("Правила и сюжет")
    blood_btn = types.KeyboardButton("Касты крови")
    form_btn = types.KeyboardButton("Написать анкету")
    markup.add(rules_btn, blood_btn, form_btn)

    bot.send_message(
        chat_id,
        """ㅤДобро пожаловать в Bureau of Utter Confusion!

Наш канал: https://t.me/BureauofUtterConfusion

Здесь появляются новички, гости и те, кто нажал не туда, но всё ещё надеется, что попал по адресу.
Перед тем как отправить свою форму, ознакомьтесь с сюжетом и правилами.""",

Именно здесь, в боте, появляются новички, гости и те, кто нажал не туда, но всё ещё надеется, что попал по адресу.
Через этот раздел проходят все, кто хочет присоединиться к проекту, задать вопрос, пожаловаться на жизнь, систему или свой Wi-Fi… или просто прийти и потеряться в интерфейсе.
Перед тем как отправить свою форму, обязательно ознакомьтесь с сюжетом и правилами, чтобы потом не изображать удивление.

Если у вас есть вопрос технических (по поводу бота) или вопрос по проекту писать лидеру  @mifanohitra

ㅤ""",

        reply_markup=markup
    )

# стартовое сообщение с кнопкой "Старт"
@bot.message_handler(commands=['start'])
def start(message):
    # создаём inline-кнопку "Старт"
    markup = types.InlineKeyboardMarkup()
    start_btn = types.InlineKeyboardButton("Старт", callback_data="start_main")
    markup.add(start_btn)

    bot.send_message(
        message.chat.id,
        "Привет! Нажми кнопку ниже, чтобы начать:",
        reply_markup=markup
    )

# обработка нажатий inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "start_main":
        send_main_menu(call.message.chat.id)

    # обработка кнопок одобрения/отклонения анкеты
    elif call.data.startswith("approve_") or call.data.startswith("reject_"):
        action, user_id_str = call.data.split("_")
        user_id = int(user_id_str)

        if action == "approve":
            bot.send_message(user_id, "Ваша анкета одобрена! https://t.me/+wTLz-jPwlEQyY2Qy флуд: https://t.me/+0AaH8TdGSu0xMzEy")
            bot.edit_message_text("Анкета одобрена",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif action == "reject":
            bot.send_message(user_id, "Ваша анкета отклонена.")
            bot.edit_message_text("Анкета отклонена",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        pending_forms.pop(user_id, None)

# остальная логика меню и анкеты остаётся прежней
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "Правила и сюжет":
        bot.send_message(message.chat.id, "Правила (https://telegra.ph/Ustav-Arhiva-Glupyh-Oshibok-11-29)\nСюжет (https://telegra.ph/Syuzhet-BUC-11-29)")
    elif message.text == "Касты крови":
        bot.send_message(message.chat.id, "Корпоративный гемоспектр (https://telegra.ph/KORPORATIVNYJ-GEMOSPEKTR-11-29)")
    elif message.text == "Написать анкету":
        send_form_menu(message.chat.id)
        bot.register_next_step_handler(message, handle_form_step)

def send_form_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = types.KeyboardButton("Назад в меню")
    markup.add(back_btn)
    bot.send_message(chat_id, "Введите анкету...", reply_markup=markup)

def handle_form_step(message):
    if message.text == "Назад в меню":
        send_main_menu(message.chat.id)
        return

Возраст:
(Минимум 13 лет)

Участвовали ли вы ранее в RP-проектах?

Да / Нет
Если да, укажите, в каких:

Согласны ли вы создать нового персонажа или адаптировать своего персонажа под каноны проекта?

- Создам нового

- Адаптирую своего

Введите код из правил проекта:
(Код нужен для подтверждения, что вы ознакомились с правилами)

Что вы будете делать, если увидите нашу форму у не участника проекта?

Как вы отреагируете на агрессию в сторону незнакомых людей при наборе/сборе?
(Напишите, как обычно действуете в конфликтных ситуациях)

Отправь анкету одним сообщением.""",
        reply_markup=markup
    )

def handle_form_step(message):

    user_id = message.from_user.id
    username = message.from_user.username
    first = message.from_user.first_name

    pending_forms[user_id] = message.text

    # inline-кнопки для админа
    markup = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton("Подтвердить", callback_data=f"approve_{user_id}")
    reject_btn = types.InlineKeyboardButton("Отклонить", callback_data=f"reject_{user_id}")
    markup.add(approve_btn, reject_btn)

    # отправка админу с username
    bot.send_message(
        ADMIN_ID,
        f"Новая анкета от {first} (@{username}):\n\n{message.text}",
        reply_markup=markup
    )

    bot.send_message(message.chat.id, "Анкета отправлена на проверку!")


# обработка кнопок одобрения/отклонения
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    action, user_id_str = call.data.split("_")
    user_id = int(user_id_str)

    if action == "approve":
        bot.send_message(user_id, "Ваша анкета одобрена! https://t.me/+wTLz-jPwlEQyY2Qy флуд: https://t.me/+0AaH8TdGSu0xMzEy")
        bot.edit_message_text("Анкета одобрена",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif action == "reject":
        bot.send_message(user_id, "Ваша анкета отклонена.")
        bot.edit_message_text("Анкета отклонена",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    pending_forms.pop(user_id, None)

bot.infinity_polling()
