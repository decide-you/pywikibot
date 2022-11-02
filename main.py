import telebot
import wikipedia
import sqlite3


bot = telebot.TeleBot('5705397083:AAG5XFQ0ZN_vNgsd2B1HgQSym7ouPSgBfSY')


def getwiki(msg, lang):
    wikipedia.set_lang(lang)
    try:
        wikipage = wikipedia.page(msg)
        wikicontent = wikipage.content
        finaltext = ''
        for x in wikicontent:
            if ('\n' in x):
                break
            else:
                finaltext = finaltext + x
        return finaltext

    except Exception as e:
        if lang == 'ru':
            return 'Введённое слово не найдено в базе данных википедии.'
        else:
            return 'The word entered was not found in the wikipedia database.'


@bot.message_handler(commands=['start'])
def start(message):

    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO 'lang' ('uid') VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rubot = telebot.types.KeyboardButton('🇷🇺RUSSIAN')
    engbot = telebot.types.KeyboardButton('🇺🇸ENGLISH(US)')

    markup.add(rubot, engbot)
    bot.send_message(message.chat.id, 'Select a languageВыберите язык', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def bot_menu_choose(message):
    if message.chat.type == 'private':
        conn = sqlite3.connect("base.db")
        cursor = conn.cursor()
        user_id = message.from_user.id
        if message.text == '🇷🇺RUSSIAN':
            bot.send_message(message.chat.id,
                             'Бот начал свою работу! Отправьте в чат слово, определение которого хотите узнать.', )

            cursor.execute("UPDATE lang SET value = ? WHERE uid = ?", (1, user_id))
            conn.commit()
            conn.close()

        elif message.text == '🇺🇸ENGLISH(US)':
            bot.send_message(message.chat.id,
                             'Bot has begun its work! Send to the chat the word whose definition you want to know.', )

            cursor.execute("UPDATE lang SET value = ? WHERE uid = ?", (2, user_id))
            conn.commit()
            conn.close()

        else:
            cursor.execute("SELECT value FROM lang WHERE uid = ?", (user_id,))
            result = cursor.fetchone()
            if result[0] == 1:
                lang = "ru"
            elif result[0] == 2:
                lang = "en"
            else:
                cursor.execute("INSERT OR IGNORE INTO 'lang' ('uid') VALUES (?)", (user_id,))
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, getwiki(message.text, lang))


bot.polling(none_stop=True)