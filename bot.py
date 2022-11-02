import wikipedia
import telebot

from db import dbbot
from config import BOT_TOKEN, DB_NAME
dbbot = dbbot(DB_NAME)
dbbot.table_create()

bot = telebot.TeleBot(BOT_TOKEN)

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

    if(not dbbot.user_exists(message.from_user.id)):
        dbbot.add_user(message.from_user.id)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rubot = telebot.types.KeyboardButton('🇷🇺RUSSIAN')
    engbot = telebot.types.KeyboardButton('🇺🇸ENGLISH(US)')

    markup.add(rubot, engbot)
    bot.send_message(message.chat.id, 'Select a languageВыберите язык', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def bot_menu_choose(message):
    if(not dbbot.user_exists(message.from_user.id)):
        dbbot.add_user(message.from_user.id)

    if message.chat.type == 'private':
        if message.text == '🇷🇺RUSSIAN':
            bot.send_message(message.chat.id,
                     'Бот начал свою работу! Отправьте в чат слово, определение которого хотите узнать.', )
            dbbot.change_user_lang(message.from_user.id, "ru")
            

        elif message.text == '🇺🇸ENGLISH(US)':
            bot.send_message(message.chat.id,
                     'Bot has begun its work! Send to the chat the word whose definition you want to know.', )
            dbbot.change_user_lang(message.from_user.id, "en")

        else:
            ulang = dbbot.get_user_lang(message.from_user.id)
            bot.send_message(message.chat.id, getwiki(message.text, ulang))

bot.polling(none_stop=True)