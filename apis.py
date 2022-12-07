from urllib import request, parse
import json
from datetime import datetime
from pytz import timezone

GEOCODING_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_APIKEY = 'AIzaSyBOZ6tkbWNdSqfb_o_QMTbBH11KjVT60vc'

WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'
WEATHER_APPID = '81d827fe8034c52994bd9c2dbafdf659'


def address_to_latlng(address):
    params = {'key': GOOGLE_APIKEY, 'address': address, 'language': 'ja'}

    url = GEOCODING_URL + '?' + parse.urlencode(params)
    res = request.urlopen(url)
    result = json.loads(res.read().decode('utf-8'))
    res.close()

    loc = result['results'][0]['geometry']['location']

    return (loc['lat'], loc['lng'])


def get_weather(latitude, longitude):
    params = {
        'appid': WEATHER_APPID,
        'lat': latitude,
        'lon': longitude,
        'units': 'metric'
    }

    url = WEATHER_URL + '?' + parse.urlencode(params)
    req = request.Request(url)
    res = request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    res.close()

    result = []
    for item in data['list']:
        date = datetime.strptime(item['dt_txt'],
                                 '%Y-%m-%d %H:%M:%S').astimezone(
                                     timezone('Asia/Tokyo'))
        weather = {
            'date': date.strftime('%Y-%m-%d %H:%M'),
            'weather': item['weather'][0]['main'],
            'temperature': item['main']['temp'],
            'pressure': item['main']['pressure'],
            'humidity': item['main']['humidity'],
        }
        result.append(weather)

    return result


#mail
import smtplib
from email.mime.text import MIMEText

from_email = 'js.mail.test00@gmail.com'
smtp_host = 'smtp.gmail.com'
smtp_port = 587
smtp_password = 'qjlprqnxvaorlitd'


def submitemail(to_email, mail_title, message):
    msg = MIMEText(message, 'plain')
    msg['Subject'] = mail_title
    msg['To'] = to_email
    msg['From'] = from_email

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(from_email, smtp_password)
    server.send_message(msg)
    server.quit()
