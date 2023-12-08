import telebot
import spacy

bot = telebot.TeleBot("6868602618:AAG5jSFLgC0nLUY96TndRe7-DkHBfRMXlis")


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