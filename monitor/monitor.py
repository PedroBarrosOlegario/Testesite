import os
import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=ba079116e770156e1656d647dfd34a44018e461e9fa107a5"
ULTIMO_ARQUIVO = "ultima.txt"

def pegar_movimentacoes():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")

    # Localiza a div que contém as movimentações
    div_mov = soup.find("div", {"id": "j_id145:processoEventoPanel"})
    if not div_mov:
        return "Movimentações não encontradas."

    # Extrai o texto da div
    return div_mov.get_text(strip=True)

def enviar_email(mensagem):
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    servidor.sendmail(
        os.environ["EMAIL_USER"],
        os.environ["EMAIL_DEST"],
        f"Subject: Nova movimentação\n\n{mensagem}"
    )
    servidor.quit()

texto_atual = pegar_movimentacoes()

try:
    with open(ULTIMO_ARQUIVO, "r") as f:
        ultimo = f.read()
except FileNotFoundError:
    ultimo = ""

if texto_atual != ultimo:
    enviar_email("Houve nova movimentação!\n\n" + texto_atual)
    with open(ULTIMO_ARQUIVO, "w") as f:
        f.write(texto_atual)
