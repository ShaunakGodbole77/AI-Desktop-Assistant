import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json",encoding="utf8").read())

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

model = load_model("AIBotmodel.h5")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def usercommand():
    recognize = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognize.adjust_for_ambient_noise(source)
            print("listening....")
            recognize.pause_threshold = 1
            audio = recognize.listen(source, timeout=10, phrase_time_limit=10)

            print("Recognizing....")
            query = recognize.recognize_google(audio, language="en-in")
            print(f"User said {query}")


    except Exception as e:
        # speak("Say that again please...")
        return None

    query = query.lower()
    return query


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1],reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability':str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    print(tag)
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("YO! I am ready to chat")
while True:
    try:
        message = usercommand()
        print(message)
        if "quit" in message or "goodbye" in message or "good bye" in message:
            break
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)
        speak(res)

    except Exception as e:
        continue

