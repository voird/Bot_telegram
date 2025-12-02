import telebot
from telebot import types

TOKEN = '8295881899:AAGZ3IFDRKXMkPo9r814IfcgMmnZBdx0RJs'
ADMIN_ID = 1967263018  # твой Telegram ID

bot = telebot.TeleBot(TOKEN)

# временное хранилище анкет
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
        """ㅤㅤㅤㅤㅤДобро пожаловать в  Bureau of Utter Confusion!

ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤНаш канал (https://t.me/BureauofUtterConfusion)

Именно здесь, в боте, появляются новички, гости и те, кто нажал не туда, но всё ещё надеется, что попал по адресу.
Через этот раздел проходят все, кто хочет присоединиться к проекту, задать вопрос, пожаловаться на жизнь, систему или свой Wi-Fi… или просто прийти и потеряться в интерфейсе.
Перед тем как отправить свою форму, обязательно ознакомьтесь с сюжетом и правилами, чтобы потом не изображать удивление.

ㅤ""",
        reply_markup=markup
    )

# стартовое сообщение с кнопками
@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)

# обработка кнопок стартового меню
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "Правила и сюжет":
        bot.send_message(
            message.chat.id,
            """Правила (https://telegra.ph/Ustav-Arhiva-Glupyh-Oshibok-11-29)
            
Сюжет (https://telegra.ph/Syuzhet-BUC-11-29)ㅤ"""
        )
    elif message.text == "Касты крови":
        bot.send_message(
            message.chat.id,
            """Корпоративный гемоспектр (https://telegra.ph/KORPORATIVNYJ-GEMOSPEKTR-11-29)ㅤ"""
        )
    elif message.text == "Написать анкету":
        send_form_menu(message.chat.id)
        bot.register_next_step_handler(message, handle_form_step)

# функция для отправки формы с кнопкой "Назад в меню"
def send_form_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = types.KeyboardButton("Назад в меню")
    markup.add(back_btn)
    bot.send_message(
        chat_id,
        """Имя/Как к вам обращаться:

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

# обработка ввода анкеты
def handle_form_step(message):
    if message.text == "Назад в меню":
        send_main_menu(message.chat.id)
        return

    # иначе считаем, что это анкета
    user_id = message.from_user.id
    pending_forms[user_id] = message.text

    markup = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton("Подтвердить", callback_data=f"approve_{user_id}")
    reject_btn = types.InlineKeyboardButton("Отклонить", callback_data=f"reject_{user_id}")
    markup.add(approve_btn, reject_btn)

    bot.send_message(ADMIN_ID,
                     f"Новая анкета от {message.from_user.first_name}:\n\n{message.text}",
                     reply_markup=markup)
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
