import requests
from datetime import datetime

API_KEY = "c9ebb63d5d0e47e19fe151222251904"
CIDADES = {
    "Cananéia": "Cananeia",
    "Iguape": "Iguape",
    "Ilha Comprida": "Ilha Comprida, SP"
}

def obter_previsao(cidade_nome):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_nome}&days=7&aqi=no&alerts=no"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        if "forecast" not in dados or "forecastday" not in dados["forecast"]:
            print(f"[ERRO] Dados ausentes para: {cidade_nome}")
            return f"<p>Erro ao obter previsão: dados incompletos</p>"

        html = ""
        for dia in dados["forecast"]["forecastday"]:
            data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%A, %d/%m").title()
            condicao = dia["day"]["condition"]["text"]
            icon = dia["day"]["condition"]["icon"]
            minima = round(dia["day"]["mintemp_c"], 1)
            maxima = round(dia["day"]["maxtemp_c"], 1)

            html += f"""
            <div class="card">
                <p><strong>{data}</strong></p>
                <img src="https:{icon}" alt="{condicao}" width="48">
                <p>{minima}ºC / {maxima}ºC</p>
                <p>{condicao}</p>
            </div>
            """
        return html

    except Exception as e:
        print(f"[ERRO] Falha ao obter previsão para {cidade_nome}: {e}")
        return f"<p>Erro ao obter previsão: '{e}'</p>"

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

    for nome_exibicao, nome_api in CIDADES.items():
        html += f'<div class="cidade"><h2>{nome_exibicao}</h2>'
        html += obter_previsao(nome_api)
        html += '</div>'

    html += """
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
