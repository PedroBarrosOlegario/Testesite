import os
import requests
from bs4 import BeautifulSoup

URL = "https://www4.tjmg.jus.br/pje/ConsultaPublica/listView.seam"
NUM_PROCESSO = "5042180-26.2024.8.13.0079"
CAMINHO_ARQUIVO = "monitor/ultima.txt"


def extrair_ultima_movimentacao(html):
    """
    Lê o HTML de resultados e retorna a coluna da última movimentação.
    """

    soup = BeautifulSoup(html, "xml")  # parser compatível com GitHub Actions

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

    ultima_td = celulas[-1]
    texto = ultima_td.get_text(strip=True)

    return texto if texto else None


def pesquisar_processo():
    """
    Envia o número do processo ao TJMG e retorna o HTML.
    """

    session = requests.Session()

    # GET inicial apenas para cookies
    session.get(URL)

    # POST da pesquisa
    data = {
        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": NUM_PROCESSO,
        "fPP:j_id212": "Pesquisar"
    }

    response = session.post(URL, data=data)

    return response.text


def salvar_movimentacao(mov):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        f.write(mov)


def main():
    print("🔍 Pesquisando processo no TJMG...")

    html = pesquisar_processo()
    mov = extrair_ultima_movimentacao(html)

    if not mov:
        mov = "Movimentação não encontrada."

    salvar_movimentacao(mov)

    print("✅ Última movimentação salva em ultima.txt:")
    print(mov)


if __name__ == "__main__":
    main()
