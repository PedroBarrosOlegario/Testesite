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

    html.append("<h3>📊 Estatísticas gerais da conta:</h3>")
    html.append(f"<p>Total de jogos na biblioteca: {len(owned)}</p>")
    total_horas = sum(g.get("playtime_forever", 0) for g in owned) / 60
    html.append(f"<p>Tempo total jogado: {total_horas:.1f} horas</p>")

    return "".join(html)

def send_email(report_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DEST
    msg["Subject"] = "Relatório semanal da Steam"

    # Corpo em HTML
    msg.attach(MIMEText(report_html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    try:
        report_html = generate_report_html()
        print(report_html)  # opcional: debug
        send_email(report_html)
    except Exception as e:
        print("Erro ao gerar ou enviar relatório:", e)
