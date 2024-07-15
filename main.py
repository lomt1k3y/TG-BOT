import telebot
import time
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

opt = Options()
opt.add_argument('--headless')
opt.add_argument('--no-sandbox')

opt.ignore_local_proxy_environment_variables()

access_token = "6647163420:AAGTzIqt7BEBrwTLG6ui9vW4WGa4cSeqsiI"
bot = telebot.TeleBot(access_token)

today = datetime.datetime.now().strftime('%d/%m/%Y')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! "
                          "Чем могу помочь?".format(
                         message.from_user), )


def listFilms(link):
    browser = webdriver.Chrome(opt)
    browser.get(link)
    nameFilm = browser.find_elements(By.CLASS_NAME, 'film-title')
    tables = browser.find_elements(By.CLASS_NAME, 'film-table')
    raiting = browser.find_elements(By.CLASS_NAME, 'appraisal__amount_kp')
    rait = []
    names = []
    links = []
    pushkin = []
    for i in range(len(nameFilm)):
        a = nameFilm[i].find_element(By.TAG_NAME, "a")
        names.append(a.text)
        links.append(a.get_attribute('href'))
        rait.append(raiting[i].text)

        pushCard = tables[i].find_elements(By.CLASS_NAME, 'pushka')

        if pushCard:
            pushkin.append("Да")
        else:
            pushkin.append("Нет")

    browser.close()
    browser.quit()
    return names, links, rait, pushkin


@bot.message_handler(commands=['mouth'])
def mainmouth(message):
    bot.send_message(message.chat.id, text="Готовлю список фильмов")
    names, links, rait, pushkin = listFilms('https://mayak-kino.ru/affiche/thismonth/')
    res = ""
    for i in range(len(names)):
        res += f"{i + 1}. <a href='{links[i]}'>{names[i]}</a> \n <b>Рейтинг Кинопоиска - {rait[i]}</b>\n <b>Можно оплатить пушкинской картой: {pushkin[i]} \n\n</b>"
    bot.send_message(message.chat.id, "Фильмы этого месяца:")
    bot.send_message(message.chat.id, res, parse_mode="HTML")


@bot.message_handler(commands=['today'])
def main(message):
    bot.send_message(message.chat.id, text="Это займет немного времени...")
    names, links, rait, pushkin = listFilms('https://mayak-kino.ru/affiche/')
    res = ""
    for i in range(len(names)):
        res += f"{i + 1}. <a href='{links[i]}'>{names[i]}</a> \n <b>Рейтинг Кинопоиска - {rait[i]}</b>\n <b>Можно оплатить пушкинской картой: {pushkin[i]} \n\n</b>"
    bot.send_message(message.chat.id, f"Cписок фильмов на {today}:")
    bot.send_message(message.chat.id, res, parse_mode="HTML")


if __name__ == '__main__':
    bot.polling(none_stop=True)
