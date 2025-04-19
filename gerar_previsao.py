import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CIDADES = {
    "Cananéia": "346796",
    "Iguape": "346943",
    "Ilha Comprida": "42649"
}

def obter_previsao(cidade_nome, cidade_id):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=id:{cidade_id}&days=7&lang=pt"
    resposta = requests.get(url)
    dados = resposta.json()
    html = ""

    if "forecast" not in dados:
        print(f"Erro na API para {cidade_nome}: {dados}")
        return ""

    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%a., %d/%m")
        condicao = dia["day"]["condition"]["text"]
        icon = dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)
        html += f"""
        <div class="card">
            <p>{data}</p>
            <img src="https:{icon}" alt="{condicao}" width="48">
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
        <title>Previsão do Tempo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: white;
                text-align: center;
            }}
            .container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }}
            .card {{
                background-color: #222;
                border-radius: 10px;
                padding: 10px;
                width: 120px;
            }}
        </style>
    </head>
    <body>
        <h1>Previsão do Tempo - 7 Dias</h1>
    """

    for cidade, cid_id in CIDADES.items():
        html += f"<h2>{cidade}</h2><div class='container'>"
        html += obter_previsao(cidade, cid_id)
        html += "</div>"

    html += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
