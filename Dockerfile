FROM alpine

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="6493247672:AAELFqWHbi2EbYKvrrRc6Wg-N_U8-9YaC4w" \
    CMD="source /opt/prod/bin/activate"

# Instalar dependencias necesarias
RUN apk update && apk upgrade && apk add --no-cache \
    python3 py3-pip \
    chromium chromium-chromedriver \
    xvfb \
    bash \
    && python3 -m venv /opt/prod && \
    /opt/prod/bin/pip install --upgrade pip && \
    /opt/prod/bin/pip install requests telebot bs4 selenium && \
    adduser $user -D -h /app

WORKDIR /app

USER $user

# Agregar archivos del proyecto
ADD news ./news
ADD bot.py .

# Ejecutar el bot con el entorno virtual activado
ENTRYPOINT ["sh", "-c", "source /opt/prod/bin/activate && python3 bot.py"]
