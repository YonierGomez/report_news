Web scrapping para obtener noticias a través de un bot en telegram, hecho en Python.
======================  
## Referencia rápida
* [¿Qué es web scraping?](#qué-es-web-scraping)
* [¿Cuál es nuestro uso?](#cuál-es-nuestro-uso)
* [¿Cómo usar esta imagen?](#cómo-usar-esta-imagen)
* [Arquitectura soportada](#arquitectura-soportada)
* [Variables](#variables)
* [Uso en raspberry](#uso-en-raspberry)
* [Te invito a visitar mi web](#te-invito-a-visitar-mi-web)


## ¿Qué es web scraping?

### Definición Wikipedia

Web scraping o raspado web es una técnica utilizada mediante programas de software para extraer información de sitios web.​ Usualmente, estos programas simulan la navegación de un humano en la World Wide Web ya sea utilizando el protocolo HTTP manualmente, o incrustando un navegador en una aplicación.  

> [Web scrapping Wikipedia](https://es.wikipedia.org/wiki/Web_scraping)


![webscrapping](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGI2maqCgnSssWxwTySWiW-vzs0JXpyW0oXg&usqp=CAU)
  

## ¿Cuál es nuestro uso?

Este scraper fue construido en python y tiene como finalidad obtener noticias de las fuentes ["applesfera", "fayer wayer", "google news", "muylinux", "xataka", "xataka_android"] usando un bot en Telegram.  

![Polymart Downloads](https://img.shields.io/polymart/downloads/323)
  

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
La arquitectura soportada es la siguiente:

| Arquitectura | Disponible | Tag descarga |
| ------------ | ---------- | ---------------------------- |
| x86-64 | ✅ | docker pull neytor/report_news |
| arm64 | ✅ | docker pull neytor/report_news:arm |

## Variables
Puedes pasar las siguientes variables al crear el contenedor

| Variable | Función |
| ------------- | ------------------------------------------------------------ |
| `-e TOKEN` |**Obligatorio:** Es el token obtenido del BOT que creaste en TELEGRAM |
| `-e user` | Define el usuario para login - por defecto es botpro |
 

## Environment variables desde archivo (Docker secrets)


Se recomienda pasar la variable `TOKEN`a través de un archivo.

## Uso en Raspberry

Puedes utilizarla para cualquier raspberry pi

```bash
docker container run \
  --name report_news -e TOKEN=tu_token_del_bot_de_telegram
  -d neytor/report_news:arm
```

[![Try in PWD](https://github.com/play-with-docker/stacks/raw/cff22438cb4195ace27f9b15784bbb497047afa7/assets/images/button.png)](http://play-with-docker.com?stack=https://raw.githubusercontent.com/docker-library/docs/db214ae34137ab29c7574f5fbe01bc4eaea6da7e/wordpress/stack.yml)

## Te invito a visitar mi web

Puedes ver nuevos eventos en [https://www.yonier.com/](https://www.yonier.com)
