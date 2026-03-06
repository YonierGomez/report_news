# ── Stage 1: Build dependencies ────────────────────────────────
FROM alpine AS builder

RUN apk add --no-cache python3 py3-pip python3-dev gcc musl-dev && \
    python3 -m venv /opt/prod && \
    source /opt/prod/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests telebot bs4 googlenewsdecoder

# ── Stage 2: Runtime ───────────────────────────────────────────
FROM alpine

LABEL maintainer="Yonier Gómez"

ENV user=botpro \
    TOKEN="" \
    CMD="source /opt/prod/bin/activate"

RUN apk add --no-cache python3 && adduser $user -D -h /app

COPY --from=builder /opt/prod /opt/prod

WORKDIR /app

USER $user

ADD news ./news
ADD bot.py .

HEALTHCHECK --interval=60s --timeout=10s --retries=3 --start-period=10s \
    CMD python3 -c "import requests; requests.get('https://api.telegram.org', timeout=5)" || exit 1

ENTRYPOINT ["sh", "-c", "$CMD && python3 bot.py"]
