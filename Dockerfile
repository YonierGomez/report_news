FROM alpine

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="6493247672:AAELFqWHbi2EbYKvrrRc6Wg-N_U8-9YaC4w"

# Instalar dependencias del sistema y Python
RUN apk update && apk upgrade && \
    apk add --no-cache \
        python3 \
        py3-pip \
        chromium \
        chromium-chromedriver \
        # Dependencias adicionales para Selenium y otros paquetes
        libffi-dev \
        openssl-dev \
        gcc \
        musl-dev \
        libxml2-dev \
        libxslt-dev \
        zlib-dev \
        jpeg-dev \
        # Necesario para Selenium con Chrome
        dbus \
        ttf-freefont \
        # Necesario para evitar errores de Selenium
        xvfb \
        && \
    # Crear un entorno virtual
    python3 -m venv /opt/prod && \
    # Instalar dependencias de Python en el entorno virtual
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