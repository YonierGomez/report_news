FROM alpine

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="" \
    CMD="source /opt/prod/bin/activate"

RUN apk update && apk upgrade && apk add --no-cache python3 py3-pip && \
    python3 -m venv /opt/prod && $CMD && pip install --upgrade pip && \
    pip3 install requests telebot bs4 googlenewsdecoder && adduser $user -D -h /app

WORKDIR /app

USER $user

ADD news ./news
ADD bot.py .

ENTRYPOINT ["sh", "-c", "$CMD && python3 bot.py"]
