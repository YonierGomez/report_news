FROM alpine:latest

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="6493247672:AAELFqWHbi2EbYKvrrRc6Wg-N_U8-9YaC4w" \
    CMD="source /opt/prod/bin/activate"

# Install required packages including Chrome and ChromeDriver
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
    && python3 -m venv /opt/prod \
    && source /opt/prod/bin/activate \
    && pip install --upgrade pip \
    && pip3 install requests telebot bs4 selenium \
    && adduser $user -D -h /app

# Set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app

USER $user

ADD news ./news 
ADD bot.py .

# Set Chrome options for running in container
ENV PYTHONUNBUFFERED=1 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BIN=/usr/bin/chromium-browser

ENTRYPOINT ["sh", "-c", "$CMD && python3 bot.py"]