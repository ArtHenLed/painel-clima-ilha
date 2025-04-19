import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "c9ebb63d5d0e47e19fe151222251904"

CIDADES = {
    "Cananéia": "Cananeia",
    "Iguape": "Iguape",
    "Ilha Comprida": "Ilha Comprida"
}

DIAS_SEMANA_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

TRADUCOES_CLIMA = {
    "Sunny": "Ensolarado",
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Overcast": "Encoberto",
    "Mist": "Névoa",
    "Patchy rain nearby": "Chuvas isoladas nas proximidades",
    "Patchy snow nearby": "Neve isolada nas proximidades",
    "Patchy sleet nearby": "Granizo isolado nas proximidades",
    "Patchy freezing drizzle nearby": "Chuvisco congelante isolado",
    "Thundery outbreaks in nearby": "Trovoadas nas proximidades",
    "Blowing snow": "Neve soprada",
    "Blizzard": "Nevasca",
    "Fog": "Nevoeiro",
    "Freezing fog": "Nevoeiro congelante",
    "Patchy light drizzle": "Garoa leve e isolada",
    "Light drizzle": "Garoa leve",
    "Freezing drizzle": "Garoa congelante",
    "Heavy freezing drizzle": "Garoa congelante forte",
    "Patchy light rain": "Chuva leve e isolada",
    "Light rain": "Chuva leve",
    "Moderate rain at times": "Chuva moderada às vezes",
    "Moderate rain": "Chuva moderada",
    "Heavy rain at times": "Chuva forte às vezes",
    "Heavy rain": "Chuva forte",
    "Light freezing rain": "Chuva congelante leve",
    "Moderate or heavy freezing rain": "Chuva congelante moderada ou forte",
    "Light sleet": "Granizo leve",
    "Moderate or heavy sleet": "Granizo moderado ou forte",
    "Patchy light snow": "Neve leve e isolada",
    "Light snow": "Neve leve",
    "Patchy moderate snow": "Neve moderada e isolada",
    "Moderate snow": "Neve moderada",
    "Patchy heavy snow": "Neve forte e isolada",
    "Heavy snow": "Neve forte",
    "Ice pellets": "Granizo",
    "Light rain shower": "Chuva leve",
    "Moderate or heavy rain shower": "Chuva moderada ou forte",
    "Torrential rain shower": "Chuva torrencial",
    "Light sleet showers": "Chuvas leves de granizo",
    "Moderate or heavy sleet showers": "Chuvas moderadas ou fortes de granizo",
    "Light snow showers": "Neve leve",
    "Moderate or heavy snow showers": "Neve moderada ou forte",
    "Light showers of ice pellets": "Chuvas leves de granizo",
    "Moderate or heavy showers of ice pellets": "Chuvas moderadas ou fortes de granizo",
    "Patchy light rain with thunder": "Chuva leve com trovoadas isoladas",
    "Moderate or heavy rain with thunder": "Chuva moderada ou forte com trovoadas",
    "Patchy light snow with thunder": "Neve leve com trovoadas isoladas",
    "Moderate or heavy snow with thunder": "Neve moderada ou forte com trovoadas"
}

def traduzir_texto(texto):
    return TRADUCOES_CLIMA.get(texto, texto)

def gerar_previsao(cidade_nome, cidade_api):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_api}&days=7&lang=en"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        print(f"[ERRO] Falha ao obter dados para {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    dados = resposta.json()

    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        print(f"[ERRO] Dados ausentes para: {cidade_nome}")
        return "<p>Erro ao obter previsão</p>"

    html = ""
    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana_en = data.strftime("%A")
        dia_semana_pt = DIAS_SEMANA_PT.get(dia_semana_en, dia_semana_en)
        data_formatada = data.strftime("%d/%m")

        condicao_en = dia["day"]["condition"]["text"]
        condicao_pt = traduzir_texto(condicao_en)
        icone = dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class="card">
            <p><strong>{dia_semana_pt}, {data_formatada}</strong></p>
            <img src="https:{icone}" alt="{condicao_pt}" width="48">
            <p>{minima}°C / {maxima}°C</p>
            <p>{condicao_pt}</p>
        </div>
        """

    return html

def gerar_html():
    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Previsão do Tempo - 7 Dias</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                padding: 30px;
            }
            h1 {
                font-size: 42px;
                margin-bottom: 20px;
            }
            h2 {
                font-size: 32px;
                margin-top: 30px;
            }
            .cidade {
                margin-bottom: 40px;
            }
            .card {
                display: inline-block;
                width: 120px;
                margin: 10px;
                padding: 10px;
                background-color: #111;
                border-radius: 8px;
                text-align: center;
            }
            .card img {
                margin-bottom: 5px;
            }
            .card p {
                margin: 4px 0;
            }
        </style>
    </head>
    <body>
        <h1>Previsão do Tempo - 7 Dias</h1>
    """

    for cidade_nome, cidade_api in CIDADES.items():
        html += f'<div class="cidade"><h2>{cidade_nome}</h2>'
        html += gerar_previsao(cidade_nome, cidade_api)
        html += '</div>'

    html += """
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
