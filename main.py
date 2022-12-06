from flask import Flask, render_template, request
from urllib import parse
import apis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  city = '東京都北区赤羽台'
  lat = 35.7801937
  lng = 139.7181163
  forecast = apis.get_weather(lat, lng)

  return render_template('index.html', city=city, lat=lat, lng=lng, forecast=forecast)

if __name__ == '__main__':
  app.run(host='0.0.0.0')