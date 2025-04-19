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
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("""
        <html><head><meta charset="utf-8"><title>Previsão do Tempo</title>
        <style>
        body { background-color: #000; color: #fff; font-family: sans-serif; text-align: center; }
        .card { display: inline-block; background: #222; margin: 10px; padding: 10px; border-radius: 8px; width: 120px; }
        </style></head><body>
        <h1>Previsão do Tempo - 7 Dias</h1>
        """)
        for cidade, cid_id in CIDADES.items():
            f.write(f"<h2>{cidade}</h2><div>")
            f.write(obter_previsao(cidade, cid_id))
            f.write("</div>")
        f.write("</body></html>")

if __name__ == "__main__":
    gerar_html()
