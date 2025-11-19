import os
import requests
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔐 Secrets do GitHub (injetados como variáveis de ambiente)
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID64 = os.getenv("STEAM_ID64")
EMAIL_USER = os.getenv("EMAIL_USER")   # seu e-mail Outlook
EMAIL_PASS = os.getenv("EMAIL_PASS")   # senha ou senha de app
EMAIL_DEST = os.getenv("EMAIL_DEST")   # destinatário

# Endpoints da Steam API
API_RECENT = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
API_OWNED = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
API_PLAYER = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"

def get_recent_games():
    params = {"key": STEAM_API_KEY, "steamid": STEAM_ID64}
    r = requests.get(API_RECENT, params=params)
    r.raise_for_status()
    return r.json().get("response", {}).get("games", [])

def get_owned_games():
    params = {"key": STEAM_API_KEY, "steamid": STEAM_ID64, "include_appinfo": True}
    r = requests.get(API_OWNED, params=params)
    r.raise_for_status()
    return r.json().get("response", {}).get("games", [])

def get_player_info():
    params = {"key": STEAM_API_KEY, "steamids": STEAM_ID64}
    r = requests.get(API_PLAYER, params=params)
    r.raise_for_status()
    players = r.json().get("response", {}).get("players", [])
    return players[0] if players else {}

def generate_report_html():
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=7)

    player = get_player_info()
    recent = get_recent_games()
    owned = get_owned_games()
    owned_dict = {g["appid"]: g for g in owned}

    html = []
    html.append("<h2>🎮 Relatório semanal da Steam</h2>")
    html.append(f"<p>Período: {inicio.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}</p>")

    # Info do perfil
    html.append("<h3>👤 Informações do perfil:</h3>")
    html.append(f"<p>Usuário: {player.get('personaname')}<br>")
    html.append(f"Perfil: <a href='{player.get('profileurl')}'>{player.get('profileurl')}</a><br>")
    if player.get("timecreated"):
        html.append(f"Conta criada em: {datetime.datetime.fromtimestamp(player['timecreated']).strftime('%d/%m/%Y')}</p>")

    # Jogos recentes
    html.append("<h3>📌 Jogos jogados nas últimas 2 semanas:</h3>")
    if not recent:
        html.append("<p>Nenhum jogo jogado recentemente.</p>")
    else:
        html.append("<ul>")
        for g in recent:
            nome = g.get("name", "Desconhecido")
            minutos = g.get("playtime_2weeks", 0)
            horas = minutos / 60
            total_horas = g.get("playtime_forever", 0) / 60

            appid = g.get("appid")
            icon_url = ""
            if appid in owned_dict and owned_dict[appid].get("img_icon_url"):
                icon_hash = owned_dict[appid]["img_icon_url"]
                icon_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg"

            if icon_url:
                html.append(
                    f"<li><img src='{icon_url}' width='32' height='32' style='vertical-align:middle;margin-right:8px;'>"
                    f"{nome}: {horas:.1f}h nas últimas 2 semanas | {total_horas:.1f}h total</li>"
                )
            else:
                html.append(f"<li>{nome}: {horas:.1f}h nas últimas 2 semanas | {total_horas:.1f}h total</li>")
        html.append("</ul>")

    # Estatísticas gerais
    html.append("<h3>📊 Estatísticas gerais da conta:</h3>")
    html.append(f"<p>Total de jogos na biblioteca: {len(owned)}<br>")
    total_horas = sum(g.get("playtime_forever", 0) for g in owned) / 60
    html.append(f"Tempo total jogado: {total_horas:.1f} horas</p>")

    return "".join(html)

def send_email(report_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DEST
    msg["Subject"] = "Relatório semanal da Steam"

    msg.attach(MIMEText(report_html, "html"))

    # Outlook usa TLS na porta 587
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    try:
        report_html = generate_report_html()
        print("Relatório gerado com sucesso.")
        send_email(report_html)
        print("E-mail enviado com sucesso via Outlook.")
    except Exception as e:
        print("Erro ao gerar ou enviar relatório:", e)
