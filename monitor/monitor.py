import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL_BASE = "https://pje-consulta-publica.tjmg.jus.br"
URL_LISTVIEW = URL_BASE + "/pje/ConsultaPublica/listView.seam"

PROCESSO = "5042180-26.2024.8.13.0079"

ULTIMO_ARQUIVO = os.path.join(os.path.dirname(__file__), "ultima.txt")


def enviar_email(mensagem):
    msg = MIMEMultipart()
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_DEST"]
    msg["Subject"] = "⚖️ Nova movimentação no processo TJMG"

    msg.attach(MIMEText(mensagem, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    server.sendmail(os.environ["EMAIL_USER"], os.environ["EMAIL_DEST"], msg.as_string())
    server.quit()


def buscar_ultima_movimentacao():
    session = requests.Session()

    # 1) Primeiro GET → pega ViewState
    r1 = session.get(URL_LISTVIEW, timeout=30)
    soup1 = BeautifulSoup(r1.text, "html.parser")

    viewstate_tag = soup1.find("input", {"id": "javax.faces.ViewState"})
    if not viewstate_tag:
        return "VIEWSTATE não encontrado"

    viewstate = viewstate_tag.get("value")

    # 2) POST AJAX simulando o botão Pesquisar
    data = {
        "javax.faces.ViewState": viewstate,
        "fPP": "fPP",
        "AJAXREQUEST": "fPP",
        "ajaxSingle": "fPP:searchProcessos",
        "fPP:searchProcessos": "fPP:searchProcessos",
        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": PROCESSO,
    }

    headers = {
        "Faces-Request": "partial/ajax",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": URL_LISTVIEW,
        "User-Agent": "Mozilla/5.0",
    }

    r2 = session.post(URL_LISTVIEW, data=data, headers=headers, timeout=30)

    # 3) Interpretar partial-response usando html.parser
    soup2 = BeautifulSoup(r2.text, "html.parser")

    # O conteúdo vem dentro de <update id="fPP:processosGridPanel">
    updates = soup2.find_all("update")

    html_fragment = ""
    for upd in updates:
        if upd.get("id") and "processosGridPanel" in upd.get("id"):
            html_fragment = upd.text
            break

    if not html_fragment:
        return "Tabela não retornada pelo servidor."

    # 4) Parsear o fragmento HTML
    soup3 = BeautifulSoup(html_fragment, "html.parser")

    # A célula da última movimentação termina com :j_id264
    td = soup3.find("td", id=lambda x: x and x.endswith(":j_id264"))
    if not td:
        return "Movimentação não encontrada."

    return td.get_text(strip=True)


def main():
    atual = buscar_ultima_movimentacao()

    try:
        with open(ULTIMO_ARQUIVO, "r", encoding="utf-8") as f:
            ultimo = f.read().strip()
    except:
        ultimo = ""

    if atual != ultimo:
        enviar_email("Nova movimentação encontrada:\n\n" + atual)
        with open(ULTIMO_ARQUIVO, "w", encoding="utf-8") as f:
            f.write(atual)


if __name__ == "__main__":
    main()
