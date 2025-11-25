# monitor/monitor.py
# Rodar no GitHub Actions - extrai a "Última movimentação" do PJe (TJMG)
# Requisitos: requests, beautifulsoup4
# Salva resultado em monitor/ultima.txt e envia email se houver mudança.

import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIG
URL_BASE = "https://pje-consulta-publica.tjmg.jus.br"
URL_LISTVIEW = URL_BASE + "/pje/ConsultaPublica/listView.seam"
PROCESSO = "5042180-26.2024.8.13.0079"  # coloque aqui seu processo ou leia de config
ARQUIVO_ULTIMO = os.path.join(os.path.dirname(__file__), "ultima.txt")
TIMEOUT = 30
RETRIES = 2
SLEEP_BETWEEN_RETRIES = 2  # segundos


def enviar_email(mensagem: str):
    """
    Envia email (usa variáveis de ambiente).
    EMAIL_USER, EMAIL_PASS, EMAIL_DEST
    """
    user = os.environ.get("EMAIL_USER")
    passwd = os.environ.get("EMAIL_PASS")
    dest = os.environ.get("EMAIL_DEST")

    if not (user and passwd and dest):
        print("Variáveis de e-mail não configuradas. Pulando envio de e-mail.")
        return

    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = dest
    msg["Subject"] = "⚖️ Nova movimentação no processo TJMG"
    msg.attach(MIMEText(mensagem, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.starttls()
        server.login(user, passwd)
        server.sendmail(user, dest, msg.as_string())
        server.quit()
        print("E-mail enviado para", dest)
    except Exception as e:
        print("Erro enviando e-mail:", e)


def extrair_hidden_inputs_da_form(html: str, form_id: str = "fPP") -> dict:
    """
    Recebe HTML (página inicial GET) e retorna dict com todos os inputs hidden
    encontrados dentro do <form id="fPP">. Retorna nomes->valores (valores podem ser '').
    """
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form", {"id": form_id})
    if not form:
        # tenta procurar por qualquer form que contenha o campo do processo
        forms = soup.find_all("form")
        for f in forms:
            if f.find("input", {"name": lambda n: n and n.startswith("fPP")}):
                form = f
                break

    hidden = {}
    if not form:
        print("Form", form_id, "não encontrado na página inicial.")
        return hidden

    inputs = form.find_all("input", {"type": "hidden"})
    for inp in inputs:
        name = inp.get("name")
        # alguns inputs podem vir sem name; ignorar
        if not name:
            continue
        value = inp.get("value", "")
        hidden[name] = value

    return hidden


def montar_dados_post(hidden_inputs: dict, processo: str) -> dict:
    """
    Monta o dict de dados para o POST AJAX:
    - começa com todos os hidden inputs do form
    - define o campo do número do processo
    - adiciona os campos AJAX necessários
    """
    data = dict(hidden_inputs)  # copia

    # Nome real do campo do número do processo (conforme HTML)
    campo_processo = "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso"
    data[campo_processo] = processo

    # Campos adicionais que o botão envia (capturados do DevTools)
    # Garantir que existam (alguns já podem estar no hidden_inputs)
    data["fPP"] = data.get("fPP", "fPP")
    data["fPP:searchProcessos"] = "fPP:searchProcessos"
    data["AJAXREQUEST"] = "fPP"
    data["ajaxSingle"] = "fPP:searchProcessos"
    data["_viewRoot"] = data.get("_viewRoot", "")
    # AJAX events count geralmente 1 quando um único evento é enviado
    data["AJAX:EVENTS_COUNT"] = data.get("AJAX:EVENTS_COUNT", "1")
    # alguns formulários adicionam esse campo; se não existir, adicionamos vazio
    data["autoScroll"] = data.get("autoScroll", "")

    # javax.faces.ViewState deve existir nos hidden inputs; se não, manter o que temos
    if "javax.faces.ViewState" not in data:
        data["javax.faces.ViewState"] = ""

    return data


def buscar_fragmento_por_partial_response(resp_text: str) -> str:
    """
    O servidor devolve um partial-response. Procuramos <update id="...processosGridPanel..."> e retornamos o fragmento HTML.
    """
    soup = BeautifulSoup(resp_text, "html.parser")
    updates = soup.find_all("update")
    for upd in updates:
        _id = upd.get("id", "")
        if "processosGridPanel" in _id:
            # .text traz o HTML interno do update
            return upd.text
    # fallback: se não encontrou update, tenta buscar por qualquer fragmento <div id="fPP:processosGridPanel">
    frag = soup.find(id=lambda x: x and "processosGridPanel" in x)
    if frag:
        return str(frag)
    return ""


def extrair_ultima_movimentacao_do_fragmento(html_fragment: str) -> str or None:
    """
    Recebe o fragmento HTML (string) e retorna o texto da célula cujo id termina com ':j_id264'.
    """
    if not html_fragment:
        return None
    soup = BeautifulSoup(html_fragment, "html.parser")
    td = soup.find("td", id=lambda x: x and x.endswith(":j_id264"))
    if not td:
        # como fallback, tentar pegar segunda td.rich-table-cell (caso fragmento seja só a tabela)
        cells = soup.find_all("td", {"class": "rich-table-cell"})
        if len(cells) >= 2:
            return cells[1].get_text(strip=True)
        return None
    return td.get_text(strip=True)


def buscar_ultima_movimentacao() -> str:
    """
    Função principal que realiza:
    1) GET inicial (pega hidden inputs & viewstate)
    2) monta data com todos os hidden inputs + campos do botão
    3) POST com header Faces-Request: partial/ajax
    4) interpreta partial-response e extrai a última movimentação
    """
    session = requests.Session()
    # Use a URL sem jsessionid; o session cuidará do JSESSIONID
    print("GET inicial em", URL_LISTVIEW)
    r_get = session.get(URL_LISTVIEW, timeout=TIMEOUT)
    if r_get.status_code != 200:
        raise RuntimeError(f"GET inicial retornou status {r_get.status_code}")

    hidden = extrair_hidden_inputs_da_form(r_get.text, form_id="fPP")
    print(f"Encontrados {len(hidden)} inputs hidden no form fPP (ex.: keys: {list(hidden.keys())[:6]})")

    # montar dados do POST
    data = montar_dados_post(hidden, PROCESSO)

    headers = {
        "Faces-Request": "partial/ajax",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": URL_LISTVIEW,
        "User-Agent": "Mozilla/5.0 (compatible)",
        "Accept": "*/*",
    }

    print("Enviando POST AJAX simulando o botão PESQUISAR...")
    r_post = session.post(URL_LISTVIEW, data=data, headers=headers, timeout=TIMEOUT)

    if r_post.status_code != 200:
        raise RuntimeError(f"POST retornou status {r_post.status_code}")

    # extrair fragmento da partial-response
    fragment = buscar_fragmento_por_partial_response(r_post.text)
    if not fragment:
        # debug: salvar resposta bruta para investigar
        debug_path = os.path.join(os.path.dirname(__file__), "debug_partial_response.html")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(r_post.text)
        print("DEBUG: partial-response salva em", debug_path)
        return "Tabela não retornada pelo servidor."

    # parsear fragmento e extrair a movimentação
    mov = extrair_ultima_movimentacao_do_fragmento(fragment)
    if not mov:
        return "Movimentação não encontrada."
    return mov


def salvar_ultima(mov_text: str):
    os.makedirs(os.path.dirname(ARQUIVO_ULTIMO), exist_ok=True)
    with open(ARQUIVO_ULTIMO, "w", encoding="utf-8") as f:
        f.write(mov_text)


def main():
    print("Iniciando monitoramento do processo:", PROCESSO)
    attempt = 0
    resultado = None
    while attempt <= RETRIES:
        try:
            resultado = buscar_ultima_movimentacao()
            break
        except Exception as e:
            print(f"Erro na tentativa {attempt+1}: {e}")
            attempt += 1
            time.sleep(SLEEP_BETWEEN_RETRIES)

    if resultado is None:
        resultado = "Erro ao obter movimentação."

    print("Resultado obtido:", resultado)

    # lê último salvo
    try:
        with open(ARQUIVO_ULTIMO, "r", encoding="utf-8") as f:
            ultimo = f.read().strip()
    except FileNotFoundError:
        ultimo = ""

    if resultado != ultimo:
        print("Mudança detectada (ou primeira execução). Enviando e-mail e salvando.")
        enviar_email("Nova movimentação encontrada:\n\n" + resultado)
        salvar_ultima(resultado)
    else:
        print("Nenhuma mudança detectada. Último salvo mantém-se.")

    print("Fim.")


if __name__ == "__main__":
    main()
