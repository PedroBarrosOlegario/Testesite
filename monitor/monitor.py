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

    # 1) Primeiro GET para pegar ViewState
    r1 = session.get(URL_LISTVIEW, timeout=30)
    soup1 = BeautifulSoup(r1.text, "html.parser")

    viewstate = soup1.find("input", {"id": "javax.faces.ViewState"})
    if not viewstate:
        return "VIEWSTATE não encontrado"

    viewstate = viewstate.get("value")

    # 2) Montar POST AJAX idêntico ao do botão
    data = {
        "javax.faces.ViewState": viewstate,
        "fPP": "fPP",

        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": PROCESSO,

        # Parâmetro enviado pelo botão
        "fPP:searchProcessos": "fPP:searchProcessos",

        # Parâmetros RichFaces obrigatórios
        "AJAXREQUEST": "fPP",
        "ajaxSingle": "fPP:searchProcessos",
    }

    headers = {
        "Faces-Request": "partial/ajax",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": URL_LISTVIEW
    }

    r2 = session.post(URL_LISTVIEW, data=data, headers=headers, timeout=30)

    # 3) A resposta vem em XML (partial-response)
    soup2 = BeautifulSoup(r2.text, "xml")

    updates = soup2.find_all("update")

    html_fragment = ""
    for u in updates:
        if "id" in u.attrs and "processosGridPanel" in u["id"]:
            html_fragment = u.text
            break

    if not html_fragment:
        return "Tabela não encontrada (provavelmente o POST não simulou corretamente)."

    soup3 = BeautifulSoup(html_fragment, "html.parser")

    td = soup3.find("td", id=lambda x: x and x.endswith(":j_id264"))
    if not td:
        return "Movimentação não encontrada."

    return td.text.strip()


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
