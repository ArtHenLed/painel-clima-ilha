import requests
from datetime import datetime
from pathlib import Path

# Configurações
API_KEY = "c9ebb63d5d0e47e19fe15122225190481"
CIDADE = "Ilha Comprida"
URL = f"http://api.weatherapi.com/v1/forecast.json?q={CIDADE}&days=4&lang=pt&key={API_KEY}"

# Traduções para os ícones do WeatherAPI
def obter_icone(condicao):
    icones = {
        "sunny": "☀️",
        "partly cloudy": "⛅",
        "cloudy": "☁️",
        "overcast": "☁️",
        "mist": "🌫️",
        "patchy rain possible": "🌦️",
        "patchy snow possible": "🌨️",
        "patchy sleet possible": "🌧️",
        "patchy freezing drizzle possible": "🌧️",
        "thundery outbreaks possible": "⛈️",
        "blowing snow": "🌨️",
        "blizzard": "🌨️",
        "fog": "🌫️",
        "freezing fog": "🌫️",
        "patchy light drizzle": "🌦️",
        "light drizzle": "🌦️",
        "freezing drizzle": "🌧️",
        "heavy freezing drizzle": "🌧️",
        "patchy light rain": "🌦️",
        "light rain": "🌧️",
        "moderate rain at times": "🌧️",
        "moderate rain": "🌧️",
        "heavy rain at times": "🌧️",
        "heavy rain": "🌧️",
        "light freezing rain": "🌧️",
        "moderate or heavy freezing rain": "🌧️",
        "light sleet": "🌨️",
        "moderate or heavy sleet": "🌨️",
        "patchy light snow": "🌨️",
        "light snow": "🌨️",
        "patchy moderate snow": "🌨️",
        "moderate snow": "🌨️",
        "patchy heavy snow": "🌨️",
        "heavy snow": "🌨️",
        "ice pellets": "🌨️",
        "light rain shower": "🌧️",
        "moderate or heavy rain shower": "🌧️",
        "torrential rain shower": "🌧️",
        "light sleet showers": "🌨️",
        "moderate or heavy sleet showers": "🌨️",
        "light snow showers": "🌨️",
        "moderate or heavy snow showers": "🌨️",
        "light showers of ice pellets": "🌨️",
        "moderate or heavy showers of ice pellets": "🌨️",
        "patchy light rain with thunder": "⛈️",
        "moderate or heavy rain with thunder": "⛈️",
        "patchy light snow with thunder": "⛈️",
        "moderate or heavy snow with thunder": "⛈️",
    }

    return icones.get(condicao.lower(), "❓")

def buscar_previsao():
    resposta = requests.get(URL)
    resposta.raise_for_status()
    return resposta.json()

def gerar_html():
    dados = buscar_previsao()
    previsoes = dados["forecast"]["forecastday"]

    cards = ""
    for dia in previsoes:
        data = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana = data.strftime("%A")
        dia_formatado = data.strftime("%d/%m")

        icone_url = f"https:{dia['day']['condition']['icon']}"
        icone = obter_icone(dia['day']['condition']['text'])
        temp_min = round(dia["day"]["mintemp_c"], 1)
        temp_max = round(dia["day"]["maxtemp_c"], 1)

        cards += f"""
        <div class="day-card">
            <h2>{data.strftime('%A').capitalize()}, {data.strftime('%d/%m')}</h2>
            <img src="{icone_url}" alt="{icone}" />
            <p>{temp_min}°C / {temp_max}°C</p>
        </div>
        """

    with open("index_base.html", "r", encoding="utf-8") as arquivo_base:
        html_base = arquivo_base.read()

    html_final = html_base.replace("{{PREVISAO_TEMPO}}", cards)

    with open("index.html", "w", encoding="utf-8") as saida:
        saida.write(html_final)

if __name__ == "__main__":
    gerar_html()
