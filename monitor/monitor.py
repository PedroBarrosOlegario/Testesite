import os
import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=ba079116e770156e1656d647dfd34a44018e461e9fa107a5"
ULTIMO_ARQUIVO = os.path.join(os.path.dirname(__file__), "ultima.txt")

def pegar_movimentacoes():
    html = requests.get(URL, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    div_mov = soup.find("div", {"id": "j_id145:processoEventoPanel"})
    if not div_mov:
        return "Movimentações não encontradas."
    return div_mov.get_text(separator="\n", strip=True)

def enviar_email(mensagem):
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    servidor.sendmail(
        os.environ["EMAIL_USER"],
        os.environ["EMAIL_DEST"],
        f"Subject: ⚖️ Nova movimentação no processo TJMG\n\n{mensagem}"
    )
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
