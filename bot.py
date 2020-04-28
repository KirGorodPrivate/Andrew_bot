import sqlite3
import telebot
import os
from telebot import types
from datetime import datetime
import time

bot = telebot.TeleBot("702003056:AAH4yaUXRnFwwJL1iW5AQMpr9WhmoMkXKZQ")

conn = sqlite3.connect("tasks.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

data = []
# Создание таблицы
try:
    cursor.execute("""CREATE TABLE tasks
                      (TaskID int, CreatorID text, CreatorName text, TaskName text, ExecutorID text, ExecutorName text,
                       Description text, CreatingDate text, StartingDate datetime, EndDate text, TaskStatus text, Photos text)
                   """)
except Exception as e:
    print(e)



@bot.message_handler(commands=['register'])
def register(message):
    pass

@bot.message_handler(commands=['start'])
def start(message):
    key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    key.row("Создать задачу", "Посмотреть доступные задачи")
    key.row("Мои задачи")
    send = bot.send_message(message.from_user.id, "Начало работы", reply_markup=key)
    bot.register_next_step_handler(send, second)
    time.sleep(1)
    print(type(message.from_user.id))


def second(message):
    if message.text == "Создать задачу":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Назначить", "Исполнитель я")
        keyboard.row("Назад в главное меню")
        send = bot.send_message(message.from_user.id, "Вы будете исполнителем или назначить другого?", reply_markup=keyboard)
        bot.register_next_step_handler(send, create_task)
        time.sleep(1)
    elif message.text == "Мои задачи":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Завершить задачу", "Отменить задачу")
        keyboard.row("Назад в главное меню")

        conn = sqlite3.connect("tasks.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        ExecutorID = str(message.from_user.id)

        cursor.execute("SELECT TaskID FROM tasks WHERE ExecutorID = ?", (ExecutorID,))
        fetchTaskID = cursor.fetchall()
        cursor.execute("SELECT TaskName FROM tasks WHERE ExecutorID = ?", (ExecutorID,))
        fetchTaskname = cursor.fetchall()
        cursor.execute("SELECT Description FROM tasks WHERE ExecutorID = ?", (ExecutorID,))
        fetchDescription = cursor.fetchall()
        cursor.execute("SELECT StartingDate FROM tasks WhERE ExecutorID = ?", (ExecutorID,))
        fetchStartingDate = cursor.fetchall()
        cursor.execute("SELECT TaskStatus FROM tasks WHERE ExecutorID = ?", (ExecutorID,))
        fetchTaskStatus = cursor.fetchall()

        TaskID = [];
        TaskName = [];
        Description = [];
        StartingDate = [];
        TaskStatus = [];

        for i in fetchTaskID:
            TaskID.append(i[0])
        for i in fetchDescription:
            Description.append(i[0])
        for i in fetchStartingDate:
            StartingDate.append(i[0])
        for i in fetchTaskname:
            TaskName.append(i[0])
        for i in fetchTaskStatus:
            TaskStatus.append(i[0])

        print(TaskStatus)

        for i in range(len(TaskID)):
            msg = f"""#{TaskID[i]} - {TaskName[i]}\n{Description[i]}\nДата принятия: {StartingDate[i]}\nСтатус: {TaskStatus[i]}"""
            bot.send_message(message.chat.id, msg)

        time.sleep(1.3)
        send = bot.send_message(message.from_user.id, "Выберете действие:", reply_markup=keyboard)
        bot.register_next_step_handler(send, my_tasks)


    elif message.text == "Посмотреть доступные задачи":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row("Взять в работу")
        keyboard.row("Назад в главное меню")

        send = bot.send_message(message.from_user.id, "Список задач:", reply_markup=keyboard)

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT TaskID FROM tasks ORDER BY TaskID")
        fetchTaskID = cursor.fetchall()
        cursor.execute("SELECT TaskName FROM tasks ORDER BY TaskID")
        fetchTaskName = cursor.fetchall()
        cursor.execute("SELECT Description FROM tasks ORDER BY TaskID")
        if __name__ == '__main__':
            fetchDescription = cursor.fetchall()
        a = []
        b = []
        c = []
        for i in fetchTaskID:
            a.append(i[0])
        for i in fetchTaskName:
            b.append(i[0])
        for i in fetchDescription:
            c.append(i[0])

        for i in range(len(a)):
            print(str(a[i]) + " - " + str(b[i]))
            bot.send_message(message.chat.id, "#" + str(a[i]) + " - " + str(b[i]) + ": " + str(c[i]))



        bot.register_next_step_handler(send, view_task)
        time.sleep(1)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")


def my_tasks(message):
    if message.text == "Завершить задачу":
        send = bot.send_message(message.from_user.id, "Напишите номер задачи, которую хотите завершить:")
        bot.register_next_step_handler(send, finish_task)
    elif message.text == "Отменить задачу":
        send = bot.send_message(message.from_user.id, "Напишите номер задачи, которую хотите отменить:")
        bot.register_next_step_handler(send, cancel_task)


    elif message.text == "Назад в главное меню":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")


def finish_task(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row("Назад в главное меню")

    EndDate = datetime.now()
    TaskID = message.text
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET TaskStatus = 'Finished' WHERE TaskID = ?", (TaskID,))
    cursor.execute("UPDATE tasks SET EndDate = ? WHERE TaskID = ?", (EndDate,TaskID,))
    conn.commit()

    send = bot.send_message(message.from_user.id, f"Задача #{TaskID} завершена!", reply_markup=keyboard)
    bot.register_next_step_handler(send, fourth)

def cancel_task(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row("Назад в главное меню")

    TaskID = message.text
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET TaskStatus = 'Canceled' WHERE TaskID = ?", (TaskID,))
    conn.commit()

    send = bot.send_message(message.from_user.id, f"Задача #{TaskID} отменена!", reply_markup=keyboard)
    bot.register_next_step_handler(send, fourth)


def create_task(message):
    if message.text == "Назначить":
        bot.send_message(message.chat.id, "Функция в разработке!")
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    elif message.text == "Исполнитель я":
        send = bot.send_message(message.from_user.id, "Введите название задачи:", reply_markup=None)
        bot.register_next_step_handler(send, third)
        time.sleep(1)
    elif message.text == "Назад в главное меню":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")


def third(message):
        print("Massage: ", message)
        CreatorName = str(message.from_user.username)
        CreatorID = str(message.from_user.id)
        TaskName = str(message.text)
        ExecutorID = str(message.from_user.id)
        ExecutorName = str(message.from_user.username)
        send = bot.send_message(message.from_user.id, "Введите описание задачи: ")
        bot.register_next_step_handler(send, TaskDescription)
        time.sleep(1)
        a = []

        conn = sqlite3.connect("tasks.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()

        for row in cursor.execute('SELECT TaskID from tasks'):
            a.append(row)
            print(row)

        a.sort()
        if a == []:
            TaskID = 0
        else:
            a = a[-1]
            a = a[0]
            TaskID = int(a)+1
            a = []

        data.append(TaskID)
        data.append(CreatorID)
        data.append(CreatorName)
        data.append(TaskName)
        data.append(ExecutorID)
        data.append(ExecutorName)

        # conn = sqlite3.connect("tasks.db")
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO tasks(CreatorID, TaskName, ExecutorID) VALUES(?,?,?)", (CreatorID, TaskName, ExecutorID))
        # conn.commit()


def TaskDescription(message):
    if message.edit_date == None:
        key = telebot.types.ReplyKeyboardMarkup(True, True)
        key.row("В меню")
        Description = str(message.text)
        print("Описание", Description)
        send = bot.send_message(message.from_user.id, "Задача добавлена.", reply_markup=key)
        bot.register_next_step_handler(send, start)
        time.sleep(1)
        now = datetime.now()
        current_date = str(now.date())
        current_time = str(now.time())
        CreatingDate = f"{current_date} {current_time}"


        data.append(Description)
        data.append(CreatingDate)
        data.append("Waiting")

        print(data)

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks(TaskID, CreatorID, CreatorName, TaskName, ExecutorID, ExecutorName, Description, CreatingDate, TaskStatus) VALUES(?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
        data.clear()

    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")


def view_task(message):
    if message.text == "Взять в работу":
        send = bot.send_message(message.from_user.id, "Выберете задачу, написав её номер:")


        bot.register_next_step_handler(send, choose_task)
        time.sleep(1)
    elif message.text == "Назад в главное меню":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")

def choose_task(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row("Добавить фото", "Добавить коментарий")
    keyboard.row("Добавить координаты",)
    keyboard.row("Назад в главное меню")

    global GlobalTaskID
    GlobalTaskID = message.text
    choosen = GlobalTaskID
    print("Choosen task: " + choosen)
    bot.reply_to(message, "Вы выбрали задачу под номером " + choosen)

    now = datetime.now()
    current_date = str(now.date())
    current_time = str(now.time())
    StartingDate = f"{current_date} {current_time}"
    ExecutorID = message.from_user.id
    ExecutorName = message.from_user.username
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET ExecutorID = ? WHERE TaskID = ?", (ExecutorID, choosen))
    cursor.execute("UPDATE tasks SET ExecutorName = ? WHERE TaskID = ?", (ExecutorName, choosen))
    cursor.execute("UPDATE tasks SET StartingDate = ? WHERE TaskID = ?", (StartingDate, choosen))
    conn.commit()

    send = bot.send_message(message.from_user.id, "Выберете действие", reply_markup=keyboard)
    bot.register_next_step_handler(send, fourth)
    time.sleep(1)

def fourth(message):
    if message.text == "Назад в главное меню":
        print("123")
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    elif message.text == "Добавить фото":
        send = bot.send_message(message.from_user.id, "Добавьте фото")
        bot.register_next_step_handler(send, add_photo)
        time.sleep(1)
    elif message.text == "Добавить коментарий":
        bot.send_message(message.chat.id, "Функция в разработке!")
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    elif message.text == "Добавить координаты":
        bot.send_message(message.chat.id, "Функция в разработке!")
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Создать задачу", "Посмотреть доступные задачи")
        key.row("Мои задачи")
        send = bot.send_message(message.from_user.id, "Начало работы.", reply_markup=key)
        bot.register_next_step_handler(send, second)
        time.sleep(1)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так...\nНапишите /start")

@bot.message_handler(content_types=['photo', 'text'])
def add_photo(message):
    if message.content_type == "photo":
        try:

            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            print("File info: ",file_info)
            downloaded_file = bot.download_file(file_info.file_path)
            print("Donwloaded file:",downloaded_file)
            Photos = file_info.file_path
            Photos = Photos.split("/")[1]

            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Photos FROM tasks WHERE TaskID = ?", GlobalTaskID,)
            PhotosFetch = cursor.fetchall()
            PhotosFetch = PhotosFetch[0][0]
            if PhotosFetch == None:
                PhotosFetch = ""
            print("PhotosFetch: ", PhotosFetch)
            cursor.execute("UPDATE tasks SET Photos = ? WHERE TaskID = ?", (PhotosFetch, GlobalTaskID,))
            conn.commit()

            src = 'C:/Users/Кирилл/PycharmProjects/untitled/' + file_info.file_path;
            print("src:", src)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, "Фото добавлено")


        except Exception as e:
            bot.reply_to(message, e)
    elif message.content_type == "text":
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        key.row("Назад в главное меню")
        send = bot.send_message(message, "Начало работы", reply_markup=key)
        bot.register_next_step_handler(send, create_task)





if __name__ == "__main__":
    bot.polling(none_stop=True)