import requests
from datetime import datetime
import os

API_KEY = os.getenv("WEATHER_API_KEY") or "SUA_CHAVE_API"
CIDADES = {
    "Cananéia": "Cananéia",
    "Iguape": "Iguape",
    "Ilha Comprida": "Ilha Comprida"
}

# Traduções de dias da semana
DIAS_SEMANA = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Traduções de condições climáticas
TRADUCOES_CONDICOES = {
    "Sunny": "Ensolarado",
    "Clear": "Céu limpo",
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Overcast": "Encoberto",
    "Mist": "Névoa",
    "Patchy rain possible": "Possibilidade de chuva fraca",
    "Patchy rain nearby": "Chuva fraca nas proximidades",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Light rain": "Chuva leve",
    "Thundery outbreaks possible": "Possibilidade de trovoadas",
    "Fog": "Nevoeiro",
    "Freezing fog": "Nevoeiro congelante",
    "Patchy light drizzle": "Garoa leve localizada",
    "Light drizzle": "Garoa leve",
    "Patchy snow possible": "Possibilidade de neve fraca",
    "Light snow": "Neve leve",
    "Moderate snow": "Neve moderada",
    "Heavy snow": "Neve forte",
    "Blizzard": "Nevasca",
    "Patchy sleet possible": "Possibilidade de granizo",
    "Light sleet": "Granizo leve",
    "Moderate or heavy sleet": "Granizo moderado ou forte",
    "Torrential rain shower": "Chuva torrencial",
    "Patchy freezing drizzle possible": "Possibilidade de garoa congelante",
    "Patchy light snow": "Neve leve localizada",
    "Patchy moderate snow": "Neve moderada localizada",
    "Patchy heavy snow": "Neve forte localizada",
    "Patchy light rain": "Chuva leve localizada",
    "Patchy moderate rain": "Chuva moderada localizada",
    "Patchy heavy rain": "Chuva forte localizada",
    "Light rain shower": "Pancada leve de chuva",
    "Moderate or heavy rain shower": "Pancada moderada ou forte de chuva",
    "Light snow shower": "Pancada leve de neve",
    "Moderate or heavy snow shower": "Pancada moderada ou forte de neve",
    "Light sleet showers": "Pancada leve de granizo",
    "Moderate or heavy sleet showers": "Pancada moderada ou forte de granizo"
}

def obter_previsao(cidade_nome, local):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={local}&days=7&lang=en"
    resposta = requests.get(url)
    dados = resposta.json()

    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        print(f"[ERRO] Dados ausentes para: {cidade_nome}")
        return f"<h2>{cidade_nome}</h2><p>Erro ao obter previsão</p>"

    html = f"<h2>{cidade_nome}</h2><div class='previsao'>"
    for dia in dados["forecast"]["forecastday"]:
        data_obj = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana_en = data_obj.strftime("%A")
        dia_semana_pt = DIAS_SEMANA.get(dia_semana_en, dia_semana_en)
        data_formatada = data_obj.strftime("%d/%m")

        condicao_en = dia["day"]["condition"]["text"]
        condicao_pt = TRADUCOES_CONDICOES.get(condicao_en, condicao_en)
        icon = "https:" + dia["day"]["condition"]["icon"]

        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class='card'>
            <p><strong>{dia_semana_pt}, {data_formatada}</strong></p>
            <img src="{icon}" width="48"><br>
            <span>{minima}°C / {maxima}°C</span><br>
            <p>{condicao_pt}</p>
        </div>
        """
    html += "</div>"
    return html

def gerar_html():
    html = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Previsão do Tempo - 7 Dias</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        .cidade { margin-top: 30px; }
        .card {
            display: inline-block;
            width: 120px;
            margin: 10px;
            padding: 10px;
            background: #f1f1f1;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Previsão do Tempo - 7 Dias</h1>
    """
    for nome, local in CIDADES.items():
        html += f"<div class='cidade'>{obter_previsao(nome, local)}</div>"
    html += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
