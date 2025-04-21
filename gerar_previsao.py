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

TRADUCOES_CLIMA = {
    "Sunny": "Ensolarado",
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Overcast": "Encoberto",
    "Mist": "Névoa",
    "Patchy rain nearby": "Chuvas isoladas nas proximidades",
    "Patchy rain possible": "Possibilidade de chuva isolada",
    "Light rain shower": "Pancada de chuva leve",
    "Moderate rain": "Chuva moderada",
    "Heavy rain": "Chuva forte",
    "Showers": "Pancadas de chuva",
    "Rain": "Chuva",
}

def traduzir_condicao(condicao):
    return TRADUCOES_CLIMA.get(condicao, condicao)

def obter_previsao(cidade):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days={DIAS}&lang=en"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao obter dados: {response.text}")
        return "<p>Erro ao obter previsão</p>"

    dados = response.json()
    html = ""

    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%A, %d/%m")
        dia_semana_pt = DIAS_SEMANA_PT.get(data.split(',')[0], data.split(',')[0])
        condicao_en = dia["day"]["condition"]["text"]
        condicao = traduzir_condicao(condicao_en)
        icon = dia["day"]["condition"]["icon"]
        min_temp = round(dia["day"]["mintemp_c"], 1)
        max_temp = round(dia["day"]["maxtemp_c"], 1)

        html += f"""
        <div class="card">
            <strong>{dia_semana_pt}, {data.split(',')[1]}</strong>
            <img src="{icon}" alt="{condicao}" width="48"><br>
            <span>{min_temp}°C / {max_temp}°C</span>
            <p>{condicao}</p>
        </div>
        """
    return html

def gerar_html():
    with open("index_base.html", "r", encoding="utf-8") as f:
        template = f.read()

    bloco_previsao = obter_previsao(CIDADE)
    pagina_final = template.replace("{{PREVISAO_TEMPO}}", bloco_previsao)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(pagina_final)

if __name__ == "__main__":
    gerar_html()
