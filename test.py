import telebot
from selenium import webdriver
from telebot import types
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

opt = Options()
opt.ignore_local_proxy_environment_variables()
access_token = "6647163420:AAGTzIqt7BEBrwTLG6ui9vW4WGa4cSeqsiI"
bot = telebot.TeleBot(access_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! "
                          "Я тестовый бот который умеет показывать расписание фильмов!".format(
                         message.from_user), )


def listFilms():
    browser = webdriver.Chrome(opt)
    browser.get('https://mayak-kino.ru/affiche/')
    nameFilm = browser.find_elements(By.CLASS_NAME, 'film-title')
    tables = browser.find_elements(By.CLASS_NAME, 'film-table')
    raiting = browser.find_elements(By.CLASS_NAME, 'appraisal__amount_kp')
    filmtime = []
    rait = []
    names = []
    links = []
    pushkin = []
    for i in range(len(nameFilm)):
        a = nameFilm[i].find_element(By.TAG_NAME, "a")
        names.append(a.text)
        links.append(a.get_attribute('href'))
        rait.append(raiting[i].text)
        timeF = tables[i].find_elements(By.XPATH,
                                        '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[9]/td[2]')
        filmtime.append(timeF[i].text)

        pushCard = tables[i].find_elements(By.CLASS_NAME, 'pushka')

        if pushCard:
            pushkin.append("Можно оплатить ")
        else:
            pushkin.append("Нельзя оплатить")

    browser.close()
    browser.quit()
    return names, links, rait, pushkin, filmtime


# def get_page(date=''):
#     url = f"https://mayak-kino.ru/"
#     if date != '':
#         url += f"?date={date}"
#     response = requests.get(url)
#     web_page = response.text
#
#     return web_page
#
# def get_films(web_page):
#     soup = BeautifulSoup(web_page, "html.parser")
#     films = soup.find("ul", attrs={"class": "now"})
#     films_one = films.find_all("li", attrs={"class": "now-item"})
#     print(films_one)
#
@bot.message_handler(commands=['today'])
def main(message):
    bot.send_message(message.chat.id, text="Это займет немного времени...")
    names, links, rait, pushkin, filmtime = listFilms()
    res = ""
    for i in range(len(names)):
        res += f"{i + 1}. <a href='{links[i]}'>{names[i]}</a> \n <b>Рейтинг Кинопоиска - {rait[i]}</b>\n <b>Пушкинская карта: {pushkin[i]} \n\n {filmtime[i]}\n\n</b>"
    bot.send_message(message.chat.id, "Cписок фильмов на сегодня:")
    bot.send_message(message.chat.id, res, parse_mode="HTML")


if __name__ == '__main__':
    bot.polling(none_stop=True)
