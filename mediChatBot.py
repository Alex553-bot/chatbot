from dotenv import load_dotenv
import os
import telebot
import spacy
import nltk
import pickle
import json
import numpy as np
from keras.models import load_model

load_dotenv()

words = pickle.load(open('./modelo/word.pkl', 'rb'))
classes = pickle.load(open('./modelo/classes.pkl', 'rb'))
model = load_model('./modelo/chatbot_model.h5')

with open('./conocimiento/locaciones.json', 'r') as file:
    datos = json.load(file)

lemmatizer = nltk.stem.WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        print(f'token: {s}')
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def obtain_response(intent_predicted):
    intent_info = next((intent for intent in datos['intents'] if intent['name'] == intent_predicted), None)
    if intent_info:
        respuesta = intent_info.get('responses', ['No entiendo'])
        return np.random.choice(respuesta)
    else:
        return 'No entiendo'

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
print(TELEGRAM_TOKEN)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# PARA PROBAR SI HAY RESPUESTA
# commands
@bot.message_handler(commands=["help", "start"])
def enviar(message):
    bot.reply_to(message, "Hola, ¿cómo estás?")

@bot.message_handler(func=lambda message: True)
def mensaje(message):
    input_text = message.text
    intent_predicho = predict_class(input_text, model)
    if intent_predicho:
        respuesta = obtain_response(intent_predicho[0]['intent'])
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, 'no entiendo lo que me dijiste')

# Inicia el bot
bot.polling()
