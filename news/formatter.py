NUM_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def format_news(source_name, source_emoji, news_list):
    """Formatea una lista de noticias (titulo, url) en mensajes individuales para Telegram."""
    if not news_list:
        return [f"{source_emoji} {source_name}\n\n😕 No se encontraron noticias"]

    messages = [f"{source_emoji} {source_name}\n"]
    for i, (title, url) in enumerate(news_list):
        emoji = NUM_EMOJIS[i] if i < len(NUM_EMOJIS) else "▸"
        messages.append(f"{emoji} {title}\n🔗 {url}")

    messages.append("━━━━━━━━━━━━━━━\n🤖 report_news bot")
    return messages
