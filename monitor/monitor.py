import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=ba079116e770156e1656d647dfd34a44018e461e9fa107a5"
ULTIMO_ARQUIVO = os.path.join(os.path.dirname(__file__), "ultima.txt")

def pegar_movimentacoes():
    # Faz a requisição ao site
    html = requests.get(URL, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    # Localiza a div que contém as movimentações
    div_mov = soup.find("div", {"id": "j_id145:processoEventoPanel"})
    if not div_mov:
        return "Movimentações não encontradas."

    # Extrai o texto da div, preservando quebras de linha
    return div_mov.get_text(separator="\n", strip=True)

def enviar_email(mensagem):
    # Monta o e-mail com suporte a UTF-8
    msg = MIMEMultipart()
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_DEST"]
    msg["Subject"] = "⚖️ Nova movimentação no processo TJMG"

    msg.attach(MIMEText(mensagem, "plain", "utf-8"))

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    servidor.sendmail(os.environ["EMAIL_USER"], os.environ["EMAIL_DEST"], msg.as_string())
    servidor.quit()

def main():
    texto_atual = pegar_movimentacoes()

    try:
        with open(ULTIMO_ARQUIVO, "r", encoding="utf-8") as f:
            ultimo = f.read()
    except FileNotFoundError:
        ultimo = ""

    if texto_atual and texto_atual != ultimo:
        enviar_email("Houve nova movimentação no processo!\n\n" + texto_atual)
        with open(ULTIMO_ARQUIVO, "w", encoding="utf-8") as f:
            f.write(texto_atual)

if __name__ == "__main__":
    main()
