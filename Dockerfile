FROM alpine

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="6493247672:AAELFqWHbi2EbYKvrrRc6Wg-N_U8-9YaC4w" \
    CMD="source /opt/prod/bin/activate"

# Instalar dependencias del sistema y Python
RUN apk update && apk upgrade && \
    apk add --no-cache python3 py3-pip chromium chromium-chromedriver && \
    python3 -m venv /opt/prod && \
    /opt/prod/bin/pip install --upgrade pip && \
    /opt/prod/bin/pip install requests telebot bs4 selenium

# Crear un usuario no root
RUN adduser -D -h /app $user

WORKDIR /app

# Copiar los archivos de la aplicación
COPY --chown=botpro:botpro news ./news
COPY --chown=botpro:botpro bot.py .

USER $user

# Ejecutar la aplicación
ENTRYPOINT ["sh", "-c", "/opt/prod/bin/python3 bot.py"]