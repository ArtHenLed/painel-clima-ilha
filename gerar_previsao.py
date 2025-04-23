import requests
from datetime import datetime
from pathlib import Path

# Configurações
API_KEY = "c9ebb63d5d0e47e19fe15122225190481"
CIDADE = "Ilha Comprida"
URL = f"https://api.weatherapi.com/v1/forecast.json?q={CIDADE}&days=3&lang=pt&key={API_KEY}"

def buscar_previsao():
    resposta = requests.get(URL)
    resposta.raise_for_status()
    return resposta.json()

def obter_icone(condicao):
    # Usa o ícone da WeatherAPI (URL já vem no JSON)
    return condicao["icon"]

def gerar_html():
    dados = buscar_previsao()
    previsoes = dados["forecast"]["forecastday"]
    cards = []

    for dia in previsoes:
        data_obj = datetime.strptime(dia["date"], "%Y-%m-%d")
        dia_semana = data_obj.strftime("%A")
        dia_semana_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }[dia_semana]

        data_formatada = f'{dia_semana_pt}, {data_obj.strftime("%d/%m")}'
        icone_url = "https:" + obter_icone(dia["day"]["condition"])
        temp_min = round(dia["day"]["mintemp_c"], 1)
        temp_max = round(dia["day"]["maxtemp_c"], 1)

        card = f"""
        <div class="day-card">
            <h2>{data_formatada}</h2>
            <img src="{icone_url}" alt="Ícone do clima" />
            <p>{temp_min}°C / {temp_max}°C</p>
        </div>
        """
        cards.append(card)

    return "\n".join(cards)

def main():
    # Caminhos dos arquivos
    base_path = Path(__file__).parent
    html_base_path = base_path / "index_base.html"
    html_saida_path = base_path / "index.html"

    # Lê o HTML base e insere as previsões
    with open(html_base_path, "r", encoding="utf-8") as f:
        html_base = f.read()

    previsao_html = gerar_html()
    html_final = html_base.replace("{{PREVISAO_TEMPO}}", previsao_html)

    with open(html_saida_path, "w", encoding="utf-8") as f:
        f.write(html_final)

if __name__ == "__main__":
    main()
