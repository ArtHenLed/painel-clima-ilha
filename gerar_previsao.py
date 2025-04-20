import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "c9ebb63d5d0e47e19fe151222251904"
CIDADE_NOME = "Ilha Comprida"

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
    "Patchy light rain": "Chuva leve isolada",
    "Light rain": "Chuva leve",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Thundery outbreaks possible": "Possibilidade de trovoadas",
    "Patchy light drizzle": "Garoa isolada",
    "Light drizzle": "Garoa leve",
    "Clear": "Céu limpo",
    "Partly Cloudy": "Parcialmente nublado",
    "Moderate or heavy rain with thunder": "Chuva forte com trovoadas",
    "Patchy rain possible": "Possibilidade de chuva isolada"
}

def obter_previsao(cidade_nome):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_nome}&days=3&lang=en"
    resposta = requests.get(url)
    dados = resposta.json()

    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        print(f"[ERRO] Dados ausentes para: {cidade_nome}")
        return ""

    html = ""
    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%A, %d/%m")
        data_pt = DIAS_SEMANA_PT.get(data.split(",")[0], data.split(",")[0]) + "," + data.split(",")[1]
        condicao = dia["day"]["condition"]["text"]
        condicao_pt = TRADUCOES_CLIMA.get(condicao, condicao)
        icon = dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class="card">
            <p><strong>{data_pt}</strong></p>
            <img src="https:{icon}" alt="{condicao_pt}" width="42">
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
    <title>Previsão do Tempo - Ilha Comprida</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: black;
            color: white;
            padding: 10px;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        .cidade {{
            margin-top: 10px;
        }}
        .card {{
            display: inline-block;
            width: 110px;
            margin: 5px;
            padding: 8px;
            background: #222;
            border-radius: 6px;
            text-align: center;
        }}
        img.logo {{
            position: absolute;
            top: 8px;
            right: 8px;
            width: 100px;
        }}
    </style>
</head>
<body>
    <img src="marcadagua.jpg" alt="Logo" class="logo">
    <h1>Previsão do Tempo - Ilha Comprida</h1>
    <div class="cidade">
        {conteudo}
    </div>
</body>
</html>
""".format(conteudo=obter_previsao(CIDADE_NOME))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
