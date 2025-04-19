import requests
from datetime import datetime
import locale

# Forçar local em português
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

API_KEY = "c9ebb63d5d0e47e19fe151222251904"
CIDADES = {
    "Cananéia": "Cananeia",
    "Iguape": "Iguape",
    "Ilha Comprida": "Ilha Comprida"
}

TRADUCOES_CONDICOES = {
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Overcast": "Encoberto",
    "Mist": "Névoa",
    "Patchy rain possible": "Possibilidade de chuva isolada",
    "Patchy rain nearby": "Chuva isolada nas proximidades",
    "Light rain": "Chuva leve",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Sunny": "Ensolarado",
    "Clear": "Limpo",
    "Rain": "Chuva",
    "Showers": "Pancadas de chuva",
    "Thundery outbreaks possible": "Possibilidade de trovoadas",
    "Patchy light rain": "Chuva fraca isolada",
    "Patchy moderate rain": "Chuva moderada isolada",
    "Light rain shower": "Chuva leve passageira",
    "Patchy heavy rain": "Chuva forte isolada",
    "Heavy rain at times": "Chuva forte às vezes",
    "Partly Cloudy": "Parcialmente nublado",
}

def obter_previsao(cidade_nome, cidade_query):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_query}&days=7&lang=pt"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print(f"[ERRO] Falha ao obter dados para {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    dados = resposta.json()
    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        print(f"[ERRO] Dados ausentes para: {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    html = "<div class='cidade'>"
    html += f"<h2>{cidade_nome}</h2>"
    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana = data.strftime("%A").capitalize()
        dia_formatado = data.strftime("%d/%m")
        condicao = dia["day"]["condition"]["text"]
        condicao_pt = TRADUCOES_CONDICOES.get(condicao, condicao)
        icon = "https:" + dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class='card'>
            <p><strong>{dia_semana}, {dia_formatado}</strong></p>
            <img src="{icon}" alt="{condicao_pt}" width="48">
            <p>{minima}°C / {maxima}°C</p>
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
        body { font-family: Arial, sans-serif; padding: 20px; background: #fff; color: #333; }
        h1 { font-size: 28px; }
        .cidade { margin-top: 40px; }
        .card {
            display: inline-block;
            width: 130px;
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
    for nome, query in CIDADES.items():
        html += obter_previsao(nome, query)

    html += """
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
