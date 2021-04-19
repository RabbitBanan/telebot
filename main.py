from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

import random
import nltk
import csv

TG_TOKEN = '1671525688:AAGUlmd3zXvI_hJE_5-GXWyxoYeEZirXS3g'
BOT_CONFIG = {}


def csv_reader(file_obj):
    dc = {'intents': {}, 'failure_phrases': ['Извените, я всего лишь робот, поэтому не все понимаю.']}

    # print(dc['intents'])
    reader = csv.DictReader(file_obj, delimiter=";")
    for row in reader:
        # print(row['num'])
        intent = 'question_' + str(row['num'])
        if intent not in dc['intents']:
            dc['intents'][intent] = {
                'examples': [],
                'responses': []
            }
        dc['intents'][intent]['examples'].append(row['question'])
        dc['intents'][intent]['responses'].append(row['answer'])
    return dc

#NLP
def clear_phrase(phrase):
    phrase = phrase.lower()
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet)
    return result


def classify_intent(replica):
    replica = clear_phrase(replica)
    distances = []
    intents = []
    for intent, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            example = clear_phrase(example)
            # Растояние Левештейна
            distance = nltk.edit_distance(replica, example)
            # print(intent, distance / len(example))
            if example and distance / len(example) < 0.4:
                distances.append(str(distance / len(example)))
                intents.append(intent)
    if distances:
        return intents[distances.index(str(min(distances)))]

def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        responses = BOT_CONFIG['intents'][intent]['responses']
        return random.choice(responses)

def get_failure_phrase():
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


def NLPbot(replica):
    # NLU
    intent = classify_intent(replica)
    # выбор заготовленной реплики
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer
    # берем заглушку
    return get_failure_phrase()


def do_start(bot:Bot, update:Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Hello World',
    )

def do_echo(bot:Bot, update:Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=NLPbot(update.message.text),
    )

def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    path = "База знаний.csv"
    with open(path, "r") as f_obj:
        BOT_CONFIG = csv_reader(f_obj)
    main()