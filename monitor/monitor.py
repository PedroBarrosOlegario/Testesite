import os
from playwright.sync_api import sync_playwright

URL = "https://pje-consulta-publica.tjmg.jus.br/"
NUM_PROCESSO = "5042180-26.2024.8.13.0079"
ULTIMO_ARQUIVO = os.path.join(os.path.dirname(__file__), "ultima.txt")


def pegar_movimentacao():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("➡ Acessando página...")
        page.goto(URL, timeout=60000)

        # Campo do número do processo
        input_selector = "#fPP\\:numProcesso-inputNumeroProcessoDecoration\\:numProcesso-inputNumeroProcesso"
        page.wait_for_selector(input_selector)

        print("➡ Preenchendo número do processo...")
        page.fill(input_selector, NUM_PROCESSO)

        print("➡ Clicando em pesquisar...")
        page.click("#fPP\\:searchProcessos")

        # Espera a tabela de resultados
        print("➡ Aguardando resultados...")
        page.wait_for_selector("#fPP\\:processosTable", timeout=60000)

        # Captura apenas a coluna “Última movimentação”
        print("➡ Extraindo última movimentação...")
        td_mov = page.query_selector("td[id$='j_id264']")

        if not td_mov:
            browser.close()
            return "Movimentação não encontrada."

        movimento = td_mov.inner_text().strip()

        browser.close()
        return movimento


def enviar_email(mensagem):
    from smtplib import SMTP
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_DEST"]
    msg["Subject"] = "⚖️ Nova movimentação no processo TJMG"

    msg.attach(MIMEText(mensagem, "plain", "utf-8"))

    servidor = SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    servidor.sendmail(os.environ["EMAIL_USER"], os.environ["EMAIL_DEST"], msg.as_string())
    servidor.quit()


def main():
    texto_atual = pegar_movimentacao()

    # Lê o último estado salvo
    try:
        with open(ULTIMO_ARQUIVO, "r", encoding="utf-8") as f:
            ultimo = f.read().strip()
    except FileNotFoundError:
        ultimo = ""

    # Se mudou, envia e-mail e salva
    if texto_atual and texto_atual != ultimo:
        print("✔ Mudança detectada! Enviando e-mail...")
        enviar_email("Houve nova movimentação no processo:\n\n" + texto_atual)

        with open(ULTIMO_ARQUIVO, "w", encoding="utf-8") as f:
            f.write(texto_atual)
    else:
        print("Nenhuma mudança detectada.")


if __name__ == "__main__":
    main()
