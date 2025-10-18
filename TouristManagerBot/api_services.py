import requests

WEATHER_API_KEY = "*************************"
EXCHANGE_API_KEY = "************************"

CITY_COUNTRY = {
    "Moscow": "RU",
    "Paris": "FR",
    "Rome": "IT",
    "Minsk": "BY",
    "Madrid": "ES",
    "Berlin": "DE",
    "Kyiv": "UA",
    "Astana": "KZ",
    "Lisbon": "PT",
    "Warsaw": "PL",
    "Vienna": "AT",
    "Athens": "GR",
    "Stockholm": "SE",
    "Oslo": "NO",
    "Washington": "US",
    "Ottawa": "CA",
    "Rio de Janeiro": "BR",
    "London": "GB",
    "Krasnodar": "RU",
    "Marseille": "FR",
    "Milan": "IT",
    "Brest": "BY",
    "Barcelona": "ES",
    "Cologne": "DE",
    "Odesa": "UA",
    "Almaty": "KZ",
    "Porto": "PT",
    "Lublin": "PL",
    "Graz": "AT",
    "Grodno": "BY",
    "Zagreb": "HR",
    "Bergen": "NO",
    "New York": "US",
    "Toronto": "CA",
    "Bucharest": "RO",
    "Budapest": "HU"
}

COUNTRY_TO_CURRENCY = {
    "RU": "RUB",
    "FR": "EUR",
    "IT": "EUR",
    "BY": "BYN",
    "ES": "EUR",
    "DE": "EUR",
    "UA": "UAH",
    "KZ": "KZT",
    "PT": "EUR",
    "PL": "PLN",
    "AT": "EUR",
    "GR": "EUR",
    "SE": "SEK",
    "NO": "NOK",
    "US": "USD",
    "CA": "CAD",
    "BR": "BRL",
    "GB": "GBP",
    "HR": "EUR",
    "HU": "HUF",
    "RO": "RON"
}


def get_weather(city):
    if not WEATHER_API_KEY or WEATHER_API_KEY == "ВАШ_OPENWEATHERMAP_API_KEY":
        print("Weather API key is missing or invalid")
        return "Ошибка: Не указан ключ OpenWeatherMap API"

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&cnt=7"
    try:
        response = requests.get(url)
        print(f"Weather API request for {city}: Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            forecast = []
            for day in data['list'][::8]:
                date = day['dt_txt'].split()[0]
                temp = day['main']['temp']
                desc = day['weather'][0]['description']
                forecast.append(f"{date}: {temp}°C, {desc}")
            return "\n".join(forecast)
        else:
            print(f"Weather API error: {response.status_code}, {response.text}")
            return f"Не удалось получить погоду: {response.status_code}"
    except Exception as e:
        print(f"Weather API exception for {city}: {e}")
        return f"Не удалось получить погоду: {str(e)}"


def get_currency(country_code):
    currency_code = COUNTRY_TO_CURRENCY.get(country_code, "Unknown")
    if currency_code == "Unknown":
        return "Неизвестная валюта"
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates = data['conversion_rates']
            currency_value = rates.get(currency_code, "Не удалось определить валюту.")
            return f"{currency_code}: {currency_value}"
        return "Не удалось получить валюту."
    except Exception as e:
        print(f"Currency API error: {e}")
        return "Не удалось получить валюту."
