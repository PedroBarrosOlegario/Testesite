import os
import requests
from bs4 import BeautifulSoup

URL = "https://www4.tjmg.jus.br/pje/ConsultaPublica/listView.seam"
NUM_PROCESSO = "5042180-26.2024.8.13.0079"
CAMINHO_ARQUIVO = "monitor/ultima.txt"


def extrair_ultima_movimentacao(html):
    """
    Lê o HTML retornado e pega a última movimentação da tabela principal.
    """

    soup = BeautifulSoup(html, "html.parser")  # parser 100% compatível no GitHub Actions

    tabela = soup.find("table", {"id": "fPP:processosTable"})
    if not tabela:
        return None

    tbody = tabela.find("tbody")
    if not tbody:
        return None

    linha = tbody.find("tr")
    if not linha:
        return None

    celulas = linha.find_all("td")
    if not celulas or len(celulas) < 3:
        return None

    ultima = celulas[-1].get_text(strip=True)
    return ultima if ultima else None


def pesquisar_processo():
    """
    Envia o número do processo e retorna o HTML da página com a tabela de resultados.
    """

    session = requests.Session()

    # GET inicial para pegar cookies
    session.get(URL, timeout=30)

    # POST para pesquisar
    data = {
        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": NUM_PROCESSO,
        "fPP:j_id212": "Pesquisar"
    }

    resp = session.post(URL, data=data, timeout=30)
    return resp.text


def salvar_movimentacao(mov):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arq:
        arq.write(mov)


def main():
    print("🔍 Pesquisando processo no TJMG...")

    html = pesquisar_processo()
    mov = extrair_ultima_movimentacao(html)

    if not mov:
        mov = "Movimentação não encontrada."

    salvar_movimentacao(mov)

    print("✅ Última movimentação salva:")
    print(mov)


if __name__ == "__main__":
    main()
