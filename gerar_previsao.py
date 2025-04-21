import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "sua_api_key_aqui"
CIDADES = {
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

def obter_previsao(cidade):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=4&lang=en"
    resposta = requests.get(url)
    return resposta.json()

def gerar_html():
    fuso_horario = ZoneInfo("America/Sao_Paulo")
    cards_html = ""

    for nome_exibicao, nome_api in CIDADES.items():
        dados = obter_previsao(nome_api)
        previsoes = dados["forecast"]["forecastday"]
        cards = ""

        for dia in previsoes:
            data = datetime.strptime(dia["date"], "%Y-%m-%d")
            dia_semana = DIAS_SEMANA_PT[data.strftime("%A")]
            data_formatada = f"{dia_semana}, {data.day:02d}/{data.month:02d}"
            icone = dia["day"]["condition"]["icon"]
            minima = dia["day"]["mintemp_c"]
            maxima = dia["day"]["maxtemp_c"]

            cards += f"""
                <div class="card">
                    <h3>{data_formatada}</h3>
                    <img src="https:{icone}" alt="Ícone">
                    <p>{minima:.1f}°C / {maxima:.1f}°C</p>
                </div>
            """

        cards_html += f"""
            <div class="cidade">
                <h2>Previsão do Tempo - {nome_exibicao}</h2>
                <div class="cards">{cards}</div>
            </div>
        """

    with open("index_base.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{PREVISAO_TEMPO}}", cards_html)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)

if __name__ == "__main__":
    gerar_html()
