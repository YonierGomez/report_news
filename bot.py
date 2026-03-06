import logging
import json
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    news_theverge,
    news_hackernews,
    news_techcrunch,
    news_thehackernews,
    news_krebsonsecurity,
    config
)
from news.formatter import format_news, format_search_results
from news import cache

# ── Logging ────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('report_news')

bot = telebot.TeleBot(config.VAR_TOKEN)

# ── Favoritos (persistencia simple en JSON) ────────────────────

FAVS_FILE = os.path.join(os.path.dirname(__file__), 'favorites.json')


def _load_favs():
    try:
        with open(FAVS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_favs(favs):
    with open(FAVS_FILE, 'w') as f:
        json.dump(favs, f)


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
    # Internacional (EN)
    '/theverge':     ('The Verge', '🔷', lambda: news_theverge.news('https://www.theverge.com/tech')),
    '/hackernews':   ('Hacker News', '🟧', lambda: news_hackernews.news('https://news.ycombinator.com/')),
    '/techcrunch':   ('TechCrunch', '💚', lambda: news_techcrunch.news('https://techcrunch.com/')),
    # Seguridad
    '/thehackernews': ('The Hacker News', '🔐', lambda: news_thehackernews.news('https://thehackernews.com/')),
    '/krebs':         ('Krebs on Security', '🛡️', lambda: news_krebsonsecurity.news('https://krebsonsecurity.com/')),
    # Agregadores
    '/google':       ('Google News', '📰', lambda: news_google.news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/')),
}

CATEGORIES = {
    '💻 Tecnología': ['/xataka', '/genbeta', '/hipertextual', '/computerhoy', '/omicrono', '/fayer'],
    '📱 Apple & Android': ['/applesfera', '/xatakandroid'],
    '🐧 Linux & Open Source': ['/muylinux', '/distrowatch', '/itsfoss', '/omgubuntu'],
    '🧠 IA & Ciencia': ['/wwwhatsnew', '/microsiervos', '/arstechnica'],
    '🌍 Internacional': ['/theverge', '/hackernews', '/techcrunch'],
    '🔒 Seguridad': ['/thehackernews', '/krebs'],
    '📰 Agregadores': ['/google'],
}

# Mapeo inverso: nombre de categoría corto -> key
CAT_KEYS = {
    'tecnologia': '💻 Tecnología',
    'apple': '📱 Apple & Android',
    'android': '📱 Apple & Android',
    'linux': '🐧 Linux & Open Source',
    'ia': '🧠 IA & Ciencia',
    'ciencia': '🧠 IA & Ciencia',
    'internacional': '🌍 Internacional',
    'seguridad': '🔒 Seguridad',
    'agregadores': '📰 Agregadores',
}


# ── Funciones del bot ──────────────────────────────────────────

def fetch_with_cache(cmd):
    """Obtiene noticias usando caché."""
    cached = cache.get(cmd)
    if cached is not None:
        return cached
    name, emoji, fetcher = SOURCES[cmd]
    try:
        result = fetcher() or []
        cache.set(cmd, result)
        return result
    except Exception as e:
        logger.error(f'Error en {name}: {e}')
        return None


def send_news(message, source_name, source_emoji, news_list, page=0):
    """Envía noticias formateadas con preview de cada link."""
    if news_list is None:
        bot.send_message(message.chat.id, f"{source_emoji} {source_name}\n\n⚠️ Fuente no disponible en este momento")
        return

    msgs = format_news(source_name, source_emoji, news_list, page=page)
    for msg in msgs:
        bot.send_message(message.chat.id, msg)

    # Botón "Ver más" si hay más noticias
    total = len(news_list)
    page_size = 10
    if total > (page + 1) * page_size:
        markup = InlineKeyboardMarkup()
        # Buscar el cmd por nombre
        cmd_key = None
        for k, v in SOURCES.items():
            if v[0] == source_name:
                cmd_key = k
                break
        if cmd_key:
            markup.add(InlineKeyboardButton("📄 Ver más", callback_data=f"more:{cmd_key}:{page + 1}"))
            bot.send_message(message.chat.id, "¿Quieres ver más noticias?", reply_markup=markup)


def handle_source(message, cmd):
    """Maneja cualquier comando de fuente."""
    name, emoji, _ = SOURCES[cmd]
    logger.info(f'{name} - solicitado por {message.from_user.first_name}')
    result = fetch_with_cache(cmd)
    send_news(message, name, emoji, result)


def build_main_menu():
    """Construye el teclado inline del menú principal."""
    markup = InlineKeyboardMarkup(row_width=2)
    for cat_name in CATEGORIES:
        # Extraer emoji y nombre corto
        parts = cat_name.split(' ', 1)
        emoji = parts[0]
        name = parts[1] if len(parts) > 1 else cat_name
        markup.add(InlineKeyboardButton(f"{emoji} {name}", callback_data=f"cat:{cat_name}"))
    markup.add(
        InlineKeyboardButton("🔍 Buscar", callback_data="action:search"),
        InlineKeyboardButton("⭐ Favoritos", callback_data="action:favs"),
    )
    return markup


def build_category_menu(cat_name):
    """Construye teclado inline para una categoría."""
    markup = InlineKeyboardMarkup(row_width=2)
    cmds = CATEGORIES.get(cat_name, [])
    for cmd in cmds:
        name, emoji, _ = SOURCES[cmd]
        markup.add(InlineKeyboardButton(f"{emoji} {name}", callback_data=f"src:{cmd}"))
    markup.add(
        InlineKeyboardButton("📚 Todas las fuentes", callback_data=f"all:{cat_name}"),
    )
    markup.add(InlineKeyboardButton("⬅️ Volver", callback_data="action:menu"))
    return markup


def get_cmd(message):
    """Mensaje de bienvenida con menú inline por categorías."""
    markup = build_main_menu()
    bot.send_message(
        message.chat.id,
        "🤖 *report\\_news bot*\n\nSelecciona una categoría:",
        parse_mode='MarkdownV2',
        reply_markup=markup
    )


# ── Callbacks de botones inline ────────────────────────────────

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data

    if data.startswith('cat:'):
        cat_name = data[4:]
        markup = build_category_menu(cat_name)
        bot.edit_message_text(
            f"{cat_name}\n\nElige una fuente o pulsa 'Todas':",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif data.startswith('src:'):
        cmd = data[4:]
        bot.answer_callback_query(call.id, "Cargando noticias...")
        if cmd in SOURCES:
            handle_source(call.message, cmd)

    elif data.startswith('all:'):
        cat_name = data[4:]
        bot.answer_callback_query(call.id, f"Cargando {cat_name}...")
        handle_todas_category(call.message, cat_name)

    elif data.startswith('more:'):
        parts = data.split(':')
        cmd = parts[1]
        page = int(parts[2])
        bot.answer_callback_query(call.id, "Cargando más...")
        if cmd in SOURCES:
            name, emoji, _ = SOURCES[cmd]
            result = fetch_with_cache(cmd)
            send_news(call.message, name, emoji, result, page=page)

    elif data == 'action:menu':
        markup = build_main_menu()
        bot.edit_message_text(
            "🤖 *report\\_news bot*\n\nSelecciona una categoría:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='MarkdownV2',
            reply_markup=markup
        )

    elif data == 'action:search':
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "🔍 Escribe el término de búsqueda:")
        bot.register_next_step_handler(msg, process_search)

    elif data == 'action:favs':
        bot.answer_callback_query(call.id)
        show_favorites(call.message)

    elif data.startswith('fav_add:'):
        cmd = data[8:]
        add_favorite(call.message.chat.id, cmd)
        bot.answer_callback_query(call.id, f"⭐ {SOURCES[cmd][0]} agregado a favoritos")

    elif data.startswith('fav_rm:'):
        cmd = data[7:]
        remove_favorite(call.message.chat.id, cmd)
        bot.answer_callback_query(call.id, f"❌ {SOURCES[cmd][0]} eliminado de favoritos")
        show_favorites(call.message)


# ── /todas - Todas las fuentes de una categoría ────────────────

def handle_todas_category(message, cat_name):
    """Ejecuta todas las fuentes de una categoría."""
    cmds = CATEGORIES.get(cat_name, [])
    if not cmds:
        bot.send_message(message.chat.id, "❌ Categoría no encontrada")
        return

    bot.send_message(message.chat.id, f"📡 Cargando {cat_name}...")
    for cmd in cmds:
        name, emoji, _ = SOURCES[cmd]
        result = fetch_with_cache(cmd)
        send_news(message, name, emoji, result)


@bot.message_handler(commands=['todas'])
def cmd_todas(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        # Mostrar categorías disponibles
        lines = ["📚 Uso: /todas <categoría>\n\nCategorías disponibles:"]
        for alias, cat in CAT_KEYS.items():
            lines.append(f"  • {alias}")
        bot.send_message(message.chat.id, "\n".join(lines))
        return

    query = parts[1].lower().strip()
    cat_name = CAT_KEYS.get(query)
    if not cat_name:
        bot.send_message(message.chat.id, f"❌ Categoría '{query}' no encontrada. Usa /todas para ver opciones.")
        return

    handle_todas_category(message, cat_name)


# ── /buscar - Búsqueda en todas las fuentes ────────────────────

def process_search(message):
    """Procesa el término de búsqueda."""
    query = message.text.strip().lower()
    if not query or query.startswith('/'):
        bot.send_message(message.chat.id, "❌ Término de búsqueda no válido")
        return

    bot.send_message(message.chat.id, f"🔍 Buscando '{query}' en todas las fuentes...")
    results = []

    for cmd, (name, emoji, _) in SOURCES.items():
        try:
            news_list = fetch_with_cache(cmd)
            if news_list:
                for title, url in news_list:
                    if query in title.lower():
                        results.append((name, title, url))
        except Exception as e:
            logger.error(f'Error buscando en {name}: {e}')

    for msg in format_search_results(query, results[:10]):
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        msg = bot.send_message(message.chat.id, "🔍 Escribe el término de búsqueda:")
        bot.register_next_step_handler(msg, process_search)
    else:
        # Crear un mensaje fake con el texto de búsqueda
        message.text = parts[1]
        process_search(message)


# ── /favoritos - Fuentes favoritas del usuario ─────────────────

def add_favorite(chat_id, cmd):
    favs = _load_favs()
    key = str(chat_id)
    if key not in favs:
        favs[key] = []
    if cmd not in favs[key]:
        favs[key].append(cmd)
    _save_favs(favs)


def remove_favorite(chat_id, cmd):
    favs = _load_favs()
    key = str(chat_id)
    if key in favs and cmd in favs[key]:
        favs[key].remove(cmd)
    _save_favs(favs)


def get_favorites(chat_id):
    favs = _load_favs()
    return favs.get(str(chat_id), [])


def show_favorites(message):
    user_favs = get_favorites(message.chat.id)
    if not user_favs:
        # Mostrar botones para agregar favoritos
        markup = InlineKeyboardMarkup(row_width=2)
        for cmd, (name, emoji, _) in SOURCES.items():
            markup.add(InlineKeyboardButton(f"{emoji} {name}", callback_data=f"fav_add:{cmd}"))
        markup.add(InlineKeyboardButton("⬅️ Volver", callback_data="action:menu"))
        bot.send_message(message.chat.id, "⭐ No tienes favoritos aún.\n\nToca una fuente para agregarla:", reply_markup=markup)
        return

    # Mostrar favoritos con opción de ejecutar o eliminar
    markup = InlineKeyboardMarkup(row_width=1)
    for cmd in user_favs:
        if cmd in SOURCES:
            name, emoji, _ = SOURCES[cmd]
            markup.add(
                InlineKeyboardButton(f"{emoji} {name}", callback_data=f"src:{cmd}"),
                InlineKeyboardButton(f"❌ Quitar", callback_data=f"fav_rm:{cmd}"),
            )
    markup.add(InlineKeyboardButton("➕ Agregar más", callback_data="action:fav_add_menu"))
    markup.add(InlineKeyboardButton("📡 Ver todas mis favoritas", callback_data="action:fav_all"))
    markup.add(InlineKeyboardButton("⬅️ Volver", callback_data="action:menu"))
    bot.send_message(message.chat.id, "⭐ Tus fuentes favoritas:", reply_markup=markup)


@bot.message_handler(commands=['favoritos'])
def cmd_favoritos(message):
    show_favorites(message)


# ── Callbacks adicionales de favoritos ─────────────────────────

@bot.callback_query_handler(func=lambda call: call.data == 'action:fav_add_menu')
def fav_add_menu(call):
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=2)
    user_favs = get_favorites(call.message.chat.id)
    for cmd, (name, emoji, _) in SOURCES.items():
        if cmd not in user_favs:
            markup.add(InlineKeyboardButton(f"{emoji} {name}", callback_data=f"fav_add:{cmd}"))
    markup.add(InlineKeyboardButton("⬅️ Volver", callback_data="action:favs"))
    bot.edit_message_text(
        "➕ Selecciona fuentes para agregar a favoritos:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'action:fav_all')
def fav_all(call):
    bot.answer_callback_query(call.id, "Cargando favoritas...")
    user_favs = get_favorites(call.message.chat.id)
    if not user_favs:
        bot.send_message(call.message.chat.id, "⭐ No tienes favoritos configurados")
        return
    bot.send_message(call.message.chat.id, "⭐ Cargando tus fuentes favoritas...")
    for cmd in user_favs:
        if cmd in SOURCES:
            name, emoji, _ = SOURCES[cmd]
            result = fetch_with_cache(cmd)
            send_news(call.message, name, emoji, result)


# ── Mapeo de comandos de texto ─────────────────────────────────

command_functions = {cmd: lambda msg, c=cmd: handle_source(msg, c) for cmd in SOURCES}
command_functions['/start'] = get_cmd
command_functions['/todas'] = cmd_todas
command_functions['/buscar'] = cmd_buscar
command_functions['/favoritos'] = cmd_favoritos

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
        markup = build_main_menu()
        bot.send_message(
            message.chat.id,
            "🤖 Usa los botones o escribe un comando.\n\nEscribe /start para ver el menú.",
            reply_markup=markup
        )


# ── Inicio ─────────────────────────────────────────────────────

if __name__ == '__main__':
    bot_commands = []
    for cat_name, cmds in CATEGORIES.items():
        for cmd in cmds:
            name = SOURCES[cmd][0]
            bot_commands.append(telebot.types.BotCommand(cmd, f"{cat_name.split(' ', 1)[0]} {name}"))
    bot_commands.append(telebot.types.BotCommand("/todas", "📚 Todas las noticias de una categoría"))
    bot_commands.append(telebot.types.BotCommand("/buscar", "🔍 Buscar en todas las fuentes"))
    bot_commands.append(telebot.types.BotCommand("/favoritos", "⭐ Tus fuentes favoritas"))
    bot_commands.append(telebot.types.BotCommand("/start", "🏠 Menú principal"))

    bot.set_my_commands(bot_commands)
    logger.info('=' * 60)
    logger.info('Iniciando Bot - report_news')
    logger.info(f'Fuentes registradas: {len(SOURCES)}')
    logger.info(f'Categorías: {len(CATEGORIES)}')
    logger.info('=' * 60)
    bot.infinity_polling()
