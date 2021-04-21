# _*_ coding: utf-8 _*_
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import requests



TG_TOKEN = '1671525688:AAGUlmd3zXvI_hJE_5-GXWyxoYeEZirXS3g'


def do_echo(bot:Bot, update:Update):
    responce = requests.get('http://127.0.0.1:5000/message',
                            params={'text': update.message.text})
    try:
        text = str(responce.json()['Answer'])
        bot.send_message(
            chat_id=update.message.chat_id,
            text=text,
        )
    except:
        return 0


def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )
    #start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)

    #updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
