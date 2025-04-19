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
    "Patchy light rain": "Chuva leve isolada",
    "Light rain": "Chuva leve",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Thundery outbreaks possible": "Possibilidade de trovoadas",
    "Patchy snow nearby": "Neve isolada nas proximidades",
    "Light snow": "Neve leve",
    "Moderate snow": "Neve moderada",
    "Heavy snow": "Neve forte",
    "Fog": "Nevoeiro",
    "Clear": "Céu limpo",
    "Patchy rain possible": "Possibilidade de chuva isolada",
    "Patchy light drizzle": "Garoa leve e isolada",
    "Light drizzle": "Garoa leve",
    "Showers": "Pancadas de chuva",
    "Patchy light rain with thunder": "Chuva leve isolada com trovoadas",
    "Moderate or heavy rain with thunder": "Chuva forte com trovoadas",
    "Partly Cloudy": "Parcialmente nublado",
    "Patchy rain": "Chuva isolada",
    "Moderate or heavy rain shower": "Pancada de chuva forte",
    "Light rain shower": "Pancada de chuva leve",
    "Moderate rain at times": "Chuva moderada ocasional",
}

def traduzir_dia(data_iso):
    data = datetime.strptime(data_iso, "%Y-%m-%d")
    nome_en = data.strftime("%A")
    nome_pt = DIAS_SEMANA_PT.get(nome_en, nome_en)
    return f"{nome_pt}, {data.strftime('%d/%m')}"

def gerar_previsao(cidade_nome, cidade_api):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade_api}&days=7&aqi=no&alerts=no&lang=en"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print(f"[ERRO] Não foi possível obter dados para {cidade_nome}")
        return f"<p>Erro ao obter previsão</p>"

    dados = resposta.json()
    if "forecast" not in dados or "forecastday" not in dados["forecast"]:
        return f"<p>Erro ao obter previsão</p>"

    html = ""
    for dia in dados["forecast"]["forecastday"]:
        data_formatada = traduzir_dia(dia["date"])
        condicao = dia["day"]["condition"]["text"]
        condicao_traduzida = TRADUCOES_CLIMA.get(condicao, condicao)
        icone = dia["day"]["condition"]["icon"]
        minima = dia["day"]["mintemp_c"]
        maxima = dia["day"]["maxtemp_c"]

        html += f"""
        <div class="card">
            <p><strong>{data_formatada}</strong></p>
            <img src="https:{icone}" width="48">
            <p>{minima:.1f}°C / {maxima:.1f}°C</p>
            <p>{condicao_traduzida}</p>
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

    for cidade_nome, cidade_api in CIDADES.items():
        html += f"<div class='cidade'><h2>{cidade_nome}</h2>"
        html += gerar_previsao(cidade_nome, cidade_api)
        html += "</div>"

    html += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    gerar_html()
