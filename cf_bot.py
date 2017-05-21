# -*- coding: utf-8 -*-
import logging, telebot, flask, config, vk_api, sys, random
from telebot import types
from datetime import date
from config import WEBHOOK_SSL_CERT, WEBHOOK_URL_BASE, WEBHOOK_URL_PATH, WEBHOOK_SSL_PRIV, WEBHOOK_PORT, WEBHOOK_LISTEN

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)
app = flask.Flask(__name__)
vk_token = ''
bot = telebot.TeleBot(config.token)

stickers = ['CAADAgAD9AADk9JTDMvT_TgNxVkFAg',
            'AADAgADxAADk9JTDEQUTmw7BRbBAg',
            'CAADAgADwwADk9JTDHq6O5LjyZfaAg',
            'CAADAgADywADk9JTDCn6OHGpSv08Ag']


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.send_message(m.chat.id, "Чтобы узнать актуальную тренировку "
                                "на сегодня жми <b>'Тренировка'</b>"
                                "\nДля получения дополнительной информации жми  <b>'Инфо'</b>",
                     reply_markup=markup(), parse_mode='HTML')


@bot.message_handler(commands=['price'])
def send_price(m):
    photo = open('/Users/vladov/dev/cf/images/price.jpg', 'rb')
    bot.send_photo(m.chat.id, photo, reply_markup=markup())


@bot.message_handler(commands=['schedule'])
def send_price(m):
    photo = open('/Users/vladov/dev/cf/images/schedule.jpg', 'rb')
    bot.send_photo(m.chat.id, photo, reply_markup=markup())


@bot.message_handler(func=lambda message: message.text == 'Тренировка')
def send_welcome(m):
    today = date.today().strftime("%d.%m.%Y")
    train = vk_api.get_train(today)
    bot.send_message(m.chat.id, train, reply_markup=markup(), parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'Инфо')
def send_welcome(m):
    _markup = types.ReplyKeyboardMarkup()
    _markup.row('Тренировка')
    info = "• введите дату в формате <b>дд.мм.гггг</b> для получения тренировки за определенный день" \
           "\n• для получения актуальной тренировки жми <b>'Тренировка'</b>\n" \
           "• /schedule - расписание\n" \
           "• /price - цена абонементов"
    bot.send_message(m.chat.id, info, reply_markup=_markup, parse_mode='HTML')


@bot.message_handler(regexp='(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d')
def send_by_date(m):
    train = vk_api.get_train(m.text)
    bot.send_message(m.chat.id, train, reply_markup=markup(), parse_mode='HTML')


@bot.message_handler(func=lambda message: True, content_types=['sticker'])
def default_test(m):
    bot.send_sticker(m.chat.id, random.choice(stickers))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_test(m):
    bot.send_sticker(m.chat.id, random.choice(stickers))


def markup():
    common_markup = types.ReplyKeyboardMarkup()
    common_markup.row('Тренировка', 'Инфо')
    return common_markup


# if __name__ == '__main__':
#     bot.polling(none_stop=True)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)
