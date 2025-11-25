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

    server = smtplplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    server.sendmail(os.environ["EMAIL_USER"], os.environ["EMAIL_DEST"], msg.as_string())
    server.quit()


def buscar_ultima_movimentacao():
    session = requests.Session()

    # 1) GET inicial para pegar ViewState real
    r1 = session.get(URL_LISTVIEW, timeout=30)
    soup1 = BeautifulSoup(r1.text, "html.parser")

    viewstate = soup1.find("input", {"id": "javax.faces.ViewState"})
    if not viewstate:
        return "VIEWSTATE não encontrado"
    viewstate = viewstate.get("value")

    # 2) Form Data real obtido por você
    data = {
        "AJAXREQUEST": "fPP",
        "_viewRoot": "",
        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": PROCESSO,
        "mascaraProcessoReferenciaRadio": "on",
        "fPP:j_id161:processoReferenciaInput": "",
        "fPP:dnp:nomeParte": "",
        "fPP:j_id179:nomeSocial": "",
        "fPP:j_id188:alcunha": "",
        "fPP:j_id197:nomeAdv": "",
        "fPP:j_id206:classeProcessualProcessoHidden": "",
        "tipoMascaraDocumento": "on",
        "fPP:dpDec:documentoParte": "",
        "fPP:Decoration:numeroOAB": "",
        "fPP:Decoration:j_id241": "",
        "fPP:Decoration:estadoComboOAB": "org.jboss.seam.ui.NoSelectionConverter.noSelectionValue",
        "fPP": "fPP",
        "autoScroll": "",
        "javax.faces.ViewState": viewstate,
        "fPP:j_id247": "fPP:j_id247",
        "AJAX:EVENTS_COUNT": "1",
    }

    headers = {
        "Faces-Request": "partial/ajax",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "Referer": URL_LISTVIEW,
        "Accept": "*/*"
    }

    # 3) POST — idêntico ao navegador
    r2 = session.post(URL_LISTVIEW, data=data, headers=headers, timeout=30)

    soup2 = BeautifulSoup(r2.text, "html.parser")

    update_nodes = soup2.find_all("update")

    html_fragment = ""
    for node in update_nodes:
        if node.get("id") and "processosGridPanel" in node.get("id"):
            html_fragment = node.text
            break

    if not html_fragment:
        return "Tabela não retornada pelo servidor."

    soup3 = BeautifulSoup(html_fragment, "html.parser")

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
