import requests
import json
import urllib

# Введите ваш токен бота Telegram
TOKEN = '6052677851:AAFvXRWjATtEO91TBRiMqS5nZuBiojW_McY'
# Введите ваш API-ключ OpenWeatherMap
API_KEY = '95f98815392314279764d804db8f36d5'

def send_message(chat_id, text):
    text = urllib.parse.quote_plus(text)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    requests.get(url)

def start():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url="
    requests.get(url)

def get_weather(city):
    try:
        # Запрос погоды с помощью OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Извлечение информации о погоде из ответа
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        # Формирование сообщения с информацией о погоде
        message = f"Погода в {city}:\nОписание: {weather_description}\nТемпература: {temperature}°C\nВлажность: {humidity}%"

        return message
    except:
        return 'Не удалось получить данные о погоде. Пожалуйста, попробуйте еще раз.'

def process_update(update):
    if 'message' in update and 'text' in update['message']:
        message = update['message']
        chat_id = message['chat']['id']
        text = message['text']

        if text == '/start':
            send_message(chat_id, 'Привет! Я погодный бот. Введите название города, чтобы узнать погоду.')
        else:
            weather_message = get_weather(text)
            send_message(chat_id, weather_message)

def process_updates(updates):
    for update in updates:
        process_update(update)

def main():
    start()
    offset = None

    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(url, params=params)
        data = response.json()

        if 'result' in data:
            updates = data['result']
            if updates:
                offset = updates[-1]['update_id'] + 1
                process_updates(updates)

if __name__ == '__main__':
    main()
