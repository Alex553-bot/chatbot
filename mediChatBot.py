from telegram import Bot
from telegram.ext import Updater

# Reemplaza 'TOKEN_AQUI' con el token de tu bot
TOKEN = '6868602618:AAG5jSFLgC0nLUY96TndRe7-DkHBfRMXlis'

# Crea una instancia de la clase Bot
mi_bot = Bot(token=TOKEN)

# Imprime el nombre de usuario de tu bot
print(mi_bot.get_me().username)

# También puedes usar la clase Updater para manejar actualizaciones
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola, soy un bot de ejemplo.")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Inicia el bot
updater.start_polling()
updater.idle()
