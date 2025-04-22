import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "c9ebb63d5d0e47e19fe151222251904"
CIDADE = "Ilha Comprida"
NOME_CIDADE = "Ilha Comprida"
INDEX_BASE = "index_base.html"
INDEX_FINAL = "index.html"

DIAS_SEMANA_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def buscar_previsao(cidade):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&units=metric&appid={API_KEY}&lang=pt_br"
    resposta = requests.get(url)
    resposta.raise_for_status()
    return resposta.json()

def extrair_dados(dados):
    zona = ZoneInfo("America/Sao_Paulo")
    hoje = datetime.now(tz=zona).date()
    dias_extraidos = {}
    
    for item in dados["list"]:
        datahora = datetime.fromtimestamp(item["dt"], tz=zona)
        data = datahora.date()
        hora = datahora.hour

        if data <= hoje:
            continue
        if hora != 12:
            continue
        if data not in dias_extraidos:
            dias_extraidos[data] = {
                "data_formatada": f"{DIAS_SEMANA_PT[datahora.strftime('%A')]}, {data.strftime('%d/%m')}",
                "icone": item["weather"][0]["icon"],
                "min": round(item["main"]["temp_min"], 1),
                "max": round(item["main"]["temp_max"], 1),
            }
        if len(dias_extraidos) == 4:
            break

    return list(dias_extraidos.values())

def gerar_html(dias):
    cards = ""
    for dia in dias:
        card = f"""
        <div class="day-card">
            <h2>{dia["data_formatada"]}</h2>
            <img src="https://openweathermap.org/img/wn/{dia["icone"]}@2x.png" alt="ícone clima">
            <p>{dia["min"]}°C / {dia["max"]}°C</p>
        </div>
        """
        cards += card

    with open(INDEX_BASE, "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{PREVISAO_TEMPO}}", cards)

    with open(INDEX_FINAL, "w", encoding="utf-8") as f:
        f.write(html_final)

if __name__ == "__main__":
    dados = buscar_previsao(CIDADE)
    dias = extrair_dados(dados)
    gerar_html(dias)
