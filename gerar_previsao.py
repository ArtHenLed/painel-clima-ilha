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
    "Patchy light rain": "Chuvisco isolado",
    "Light rain": "Chuva leve",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Patchy snow": "Neve esparsa",
    "Thundery outbreaks possible": "Possibilidade de trovoadas",
    "Clear": "Céu limpo",
    "Patchy light drizzle": "Garoa isolada",
    "Light drizzle": "Garoa leve",
    "Patchy rain possible": "Possibilidade de chuva isolada",
    "Moderate or heavy rain shower": "Pancadas de chuva moderada ou forte",
    "Light rain shower": "Chuva leve",
    "Partly Cloudy": "Parcialmente nublado",
    "Patchy rain with thunder": "Chuva isolada com trovoadas",
    "Heavy rain at times": "Chuva forte por vezes",
    "Moderate or heavy rain with thunder": "Chuva moderada ou forte com trovoadas",
}

def obter_previsao(cidade_nome, cidade_api):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_api}&days=7&lang=en"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print(f"[ERRO] Falha ao obter dados para {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    dados = resposta.json()
    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        print(f"[ERRO] Dados ausentes para: {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    html = ""
    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%A, %d/%m")
        data_pt = DIAS_SEMANA_PT.get(data.split(",")[0], data.split(",")[0]) + ", " + data.split(",")[1].strip()
        condicao_en = dia["day"]["condition"]["text"]
        condicao = TRADUCOES_CLIMA.get(condicao_en, condicao_en)
        icone = dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class="card">
            <p><strong>{data_pt}</strong></p>
            <img src="https:{icone}" alt="{condicao}" width="48">
            <p>{minima}°C / {maxima}°C</p>
            <p>{condicao}</p>
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
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: black;
            color: white;
        }}
        h1 {{
            color: white;
        }}
        .cidade {{
            margin-top: 30px;
        }}
        .card {{
            display: inline-block;
            width: 120px;
            margin: 10px;
            padding: 10px;
            background: #1a1a1a;
            border-radius: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>Previsão do Tempo - 7 Dias</h1>
"""

    for nome, cidade_api in CIDADES.items():
        html += f'<div class="cidade"><h2>{nome}</h2>'
        html += obter_previsao(nome, cidade_api)
        html += "</div>"

    html += """
</body>
</html>
"""
    return html

with open("index.html", "w", encoding="utf-8") as f:
    f.write(gerar_html())
