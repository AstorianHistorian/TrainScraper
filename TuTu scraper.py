#TuTu scraper
from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime

from telegram import update
import Constants as keys
from telegram.ext import *
import Responses as R




s1 = "Зеленоград - Москва"
s2 = "Зеленоград - Химки"
s3 = "Москва - Зеленоград"
s4 = "Химки - Зеленоград"
"""
print("Добрый день!")
print("Какие электрички вы хотите посмотреть?")
print('1. '+s1)
print('2. '+s2)
print('3. '+s3)
print('4. '+s4)
el = input()
"""


def start_command(update, context):
    update.message.reply_text("""
    Укажите по какому направлению вы хотите получить информацию.

1.Зеленоград - Москва
2.Зеленоград - Химки
3.Москва - Зеленоград
4.Химки - Зеленоград
Для вызова помощи нажмите  /help
Для повтора нажмите  /start""")

def help_command(update, context):
    update.message.reply_text("Введите число для выбора направления")

def exit_command(update, context):
    quit()
    

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    if (response == '1' or response == '2' or response == '3' or response == '4'):
        Get_trains(update,response)
    else:
        update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("exit",exit_command))

    dp.add_handler(MessageHandler(Filters.text,handle_message))

    dp.add_error_handler(error)

    updater.start_polling(5)
    updater.idle()

def Get_trains(update,el='1'):
    now = datetime.now()
    current_time=now.strftime("%H:%M")
    dst = ''
    if el == '1':
        response = requests.get("https://www.tutu.ru/rasp.php?st1=80710&st2=79310")
        dst = s1
    elif el == '2':
        response = requests.get("https://www.tutu.ru/rasp.php?st1=80710&st2=80010")
        dst = s2
    elif el == '3':
        response = requests.get("https://www.tutu.ru/rasp.php?st1=79310&st2=80710")
        dst = s3
    elif el == '4':
        response = requests.get("https://www.tutu.ru/rasp.php?st1=80010&st2=80710")
        dst = s4
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("tr")
    count = 5
    type = ""
    msg = f"Список ближайших электричек по направлению {dst}: \n"
    msg += "  Отб.     Приб.       Тип       Цена    В пути \n"
    for table in tables:
        if count == 0:
            update.message.reply_text(msg)
            break
        dep = table.find(class_="g-link desktop__depTimeLink__1NA_N")
        arr = table.find(class_="g-link desktop__arrTimeLink__2TJxM")
        range = table.find(class_="t-txt-s desktop__cell__2cdVW desktop__range__1Kbxz")
        price = table.find(class_="t-txt-s desktop__cell__2cdVW desktop__price__31Jsd")
        traintype = table.get_text()
        if (dep == None or arr == None):
            continue
        if "Ласточка" in traintype:
            type = "Ласточка"
        elif "Комфорт" in traintype:
            type = "Комфорт "
        else:
            type = "Обычная "
        price = price.get_text()
        if price == "":
            price = "225 ₽"
        if str(current_time) < dep.get_text():
            msg+= dep.get_text()+"   "+(arr.get_text().replace('(14 путь)',""))+"   "+type+"   "+price+"   "+range.get_text()+"\n"
            count-=1


main()