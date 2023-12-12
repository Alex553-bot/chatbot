from dotenv import load_dotenv
import os

import telebot
#import spacy

load_dotenv()
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
print(TELEGRAM_TOKEN)

bot = telebot.TeleBot("")


#PARA PROBAR SI HAY RESPUESTA
#commands
@bot.message_handler(commands=["help","start"])

def enviar(message):
    bot.reply_to(message, "Hola, ¿como estas?")


@bot.message_handler(func=lambda message:True)

def mensaje(message):
    bot.reply_to(message, message.text)
##
bot.polling()