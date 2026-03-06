Web scrapping para obtener noticias a través de un bot en telegram, hecho en Python.
======================  

![GitHub stars](https://img.shields.io/github/stars/YonierGomez/report_news?style=flat-square) ![GitHub forks](https://img.shields.io/github/forks/YonierGomez/report_news?style=flat-square) ![GitHub issues](https://img.shields.io/github/issues/YonierGomez/report_news?style=flat-square) ![GitHub license](https://img.shields.io/github/license/YonierGomez/report_news?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/YonierGomez/report_news?style=flat-square) ![GitHub top language](https://img.shields.io/github/languages/top/YonierGomez/report_news?style=flat-square) ![Docker Pulls](https://img.shields.io/docker/pulls/neytor/report_news?style=flat-square) ![Docker Image Size](https://img.shields.io/docker/image-size/neytor/report_news/latest?style=flat-square) ![Alpine Linux](https://img.shields.io/badge/base-Alpine%20Linux-0D597F?style=flat-square&logo=alpinelinux&logoColor=white) ![Python](https://img.shields.io/badge/python-3-3776AB?style=flat-square&logo=python&logoColor=white) ![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)

🌐 **Landing:** [https://yoniergomez.github.io/report_news](https://yoniergomez.github.io/report_news) · 🏠 **Web:** [https://www.yonier.com](https://www.yonier.com)

## Referencia rápida
* [¿Qué es web scraping?](#qué-es-web-scraping)
* [¿Cuál es nuestro uso?](#cuál-es-nuestro-uso)
* [¿Cómo usar esta imagen?](#cómo-usar-esta-imagen)
* [Arquitectura soportada](#arquitectura-soportada)
* [Variables](#variables)
* [Te invito a visitar mi web](#te-invito-a-visitar-mi-web)


## ¿Qué es web scraping?

### Definición Wikipedia

Web scraping o raspado web es una técnica utilizada mediante programas de software para extraer información de sitios web.​ Usualmente, estos programas simulan la navegación de un humano en la World Wide Web ya sea utilizando el protocolo HTTP manualmente, o incrustando un navegador en una aplicación.  

> [Web scrapping Wikipedia](https://es.wikipedia.org/wiki/Web_scraping)


![webscrapping](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGI2maqCgnSssWxwTySWiW-vzs0JXpyW0oXg&usqp=CAU)
  

## ¿Cuál es nuestro uso?

Este scraper fue construido en python y tiene como finalidad obtener noticias de las fuentes ["applesfera", "fayer wayer", "google news", "muylinux", "xataka", "xataka_android"] usando un bot en Telegram.
  

## ¿Cómo usar esta imagen?

Puede hacer uso de docker cli o docker compose

### Requisitos indispensables

Crea un BOT en telegram y cuando ejecutes el contenedor llama a la variable `-e TOKEN=token_obtenido_del_bot"`
  
### docker-compose (recomendado)

```yaml
---
version: '3'
services:
  report_news:
    image: neytor/report_news
    container_name: report_new_container
    restart: always
    environment:
      - TOKEN=tu_token_del_bot_de_telegram #OBLIGATORIO
      - user=botpro  #OPCIONAL
...
```

> Nota: Puedes reemplazar environment por env_file y pasarle un archivo .env como valor, recuerde que el archivo .env debe tener las variables deseadas.

### docker cli

```bash
docker container run \
   --name report_news -e TOKEN=tu_token_del_bot_de_telegram
   -d neytor/report_news
```

## Arquitectura soportada

La imagen es multi-arch. Docker descarga la versión correcta automáticamente.

| Arquitectura | Plataforma | Dispositivos |
| ------------ | ---------------- | ----------------------------------- |
| x86-64 | `linux/amd64` | PCs, servidores |
| ARM64 | `linux/arm64` | Raspberry Pi 3/4/5, Apple Silicon |
| ARMv7 | `linux/arm/v7` | Raspberry Pi 2, IoT |

## Variables
Puedes pasar las siguientes variables al crear el contenedor

| Variable | Función |
| ------------- | ------------------------------------------------------------ |
| `-e TOKEN` |**Obligatorio:** Es el token obtenido del BOT que creaste en TELEGRAM |
| `-e user` | Define el usuario para login - por defecto es botpro |
 

## Environment variables desde archivo (Docker secrets)


Se recomienda pasar la variable `TOKEN`a través de un archivo.

## Te invito a visitar mi web

Puedes ver nuevos eventos en [https://www.yonier.com/](https://www.yonier.com)
