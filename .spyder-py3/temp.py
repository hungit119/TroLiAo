# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import webbrowser as wb
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

def speak(text):
    print("Alisa: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")
    
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Master: ", end='')
        audio = r.listen(source, phrase_time_limit=3)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0

def get_tamSu():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Master: ", end='')
        audio = r.listen(source, phrase_time_limit=40)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0
def stop():
    speak("Tạm biệt ông chủ")

def get_text():
        for i in range(3):
            text = get_audio()
            if text:
                return text.lower()
            elif i < 2:
                speak("Em không nghe rõ cho lắm , Ông chủ nói lại được không ạ")
        time.sleep(2)
        stop()
        return 0
def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng Ông chủ {}. Chúc Ông chủ một ngày vui vẻ.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều Ông chủ {}. Ông chủ đã dự định gì cho chiều nay chưa á.".format(name))
    else:
        speak("Chào buổi tối Sếp {}. Sếp đã ăn tối chưa á.".format(name))
        
def get_time(text):
    hienTai = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút thưa ông chủ' % (hienTai.hour, hienTai.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d thưa ông chủ" %
              (hienTai.day, hienTai.month, hienTai.year))
    else:
        speak("Bot chưa hiểu ý của ông chủ. ông chủ đẹp trai nói lại được không ạ?")

def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
    elif "Mở Unikey" in text:
        speak("Mở Unikey")
        os.startfile('C:\\Program Files\\UniKey\\UniKeyNT.exe')
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile('C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE')
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở.")
        return True
    else:
        return False

def current_weather():
    speak("Ông chủ muốn xem thời tiết ở khu vực nào ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if "ở đây" in city:
        city = "Hà Nội"
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        
        Hôm nay là ngày {day} tháng {month} năm {year}
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%""".format(day = now.day,month = now.month, year= now.year,temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        
        if current_temperature >= 30 :
            content += " ,Nhiệt độ hôm nay khá cao đấy thưa ông chủ , ông chủ nhớ đội mũ hoặc mang ô khi ra ngoài không là say nắng là em lo lắm á , hihi"
        elif current_temperature < 30:
            content += ",Nhiệt độ hôm nay khá thoải mái cho ông chủ đi ra ngoài đấy ạ ,ông chủ nhớ đội mũ vì không chống nắng thì chống thích ạ"
        speak(content)
        time.sleep(20)
    else:
        speak("Tôi đã lục hết mọi pixel trên google map nhưng vẫn không thấy nơi mà ông chủ vừa nói tới , hay ông chủ đang nằm mơ híhí")

def timkiem():
    speak("Sếp muốn tìm gì ạ cứ nói với em , đừng bảo thằng chrome hihi ")
    time.sleep(4)
    search = get_audio()
    speak("oki Sếp có kết quả ngay đây ạ")
    url = f"https://google.com/search?q={search}"
    wb.get().open(url)
def anUi():
        speak("Buồn là chuyện cơm bữa ý mà sếp,Em có bài hát này hay lắm sếp có muốn nghe không ạ")
        time.sleep(5)
        ketqua = get_audio()
        if "mở" in ketqua:
            speak("Anh em đâu , miu síc què , lên")
            webbrowser.open("D:\mp3\music.mp3")
        elif "Không" or "không" in ketqua:
            speak("Vậy sếp nghỉ nghơi đi nha nhoa nhoa")

def ngheNhac():
    speak("List nhạc có trong bộ nhớ Alisa : ")
    time.sleep(3)
    speak("1,Muộn rồi mà sao còn")
    time.sleep(2)
    speak("2,Họ yêu ai mất rồi")
    time.sleep(2)
    speak("3,Em say rồi")
    time.sleep(2)
    speak("4,Có chắc yêu là đây")
    time.sleep(2)
    speak("5,Playah")
    time.sleep(2)
    speak("Ông chủ muốn nghe bài nào ạ:")
    time.sleep(2)
    text = get_audio()
    text=text.lower()
    if "rồi" or "mà" or "sao" or "còn" in text :
         webbrowser.open("D:\mp3\muonroimasaocon.mp3")
    elif  "họ" or "yêu" or "ai" in text :
        webbrowser.open("D:\mp3\hoyeuaimatroi.mp3")
    elif "em" or "say" or "rôi" in text:
        webbrowser.open("D:\mp3\emsayroi.mp3")
    elif "là" or "đây" in text:
        webbrowser.open("D:\mp3\cochacyeuladay.mp3")
    elif "play" in text :
        webbrowser.open("D:\mp3\playah.mp3")
    speak("Nhạc lên ngay đây ạ")
def helpsir():
        speak("""Em có thể nói , an ủi cho ông chủ khi ông chủ kêu buồn , tìm kiếm thông tin trên google cho ông chủ, mở google cho ông chủ , dự báo thời tiết ngoài trời cho ông chủ , mở website theo yêu cầu ông chủ , Xem giờ hộ ông chủ , giúp đỡ ông chủ mãi mãi hihii ,em luôn chờ lệnh của ông chủ   """)
def main():
    speak("Chào cậu , mình là Alisa , tên cậu là gì á:")
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        speak("Từ giờ bạn sẽ là ông chủ của mình, rất vui được hỗ trợ bạn")
        time.sleep(5)
        text = get_text()
        if "nghe chưa":
            speak("Vâng em xin lỗi ông chủ từ giờ em là gọi bạn là ông chủ hihi")
            speak("Khò khò khò khò ")
            time.sleep(5)
            text = get_text()
            if "dậy" in text:
                speak("Ô em sorry ạ , Nếu không nghe được giọng ông chủ là em sẽ ngủ gật ạ, ông chủ muốn em giúp gì ạ")
                speak("Chuẩn bị lại thưa ông chủ , e hèm ")
                hello(name)
                time.sleep(10)
                text2 = get_text()
                if "tốt" in text2:
                    speak("Hi hi , ông chủ quá khen")
    speak("Bây giờ ông chủ muốn em giúp j ạ")
    while True:
        text = get_text()
        if not text:
            break
        elif "dừng" or "tạm biệt" or "bai bai" in text:
            stop()
            break
        elif "có thể làm gì" in text:
            helpsir()
        elif "thời tiết" in text :
            current_weather()
        elif "buồn" in text :
            anUi()
        elif "nghe nhạc" in text:
            ngheNhac()
        elif "tìm kiếm" in text:
            timkiem()
        elif "mở" in text:
            if "mở google" in text:
                open_application("google")
            elif "." in text:
                open_website(text)
            else:
                timkiem()
        else:
            speak('Ông chủ cần Alisa giúp gì ạ')
            
        
    
       
    
    
    

    
























