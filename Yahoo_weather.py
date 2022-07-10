import requests
from plyer import notification
from bs4 import BeautifulSoup
import schedule
import datetime
import time

#Yahoo天気の情報をまとめたテキストと，それに対応する画像をLINE_Notifyに送信する(雪などは含めない)
def LINE_Notify(message,image):
    LINE_url = 'https://notify-api.line.me/api/notify'
    access_token = #'ここに自身のアクセストークンを入力'
    headers = {'Authorization':'Bearer ' + access_token}
    payload = {'message': message}
    files = {"imageFile":open(image,'rb')}
    line_req = requests.post(LINE_url, headers=headers, params=payload,files=files)

#Yahoo天気の情報をまとめたテキストのみをLINE_Notifyに送信する(雪などの晴，曇，雨以外の天気の場合)
def LINE_Message(message):
    LINE_url = 'https://notify-api.line.me/api/notify'
    access_token = #'ここに自身のアクセストークンを入力'
    headers = {'Authorization':'Bearer ' + access_token}
    payload = {'message': message}
    line_req = requests.post(LINE_url, headers=headers, params=payload)

#Yahoo天気の情報を入手する
def GetWeather(PrefectureCode,Areacode):
    url = "https://weather.yahoo.co.jp/weather/jp/" + str(PrefectureCode) + "/" + str(Areacode) + ".html"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    rs = soup.find(class_ = 'forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    global TodayWeather             #情報を入手した日の天気
    global NextWeather              #情報を入手した翌日の天気
    global NextTempH                #情報を入手した翌日の最高気温
    global NextTempL                #情報を入手した翌日の最低気温

    TodayWeather = rs[1]
    NextWeather = rs[19]
    NextTempH = rs[20]
    NextTempL = rs[21]

    print(rs[0] + "の天気は" + rs[1] + ", その次の日の天気は" + rs[19] + ".")


#天気の都道府県コードを入力(テスト用に岡山の都道府県コード33を格納した)
PrefectureCode = 33
#Yahoo天気の地域コードを入力(テスト用に岡山の地域コード6610を格納した)
Areacode = 6610

GetWeather(PrefectureCode,Areacode)

if __name__ == '__main__':
    message = "明日の岡山の天気は" + NextWeather + "だよ．" + "最高気温は" + NextTempH + "，最低気温は" + NextTempL
    if NextWeather == "晴れ":
        image = r"sun.pngの絶対パスを入力する"              #これらの画像はImageフォルダに入っています
        LINE_Notify(message,image)
    elif NextWeather == "雨":
        image = r"rain.pngの絶対パスを入力する"
        LINE_Notify(message,image)
    elif NextWeather == "曇り":
        image = r"cloud.pngの絶対パスを入力する"
        LINE_Notify(message,image)
    elif NextWeather == "晴一時雨" or "晴時々雨" or "雨時々晴" or "雨一時晴":
        image = r"sun&rain.pngの絶対パスを入力する"
        LINE_Notify(message,image)
    elif NextWeather == "曇一時雨" or "曇時々雨" or "雨時々曇" or "雨一時曇":
        image = r"cloud&rain.pngの絶対パスを入力する"
        LINE_Notify(message,image)
    elif NextWeather == "晴一時曇" or "晴時々曇" or "曇時々晴" or "曇一時晴":
        image = r"sun&cloud.pngの絶対パスを入力する"
        LINE_Notify(message,image)
    else:
        LINE_Message(message)