import telebot
from news import (
    news_apple_sfera,
    news_fayer,
    news_google,
    news_muylinux,
    news_xataka,
    news_xataka_android,
    news_distrowatch,
    news_genbeta,
    news_hipertextual,
    news_computerhoy,
    news_wwwhatsnew,
    news_microsiervos,
    news_omicrono,
    news_itsfoss,
    news_omgubuntu,
    news_arstechnica,
    config
)
from news.formatter import format_news

bot = telebot.TeleBot(config.VAR_TOKEN)

# ── Registro de fuentes por categoría ──────────────────────────

SOURCES = {
    # Tecnología general (ES)
    '/xataka':       ('Xataka', '💻', lambda: news_xataka.news('https://www.xataka.com/')),
    '/genbeta':      ('Genbeta', '⚡', lambda: news_genbeta.news('https://www.genbeta.com/categoria/actualidad')),
    '/hipertextual': ('Hipertextual', '📡', lambda: news_hipertextual.news('https://hipertextual.com/tecnologia')),
    '/computerhoy':  ('Computer Hoy', '🖥️', lambda: news_computerhoy.news('https://computerhoy.20minutos.es/')),
    '/omicrono':     ('Omicrono', '🔬', lambda: news_omicrono.news('https://www.elespanol.com/omicrono/')),
    '/fayer':        ('Fayer Wayer', '🌐', lambda: news_fayer.news('https://www.fayerwayer.com/internet/', 'https://www.fayerwayer.com')),
    # Apple & Android
    '/applesfera':   ('Apple Esfera', '🍏', lambda: news_apple_sfera.news('https://www.applesfera.com/')),
    '/xatakandroid': ('Xataka Android', '🤖', lambda: news_xataka_android.news('https://www.xatakandroid.com/')),

    # Linux & Open Source
    '/muylinux':     ('Muy Linux', '🐧', lambda: news_muylinux.news('https://www.muylinux.com/')),
    '/distrowatch':  ('DistroWatch', '🐧', lambda: news_distrowatch.news('https://distrowatch.com/')),
    '/itsfoss':      ('Its FOSS', '🟢', lambda: news_itsfoss.news('https://itsfoss.com/')),
    '/omgubuntu':    ('OMG! Ubuntu', '🟠', lambda: news_omgubuntu.news('https://www.omgubuntu.co.uk/')),

    # IA & Ciencia
    '/wwwhatsnew':   ('Wwwhats new', '🆕', lambda: news_wwwhatsnew.news('https://wwwhatsnew.com/')),
    '/microsiervos': ('Microsiervos', '🔭', lambda: news_microsiervos.news('https://www.microsiervos.com/')),
    '/arstechnica':  ('Ars Technica AI', '🧠', lambda: news_arstechnica.news('https://arstechnica.com/ai/')),

    # Agregadores
    '/google':       ('Google News', '📰', lambda: news_google.news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/articles/')),
}

CATEGORIES = {
    '💻 Tecnología': ['/xataka', '/genbeta', '/hipertextual', '/computerhoy', '/omicrono', '/fayer'],
    '📱 Apple & Android': ['/applesfera', '/xatakandroid'],
    '🐧 Linux & Open Source': ['/muylinux', '/distrowatch', '/itsfoss', '/omgubuntu'],
    '🧠 IA & Ciencia': ['/wwwhatsnew', '/microsiervos', '/arstechnica'],
    '📰 Agregadores': ['/google'],
}


# ── Funciones del bot ──────────────────────────────────────────

def send_news(message, source_name, source_emoji, news_list):
    """Envía noticias formateadas con preview de cada link."""
    for msg in format_news(source_name, source_emoji, news_list):
        bot.send_message(message.chat.id, msg)


def handle_source(message, cmd):
    """Maneja cualquier comando de fuente."""
    name, emoji, fetcher = SOURCES[cmd]
    print(f'{name} - Principales noticias')
    result = fetcher()
    send_news(message, name, emoji, result)


def get_cmd(message):
    """Mensaje de bienvenida con menú por categorías."""
    lines = ["🤖 *report\\_news bot*\n"]
    lines.append("Selecciona una fuente de noticias:\n")
    for cat_name, cmds in CATEGORIES.items():
        lines.append(f"*{cat_name}*")
        for cmd in cmds:
            name = SOURCES[cmd][0]
            emoji = SOURCES[cmd][1]
            lines.append(f"  {emoji} {cmd} \\- {name}")
        lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("💡 Escribe cualquier comando para ver las noticias")
    bot.send_message(message.chat.id, "\n".join(lines), parse_mode='MarkdownV2')


# ── Mapeo de comandos ──────────────────────────────────────────

command_functions = {cmd: lambda msg, c=cmd: handle_source(msg, c) for cmd in SOURCES}
command_functions['/start'] = get_cmd

comandos_sin_slash = [cmd[1:] for cmd in command_functions]


@bot.message_handler(commands=comandos_sin_slash)
def handle_commands(message):
    command = message.text.split()[0]
    if command in command_functions:
        command_functions[command](message)
    else:
        bot.send_message(message.chat.id, 'Comando no válido')


@bot.message_handler(content_types=['text'])
def no_found_command(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, f'Comando {message.text} no disponible')
    else:
        cmds = ', '.join(command_functions.keys())
        bot.send_message(message.chat.id, f"Los comandos disponibles son {cmds}")


if __name__ == '__main__':
    bot_commands = []
    for cat_name, cmds in CATEGORIES.items():
        for cmd in cmds:
            name = SOURCES[cmd][0]
            bot_commands.append(telebot.types.BotCommand(cmd, f"{cat_name.split(' ', 1)[0]} {name}"))
    bot_commands.append(telebot.types.BotCommand("/start", "Menú principal"))

    bot.set_my_commands(bot_commands)
    print('=' * 100)
    print('Iniciando Bot - report_news')
    print(f'Fuentes registradas: {len(SOURCES)}')
    print('=' * 100)
    bot.infinity_polling()
