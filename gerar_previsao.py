import requests
from datetime import datetime
from pathlib import Path

# Configurações
API_KEY = "c9ebb63d5d0e47e19fe15122225190481"
CIDADE = "Ilha Comprida"
URL = f"http://api.weatherapi.com/v1/forecast.json?q={CIDADE}&days=3&lang=pt&key={API_KEY}"

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
        "patchy sleet possible": "🌨️",
        "patchy freezing drizzle possible": "🌨️",
        "thundery outbreaks possible": "⛈️",
        "blowing snow": "🌨️",
        "blizzard": "❄️",
        "fog": "🌫️",
        "freezing fog": "🌫️",
        "patchy light drizzle": "🌧️",
        "light drizzle": "🌧️",
        "freezing drizzle": "🌧️",
        "heavy freezing drizzle": "🌧️",
        "patchy light rain": "🌧️",
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
        "light rain shower": "🌦️",
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
    return icones.get(condicao.lower(), "❔")

def buscar_previsao():
    resposta = requests.get(URL)
    resposta.raise_for_status()
    return resposta.json()

def gerar_html():
    dados = buscar_previsao()
    dias = dados["forecast"]["forecastday"]

    html = ""
    for dia in dias:
        data_obj = datetime.strptime(dia["date"], "%Y-%m-%d")
        data_formatada = data_obj.strftime("%A, %d/%m").capitalize()
        condicao = dia["day"]["condition"]["text"]
        icone = obter_icone(condicao)
        temp_min = dia["day"]["mintemp_c"]
        temp_max = dia["day"]["maxtemp_c"]

        card = f"""
        <div class="day-card">
            <h2>{data_formatada}</h2>
            <img src="https:{dia["day"]["condition"]["icon"]}" alt="{condicao}">
            <p>{temp_min:.1f}°C / {temp_max:.1f}°C</p>
        </div>
        """
        html += card

    return html

def salvar_html(conteudo):
    template = Path("index_base.html").read_text(encoding="utf-8")
    resultado = template.replace("{{PREVISAO_TEMPO}}", conteudo)
    Path("index.html").write_text(resultado, encoding="utf-8")

if __name__ == "__main__":
    html_previsao = gerar_html()
    salvar_html(html_previsao)
