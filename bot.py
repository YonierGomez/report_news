import telebot, threading
from news import (
    news_apple_sfera,
    news_muylinux,
    news_fayer,
    news_hipertextual,
    news_computerhoy,
    news_genbeta,
    news_xataka,
    news_google,
    news_xataka_android,
    # news_distrowatch,
    config
)

bot = telebot.TeleBot(config.VAR_TOKEN)

var_msj_news = 'Principales noticias Sr Yonier'
# Funciones para obtener noticias
def get_applesfera_news(message):
    print('Apple Esfera -', var_msj_news)
    print('='*130)
    for new in news_apple_sfera.news('https://www.applesfera.com/'):
        bot.send_message(message.chat.id, new)

# def get_distrowatch_news(message):
#     print('Distrowatch -', var_msj_news)
#     print('='*130)
#     for new in news_distrowatch.get_distrowatch_news(message):
#         bot.send_message(message.chat.id, new)

def get_fayer_news(message):
    print('Fayer Wayer -', var_msj_news)
    print('='*130)
    for new in news_fayer.news('https://www.fayerwayer.com/internet/', 'https://www.fayerwayer.com'):
        bot.send_message(message.chat.id, new)

def get_muylinux_news(message):
    print('Muy Linux -', var_msj_news)
    print('='*130)
    for new in news_muylinux.news('https://www.muylinux.com/'):
        bot.send_message(message.chat.id, new)

def get_google_news(message):
    print('Google -', var_msj_news)
    print('='*130)
    for new in news_google.news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/articles/'):
        bot.send_message(message.chat.id, new)

def get_xatakandroid_news(message):
    print('Xataka Android -', var_msj_news)
    print('='*130)
    for new in news_xataka.news('https://www.xatakandroid.com/'):
        bot.send_message(message.chat.id, new)

def get_xataka_news(message):
    print('Xataka -', var_msj_news)
    print('='*130)
    for new in news_xataka.news('https://www.xataka.com/'):
        bot.send_message(message.chat.id, new)

def get_genbeta_news(message):
    print('genbeta actualidad -', var_msj_news)
    print('='*130)
    for new in news_genbeta.news('https://www.genbeta.com/categoria/actualidad'):
        bot.send_message(message.chat.id, new)
        
def get_hipertextual_news(message):
    print('Hipertextual -', var_msj_news)
    print('='*130)
    for new in news_hipertextual.news('https://hipertextual.com/tecnologia'):
        bot.send_message(message.chat.id, new)

def get_computerhoy_news(message):
    print('computerhoy -', var_msj_news)
    print('='*130)
    for new in news_computerhoy.news('https://computerhoy.20minutos.es/'):
        bot.send_message(message.chat.id, new)


def get_cmd(message):
    print('Bienvenido al bot de Yonier')
    print('='*130)
    bot.send_message(message.chat.id, f"Bienvenid@, este BOT tiene como finalidad obtener noticias de tecnología, utiliza los siguientes comandos {', '.join(command_functions.keys())}")

# Diccionario que mapea comandos a funciones
command_functions = {
    '/applesfera': get_applesfera_news,
    '/hipertextual': get_hipertextual_news,
    '/computerhoy': get_computerhoy_news,
    '/muylinux': get_muylinux_news,
    '/xatakandroid': get_xatakandroid_news,
    '/genbeta': get_genbeta_news,
    '/xataka': get_xataka_news,
    '/fayer': get_fayer_news,
    '/google': get_google_news,
    '/start': get_cmd
    # '/distrowatch': get_distrowatch_news,
}

comandos_sin_slash = [comando[1:] for comando in command_functions.keys()]

@bot.message_handler(commands=comandos_sin_slash)
def handle_commands(message):
    command = message.text
    if command in command_functions:
        command_functions[command](message)
    else:
        bot.send_message(message.chat.id, 'Comando no válido')

@bot.message_handler(content_types=['text'])
def no_found_command(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, f'Comando {message.text} no disponible')
    else:
        list_command =  f"Los comandos disponibles son {', '.join(command_functions.keys())}"
        bot.send_message(message.chat.id, list_command )


if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/applesfera", "Noticias - Apple"),
        # telebot.types.BotCommand("/distrowatch", "Noticias - Distro Linux"),
        telebot.types.BotCommand("/hipertextual", "Noticias - Hipertextual"),
        telebot.types.BotCommand("/Computerhoy", "Noticias - Computerhoy"),
        telebot.types.BotCommand("/fayer", "Noticias - Fayer Wayer"),
        telebot.types.BotCommand("/muylinux", "Noticias - GNU/Linux"),
        telebot.types.BotCommand("/xatakandroid", "Noticias - Android"),
        telebot.types.BotCommand("/xataka", "Noticias - Xataka"),
        telebot.types.BotCommand("/genbeta", "Noticias - genbeta actualidad"),
        telebot.types.BotCommand("/google", "Noticias - Google Tecnología"),
        telebot.types.BotCommand("/start", "Bienvenido"),
    ])
    print('='*100)
    print('Iniciando Bot')
    print('='*100)
    bot.infinity_polling() #ESCUCHA O COMPRUEBA SI SE RECIBEN MSJ NUEVOS, TODO SE DETIENE AQUI,