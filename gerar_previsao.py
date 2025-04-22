import requests
from datetime import datetime
from string import Template

API_KEY = "c9ebb63d5d0e47e19fe15122225190481"
CIDADE = "Ilha Comprida"
URL = f"http://api.weatherapi.com/v1/forecast.json?q={CIDADE}&days=4&lang=pt&key={API_KEY}"

def buscar_previsao():
    resposta = requests.get(URL)
    resposta.raise_for_status()
    return resposta.json()

def gerar_html(dados):
    with open("index_base.html", "r", encoding="utf-8") as arquivo:
        base_html = Template(arquivo.read())

    cards_html = ""
    for dia in dados["forecast"]["forecastday"]:
        data_formatada = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%A, %d/%m")
        data_formatada = traduzir_dia(data_formatada)
        icone = "https:" + dia["day"]["condition"]["icon"]
        minima = dia["day"]["mintemp_c"]
        maxima = dia["day"]["maxtemp_c"]

        cards_html += f"""
        <div class="day-card">
            <h2>{data_formatada}</h2>
            <img src="{icone}" alt="Ícone do clima">
            <p>{minima:.1f}°C / {maxima:.1f}°C</p>
        </div>
        """

    pagina_html = base_html.substitute(PREVISAO_TEMPO=cards_html)
    with open("index.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(pagina_html)

def traduzir_dia(texto):
    traducoes = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    for en, pt in traducoes.items():
        if en in texto:
            texto = texto.replace(en, pt)
    return texto

if __name__ == "__main__":
    dados = buscar_previsao()
    gerar_html(dados)
