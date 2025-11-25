import os
from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://pje-consulta-publica.tjmg.jus.br/"
NUM_PROCESSO = "5042180-26.2024.8.13.0079"
ULTIMO_ARQUIVO = os.path.join(os.path.dirname(__file__), "ultima.txt")


def pegar_movimentacao():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Acessar
        page.goto(URL, timeout=60000)

        # Preencher número do processo
        selector = "#fPP\\:numProcesso-inputNumeroProcessoDecoration\\:numProcesso-inputNumeroProcesso"
        page.wait_for_selector(selector)
        page.fill(selector, NUM_PROCESSO)

        # clicar pesquisar
        page.click("#fPP\\:searchProcessos")

        # aguarda resultados
        page.wait_for_selector("td.rich-table-cell", timeout=60000)

        # pega primeira célula que contém a última movimentação
        movimento = page.query_selector("td.rich-table-cell").inner_text()

        browser.close()
        return movimento.strip()


def enviar_email(mensagem: str):
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
    atual = pegar_movimentacao()

    try:
        with open(ULTIMO_ARQUIVO, "r", encoding="utf-8") as f:
            ultimo = f.read()
    except FileNotFoundError:
        ultimo = ""

    if atual != ultimo:
        print("Nova movimentação detectada!")
        enviar_email("Houve nova movimentação no processo:\n\n" + atual)

        with open(ULTIMO_ARQUIVO, "w", encoding="utf-8") as f:
            f.write(atual)


if __name__ == "__main__":
    main()
