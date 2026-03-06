NUM_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def format_news(source_name, source_emoji, news_list):
    """Formatea una lista de noticias (titulo, url) en un mensaje bonito para Telegram."""
    if not news_list:
        return f"{source_emoji} {source_name}\n\n😕 No se encontraron noticias"

    lines = [f"{source_emoji} {source_name}\n"]
    for i, (title, url) in enumerate(news_list):
        emoji = NUM_EMOJIS[i] if i < len(NUM_EMOJIS) else f"▸"
        lines.append(f"{emoji} {title}")
        lines.append(f"🔗 {url}\n")

    lines.append("━━━━━━━━━━━━━━━")
    lines.append("🤖 report_news bot")
    return "\n".join(lines)
