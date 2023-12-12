import random
import json
import pickle 

import numpy as np

import nltk
from nltk import WordNetLemmatizer 

#fuzz -> fuzzywuzzy

from keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

def build_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(128, input_shape=(input_dim,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=SGD(learning_rate=0.001, momentum=0.9, nesterov=True, clipnorm=1.), metrics=['accuracy'])
    return model

def train_model(model, train_x, train_y, epochs=100, batch_size=5):
    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=1)

lemmatizer = WordNetLemmatizer()

with open('locaciones.json', 'r') as file:
    datos = json.load(file)

words, classes, documents = [], [], []
ignorar_letras = ['?', '!', ',', '.']

for dato in datos['intents']: 
    for patron in dato['patterns']: 
        words_list = nltk.word_tokenize(patron)
        words.extend(words_list)
        documents.append([words_list, dato['name']])
        if dato['name'] not in classes: 
            classes.append(dato['name'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignorar_letras]
words = sorted(set(words))

pickle.dump(words, open('word.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0]*len(classes)

for document in documents: 
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words: 
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training_data = np.array(training)
#training_data = np.hstack((training_data[:, 0], training_data[:, 1]))

print(training_data)

train_x = np.array(list(training_data[:, 0]))
train_y = np.array(list(training_data[:, 1]))

# Convierte las etiquetas a formato one-hot
train_y_one_hot = to_categorical(train_y, num_classes=len(classes))

# Construye el modelo
model = build_model(len(train_x[0]), len(classes))

# Entrena el modelo
train_model(model, (train_x), (train_y))

# Guarda el modelo
model.save('chatbot_model.h5')