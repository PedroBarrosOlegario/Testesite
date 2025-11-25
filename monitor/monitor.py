import os
import requests
from bs4 import BeautifulSoup

URL = "https://www4.tjmg.jus.br/pje/ConsultaPublica/listView.seam"  # página de pesquisa
NUM_PROCESSO = "5042180-26.2024.8.13.0079"
CAMINHO_ARQUIVO = "monitor/ultima.txt"


def extrair_ultima_movimentacao(html):
    """
    Lê o HTML da página de resultados e retorna SOMENTE
    o texto da coluna 'Última movimentação'.
    """

    soup = BeautifulSoup(html, "lxml-xml")  # XHTML precisa do parser XML

    # Seleciona a tabela principal
    tabela = soup.find("table", {"id": "fPP:processosTable"})
    if not tabela:
        return None

    # tbody > tr > último td
    linha = tabela.find("tbody").find("tr")
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
    Envia o número do processo para a pesquisa e retorna o HTML da tabela.
    """
    session = requests.Session()

    # Primeiro GET para obter a página (necessário para pegar cookies)
    session.get(URL)

    # Parâmetros da requisição POST de pesquisa
    data = {
        "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": NUM_PROCESSO,
        "fPP:j_id212": "Pesquisar"  # botão de pesquisar
    }

    # Faz o POST com o número do processo
    response = session.post(URL, data=data)

    return response.text


def salvar_movimentacao(mov):
    """
    Salva a movimentação em ultima.txt
    """
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
