def get_distrowatch_news(message):
    URL = 'https://distrowatch.com/'
    
    # Configurar Selenium (asegúrate de tener el driver correcto instalado, por ejemplo, chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    driver.get(URL)
    time.sleep(5)  # Esperar a que la página cargue

    # Extraer el contenido de la página
    page_source = driver.page_source
    driver.quit()

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    news_list = []

    for headline in soup.find_all('td', class_='NewsHeadline'):
        title = headline.get_text(strip=True)
        link = headline.find('a', href=True)

        if link:
            link_url = link['href']
            full_url = f"https://distrowatch.com{link_url}"
            news_list.append(f"* {title}: {full_url}")

    # Enviar las noticias al chat
    if news_list:
        for news in news_list:
            bot.send_message(message.chat.id, news)
    else:
        bot.send_message(message.chat.id, "No se encontraron noticias.")
