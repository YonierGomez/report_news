NUM_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def format_news(source_name, source_emoji, news_list, page=0, page_size=10):
    """Formatea noticias en mensajes individuales para Telegram con paginación."""
    if not news_list:
        return [f"{source_emoji} {source_name}\n\n😕 No se encontraron noticias"]

    total = len(news_list)
    start = page * page_size
    end = min(start + page_size, total)
    page_items = news_list[start:end]

    messages = [f"{source_emoji} {source_name}\n"]
    for i, (title, url) in enumerate(page_items):
        idx = start + i
        emoji = NUM_EMOJIS[idx] if idx < len(NUM_EMOJIS) else "▸"
        messages.append(f"{emoji} {title}\n🔗 {url}")

    footer = "━━━━━━━━━━━━━━━\n🤖 report_news bot"
    if total > end:
        footer += f"\n📄 Página {page + 1} de {(total + page_size - 1) // page_size}"
    messages.append(footer)
    return messages


def format_search_results(query, results):
    """Formatea resultados de búsqueda de múltiples fuentes."""
    if not results:
        return [f"🔍 Búsqueda: {query}\n\n😕 Sin resultados"]

    messages = [f"🔍 Resultados para: {query}\n"]
    for i, (source, title, url) in enumerate(results):
        emoji = NUM_EMOJIS[i] if i < len(NUM_EMOJIS) else "▸"
        messages.append(f"{emoji} [{source}] {title}\n🔗 {url}")

    messages.append("━━━━━━━━━━━━━━━\n🤖 report_news bot")
    return messages
