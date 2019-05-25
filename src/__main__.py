# TODO all
from bot import Bot

if __name__ == '__main__':
    token = '886563861:AAHBaV1huqzmOCOmrTmfuce39MA6OC0VD10'
    bot = Bot(token, threaded=False)

    bot.polling(none_stop=True)