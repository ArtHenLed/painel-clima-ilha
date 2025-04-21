import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "c9ebb63d5d0e47e19fe151222251904"
CIDADE = "Ilha Comprida"
DIAS = 4

DIAS_SEMANA_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def obter_previsao(cidade):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days={DIAS}&lang=en"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados["forecast"]["forecastday"]

def gerar_html():
    previsoes = obter_previsao(CIDADE)
    html_cards = ""

    for dia in previsoes:
        data = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana = DIAS_SEMANA_PT[data.strftime("%A")]
        data_formatada = f"{dia_semana}, {data.day:02d}/{data.month:02d}"
        icone = dia["day"]["condition"]["icon"]
        minima = round(dia["day"]["mintemp_c"], 1)
        maxima = round(dia["day"]["maxtemp_c"], 1)

        html_cards += f"""
        <div class="day-card">
            <h2>{data_formatada}</h2>
            <img src="https:{icone}" alt="Ícone">
            <p>{minima:.1f}°C / {maxima:.1f}°C</p>
        </div>
        """

    with open("index_base.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{PREVISAO_TEMPO}}", html_cards)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)

if __name__ == "__main__":
    gerar_html()
