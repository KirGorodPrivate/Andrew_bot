import telebot
import sqlite3
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot("702003056:AAH4yaUXRnFwwJL1iW5AQMpr9WhmoMkXKZQ")

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

try:
    cursor.execute("CREATE TABLE test(Photos text)")
except Exception as e:
    print(e)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_location(message.chat.id, "50.461694", "30.630710")
    # files = []
    # try:
    #     for i in range(9):
    #         f = open(f"C:/Users/Кирилл/PycharmProjects/untitled/photos/file_{i}.jpg", 'rb')
    #         media = f.read()
    #         media = InputMediaPhoto(media)
    #         files.append(media)
    #         print(files)
    # except Exception as e:
    #     print(e)
    #
    # bot.send_media_group(message.chat.id, files)
    # f.close()



@bot.message_handler(content_types=['location'])
def help(message):
    print(message.location)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    print(message.content_type)




bot.polling(none_stop=True)