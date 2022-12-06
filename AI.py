import operator
import PyPDF2
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
from requests import get
import socket
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import threading
import pyjokes
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import instaloader
from bs4 import BeautifulSoup
import pywikihow
import psutil, speedtest
from twilio.rest import Client
import numpy as np
import cv2
import random



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id)
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
webbrowser.register("brave", None, webbrowser.BackgroundBrowser(brave_path))

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def pdf_reader():
    speak("Please specify a book name to read")
    bookname = usercommand().lower()
    book = open(f"{bookname}.pdf",'rb')
    pdfreader = PyPDF2.PdfFileReader(book)
    pages = pdfreader.numPages
    speak(f"There are a total of {pages} pages in this book.")
    speak("From which page number should i read?")
    pg = usercommand().lower()
    if "page number" in pg:
        pg = int(pg[11:len(pg)])
    elif "number" in pg:
        pg = int(pg[7:len(pg)])

    for i in range(pg,pages+1):
        page = pdfreader.getPage(i)
        text = page.extractText()
        speak(text)


def usercommand():
        recognize = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognize.adjust_for_ambient_noise(source)
                print("listening....")
                recognize.pause_threshold = 1
                audio = recognize.listen(source,timeout=10,phrase_time_limit=10)

                print("Recognizing....")
                query = recognize.recognize_google(audio, language="en-in")
                print(f"User said {query}")


        except Exception as e:
            #speak("Say that again please...")
            return None

        query = query.lower()
        return query



def wish():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good Morning Sir")
    elif 12 <= hour < 16:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("How may I be of assistance?")


def sendEmail():
    password = '#'
    email = '#'
    speak("To whom should i send it to sir?")
    to = usercommand()
    speak("what should i say?")
    content = usercommand().lower()
    if "send a file" in content:
        speak("Okay sir. What is the subject for this email?")
        query = usercommand().lower()
        subject = query
        speak("And sir, what is the message for this email?")
        query2 = usercommand().lower()
        message = query2
        speak("Sir please enter the correct path of the file into the shell...")
        file_location = input("Enter File path here : ")
        speak("Please wait I am sending email now")

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename = %s" %filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email,to,text)
        server.quit()
        speak(f"The email has been sent to {to}")


    else:


        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to, content)
        server.quit()
        speak(f"The email has been sent to {to}")

def setAlarm(time):
    while True:
        timer = str(datetime.datetime.now())
        alarm = str(timer[11:16])
        if time == alarm:
            music_dir = "D:\\music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))
            break


def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=83263a48521a48a797182dbc3926e513'

    main_page = requests.get(main_url).json()
    articles = main_page['articles']
    head = []
    day = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar['title'])
    for i in range(len(day)):
        print(f"Today's {day[i]} news is : {head[i]}")
        speak(f"Today's {day[i]} news is : {head[i]}")



