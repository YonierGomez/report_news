Web scrapping para obtener noticias a través de un bot en telegram, hecho en Python.
======================  

![GitHub stars](https://img.shields.io/github/stars/YonierGomez/report_news?style=flat-square) ![GitHub forks](https://img.shields.io/github/forks/YonierGomez/report_news?style=flat-square) ![GitHub issues](https://img.shields.io/github/issues/YonierGomez/report_news?style=flat-square) ![GitHub license](https://img.shields.io/github/license/YonierGomez/report_news?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/YonierGomez/report_news?style=flat-square) ![GitHub top language](https://img.shields.io/github/languages/top/YonierGomez/report_news?style=flat-square) ![Docker Pulls](https://img.shields.io/docker/pulls/neytor/report_news?style=flat-square) ![Docker Image Size](https://img.shields.io/docker/image-size/neytor/report_news/latest?style=flat-square) ![Alpine Linux](https://img.shields.io/badge/base-Alpine%20Linux-0D597F?style=flat-square&logo=alpinelinux&logoColor=white) ![Python](https://img.shields.io/badge/python-3-3776AB?style=flat-square&logo=python&logoColor=white) ![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)

🌐 **Landing:** [https://yoniergomez.github.io/report_news](https://yoniergomez.github.io/report_news) · 🏠 **Web:** [https://www.yonier.com](https://www.yonier.com)

## Referencia rápida
* [¿Qué es web scraping?](#qué-es-web-scraping)
* [Fuentes de noticias](#fuentes-de-noticias)
* [Funcionalidades](#funcionalidades)
* [¿Cómo usar esta imagen?](#cómo-usar-esta-imagen)
* [Arquitectura soportada](#arquitectura-soportada)
* [Variables](#variables)

## ¿Qué es web scraping?

Web scraping o raspado web es una técnica utilizada mediante programas de software para extraer información de sitios web.

> [Web scrapping Wikipedia](https://es.wikipedia.org/wiki/Web_scraping)

## Fuentes de noticias

| Categoría | Fuentes |
|---|---|
| 💻 Tecnología | Xataka, Genbeta, Hipertextual, Computer Hoy, Omicrono, Fayer Wayer |
| 📱 Apple & Android | Apple Esfera, Xataka Android |
| 🐧 Linux & Open Source | Muy Linux, DistroWatch, Its FOSS, OMG! Ubuntu |
| 🧠 IA & Ciencia | Wwwhats new, Microsiervos, Ars Technica AI |
| 🌍 Internacional | The Verge, Hacker News, TechCrunch |
| 🔒 Seguridad | The Hacker News, Krebs on Security |

## Funcionalidades

- 🔘 **Menú interactivo** con botones inline de Telegram (no solo comandos de texto)
- 📚 `/todas <categoría>` para ver todas las fuentes de una categoría de un golpe
- 🔍 `/buscar <término>` para buscar noticias por palabra clave en todas las fuentes
- ⭐ `/favoritos` para guardar tus fuentes preferidas y consultarlas rápido
- 📄 **Paginación** con botón "Ver más" si hay más de 10 noticias
- ⚡ **Caché** de 15 minutos para respuestas rápidas sin re-scrapear
- 🛡️ **Error handling** por fuente: si un scraper falla, el bot sigue funcionando
- 📋 **Logging** estructurado con niveles (info/warning/error)
- 🔗 **Preview de links** en Telegram (cada noticia se envía como mensaje individual)


## ¿Cómo usar esta imagen?

### Requisitos

Crea un BOT en Telegram y obtén el token.

### docker-compose (recomendado)

```yaml
services:
  report_news:
    image: neytor/report_news
    container_name: report_news
    restart: unless-stopped
    environment:
      - TOKEN=tu_token_del_bot_de_telegram
    healthcheck:
      test: ["CMD", "python3", "-c", "import requests; requests.get('https://api.telegram.org', timeout=5)"]
      interval: 60s
      timeout: 10s
      retries: 3
```

### docker cli

```bash
docker run -d --name report_news -e TOKEN=tu_token_del_bot neytor/report_news
```

## Arquitectura soportada

La imagen es multi-arch. Docker descarga la versión correcta automáticamente.

| Arquitectura | Plataforma | Dispositivos |
|---|---|---|
| x86-64 | `linux/amd64` | PCs, servidores |
| ARM64 | `linux/arm64` | Raspberry Pi 3/4/5, Apple Silicon |
| ARMv7 | `linux/arm/v7` | Raspberry Pi 2, IoT |

## Variables

| Variable | Función |
|---|---|
| `-e TOKEN` | **Obligatorio:** Token del BOT de Telegram |
| `-e user` | Usuario del contenedor (default: botpro) |

## CI/CD

- **Docker build automático** cada lunes o al detectar nueva versión de Alpine Linux
- **Health check semanal** de todos los scrapers con creación automática de issues si alguno falla
- **Multi-arch build** con Docker Buildx (amd64, arm64, armv7)

## Te invito a visitar mi web

[https://www.yonier.com](https://www.yonier.com)
