FROM alpine:latest

LABEL maintainer="Yonier Gómez"

# Definir variables de entorno
ENV user=botpro \
    TOKEN="6493247672:AAELFqWHbi2EbYKvrrRc6Wg-N_U8-9YaC4w" \
    VIRTUAL_ENV=/opt/prod \
    PATH="/opt/prod/bin:$PATH"

# Instalar dependencias y crear usuario
RUN apk update && apk upgrade && \
    apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    xvfb \
    dbus \
    ttf-freefont \
    mesa-gl \
    mesa-dri-gallium \
    udev \
    # Crear usuario y directorio de la aplicación
    && adduser -D -h /app $user \
    # Crear y configurar entorno virtual
    && python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
    && pip install requests telebot bs4 selenium \
    # Dar permisos al usuario sobre el entorno virtual
    && chown -R $user:$user $VIRTUAL_ENV \
    && chmod -R 755 $VIRTUAL_ENV

# Configurar variables para Chrome
ENV DISPLAY=:99 \
    PYTHONUNBUFFERED=1 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BIN=/usr/bin/chromium-browser

# Configurar directorio de trabajo
WORKDIR /app
RUN chown -R $user:$user /app

# Cambiar al usuario no privilegiado
USER $user

# Copiar archivos de la aplicación
COPY --chown=$user:$user news ./news 
COPY --chown=$user:$user bot.py .

# Iniciar la aplicación
CMD ["python3", "bot.py"]