def performance():
    pyautogui.press('esc')
    speak("Verification Successful")
    speak("Welcome Shaunak Sir")
    wish()
    while True:
        try:
            query = usercommand()

            if "open notepad" in query:# or "notepad" in query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "open adobe" in query or "open acrobat" in query:
                apath = "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"
                os.startfile(apath)

            elif "open command prompt" in query or "command prompt" in query:
                os.system("start cmd")

            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("Webcam", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in query:
                music_dir = "D:\\music"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "my ip address" in query:
                ip = get("https://api.ipify.org").text
                speak(f"Your ip address is {ip}")

            elif "ip address of" in query:
                index = query.find("ip address of")
                true_index = index + 14
                website = query[true_index:len(query)] + ".com"
                print(website)
                ip = socket.gethostbyname(f'{website}')
                speak(f"Your ip address is {ip}")

            elif "wikipedia" in query:
                speak("Searching Wikipedia......")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences=4)
                speak("According to the wikipedia....")
                #print(results)
                speak(results)

            elif "open google" in query or "search google" in query:
                speak("What should I search on google sir?")
                cmd = usercommand().lower()
                cmd = "google.com/search?q="+cmd
                webbrowser.get('brave').open(cmd)

            elif "open" in query:
                query = query.replace(" ","")
                index = query.find("open")
                true_index = index + 4
                website = query[true_index:len(query)] + ".com"
                print(website)
                webbrowser.get('brave').open(website)

            elif "send message" in query:
                speak("Who do you want me to send the message to sir?")
                number = usercommand().lower()
                number = number.replace(" ","")


                number = "+91"+number
                print(number)
                speak("What message should I send sir?")
                message = usercommand().lower()
                print(message)
                kit.sendwhatmsg_instantly(number,message)

            elif "schedule whatsapp message" in query:
                speak("Who do you want me to send the message to sir?")
                number = usercommand().lower()
                number = number.replace(" ", "")
                number = "+91" + number
                print(number)
                speak("What message should I send sir?")
                message = usercommand().lower()
                print(message)
                speak("When would you like me to send this message?")
                time = usercommand().lower()
                print(time)
                hour,minutes = time.split(" ")
                kit.sendwhatmsg(number,message,hour,minutes)

            elif "play on youtube" in query or "on youtube" in query:
                speak("What would you like me to play on youtube sir?")
                song = usercommand()
                kit.playonyt(song)

            elif "send email" in query:
                try:
                    sendEmail()

                except Exception as e:
                    print(e)
                    speak("Sorry sir, I was unable to send the email.")

            elif "close" in query or "quit" in query:
                index = query.find("close")
                true_index = index + 6
                query = query[true_index:len(query)]
                speak(f"okay sir. Closing {query}")
                query = query+".exe"
                print(query)
                os.system(f"taskkill /f /im {query}")

            elif "set alarm" in query:
                index = query.find("set alarm")
                true_index = index + 14
                query = str(query[true_index:len(query)])
                alarm_thread = threading.Thread(target=setAlarm(query))
                alarm_thread.start()

            elif "joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendedState 0,1,0")

            elif "volume up" in query:
                pyautogui.press('volumeup')

            elif "volume down" in query:
                pyautogui.press('volumedown')

            elif "volume mute" in query or 'mute' in query:
                pyautogui.press('volumemute')

            elif "no thanks" in query or "thanks" in query:
                speak("In that case I will be dormant. Just wake me up if you need me sir.")
                break

            elif "switch the window" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "tell me news" in query or "news" in query:
                speak("Please be patient for a few minutes sir. I am fetching the news.")
                news()

            elif "where am i" in query:
                speak("Wait sir, let me check our current location...")
                try:
                    ipadd = requests.get('https://api.ipify.org').text
                    print(ipadd)
                    url = "https://get.geojs.io/v1/ip/geo/"+ipadd+".json"
                    georequests = requests.get(url)
                    geo_data = georequests.json()
                    print(geo_data)
                    city = geo_data['city']
                    state = geo_data['region']
                    country = geo_data['country']
                    speak(f"Sir, I am not sure but i think we are in {city} city in the state of {state} of {country} country.")

                except Exception as e:
                    speak("Sorry sir, I was unable to determine where we are.")

            elif "check instagram" in query:
                speak("Which Instagram profile should i check sir?")
                profile_name = usercommand()
                print(profile_name)
                webbrowser.open(f"https://instagram.com/{profile_name}")
                speak(f"Here is the profile of user {profile_name} that you requested.")
                time.sleep(5)
                speak("Sir would you like to download profile picture of this account?")
                condition = usercommand().lower()
                if "yes" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(profile_name,profile_pic_only=True)
                    speak("Sir, I have downloaded the profile pic. It is stored in the main folder if you wanna check.")

            elif "take screenshot" in query or "take a screenshot" in query:
                speak("Under what filename should i save the screenshot sir?")
                name = usercommand().lower()
                speak("Taking screenshot now.")
                time.sleep(2)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak(f"Sir, I have save the screenshot under the name of {name}. It is stored in the main folder if you wanna check.")

            elif "read pdf" in query or "Read me a book" in query or "read a book" in query:
                pdf_reader()

            elif "hide files" in query or "hide all files" in query or "hide my files" in query or "make my files hidden" in query or "make my files visible" in query or "visible" in query:
                if "hide" in query or "hidden" in query:
                    os.system("attrib +h /s /d")
                    speak("The files are now hidden sir")
                elif "visible" in query:
                    speak("Are you sure sir? It will make all the files visible to everybody.")
                    condition = usercommand().lower()
                    if "yes" in condition or "sure" in condition:
                        os.system("attrib -h /s /d")
                        speak("Very well sir. The files are now visible")
                    else:
                        pass

            elif "calculate" in query or "calculation" in query:
                if "calculate" in query:
                    index = query.find("calculate")
                    true_index = index + 10
                    query = query[true_index:len(query)]
                elif "calculation" in query:
                    index = query.find("calculation")
                    true_index = index + 12
                    query = query[true_index:len(query)]
                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided': operator.__truediv__
                    }[op]

                def eval_binary_expression(op1,oper, op2):
                    op1,op2 = float(op1), float(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak(f"Your result is {eval_binary_expression(*(query.split()))}")

            elif "temperature" in query or "weather" in query:
                if "temperature" in query:
                    speak("Which region's temperature should i check for?")
                    region = usercommand()
                    cmd = f"https://www.google.com/search?q=temperature in {region}"
                    req = requests.get(cmd)
                    data = BeautifulSoup(req.text, "html.parser")
                    temp = data.find("div",class_="BNeawe").text
                    speak(f"Currently the temperature in {region} is {temp}")
                elif "weather" in query:
                    speak("Which region's weather should i check for?")
                    region = usercommand()
                    cmd = f"https://www.google.com/search?q=weather in {region}"
                    req = requests.get(cmd)
                    data = BeautifulSoup(req.text, "html.parser")
                    weather = data.find("div", class_="s3v9rd").text
                    print(weather)
                    wind = data.find("div", class_="AP7Wnd").text
                    print(wind)
                    speak(f"Currently the weather in {region} is {wind} {weather}")

            elif "how to" in query:
                try:
                    index = query.find("how to")
                    true_index = index + 7
                    query = query[true_index:len(query)]
                    max_results = 1
                    how_to = pywikihow.search_wikihow(query, max_results)
                    assert len(how_to)==1
                    how_to[0].print()
                    speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry sir. I was unable to find that.")

            elif "how much power is left" in query or "how much power left" in query or "battery" in query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Sir the system has {percentage} percent battery left.")
                if percentage > 75:
                    speak("We have enough battery to continue our work")
                elif 50 < percentage <= 75:
                    speak("We have enough battery now but you should consider connecting to a charging point soon")
                elif 25 < percentage <= 50:
                    speak("I think its quite necessary to connect to a charging point now")
                else:
                    speak("Please connect to a charging point ASAP ortherwise we risk the system being shutdown by low battery")

            elif "internet speed" in query:
                spdtst = speedtest.Speedtest()
                speak("Calculating now. It might take some time.")
                dl = spdtst.download()
                up = spdtst.upload()
                speak(f"Sir our downloading speed is {dl} bits per second and our uploading speed is {up} bits per second")

            elif "send sms" in query:   # admiral zeno jahimog820@topyte.com
                speak("What should I say in the message?")
                msg = usercommand()
                speak("To whom should i send this message to sir?")
                send_to = usercommand()
                account_sid = None
                auth_token = None
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=msg,
                    from_=None,
                    to=None
                )
                print(message.sid)

            elif "place a call" in query or "place call" in query or "make call" in query:   # admiral zeno jahimog820@topyte.com
                speak("What should I say in the message?")
                msg = usercommand()
                speak("To whom should i send this message to sir?")
                send_to = usercommand()
                account_sid = None
                auth_token = None
                client = Client(account_sid, auth_token)

                message = client.calls.create(
                    body=msg,
                    from_=None,
                    to=None
                )
                print(message.sid)

            elif "open mobile camera" in query:
                import urllib.request
                import cv2
                import numpy as np
                import time
                url = ""
                while True:
                    img_arr = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
                    img = cv2.imdecode(img_arr,-1)
                    cv2.imshow("IPWebcam",img)
                    q = cv2.waitKey(1)
                    if q == ord("q"):
                        break

                cv2.destroyAllWindows()

            elif "check twitter" in query or "twitter" in query:
                import TwitterBot


            else:
                import chatbot

            speak("Do you have any other request sir?")



        except Exception as e:
            continue



if __name__ == "__main__":

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    recognizer.read('trainer/trainer.yml')  # load trained model
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)  # initializing haar cascade for object detection approach

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type

    id = 2  # number of persons you want to Recognize

    names = ['', 'avi']  # names, leave first empty bcz counter starts from 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # flag = True
    check =1

    while check == 1:

        ret, img = cam.read()  # read the frames using the above created object

        converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # used to draw a rectangle on any image

            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])  # to predict on every single image

            # Check if accuracy is less them 100 ==> "0" is perfect match
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                performance()
                check = 2

            else:
                speak("Face not recognized!  Verification Unsuccessful")
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()

    while True:
        try:
            permission = usercommand()
            if "wake up" in permission:
                performance()
            elif "goodbye" in permission or "good bye" in permission:
                speak("I will take your leave then sir. Have a great day!")
                sys.exit()
        except Exception as e:
            continue



#usercommand()
#speak("Hello! this is your personal assistant")