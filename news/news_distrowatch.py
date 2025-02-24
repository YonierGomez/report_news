from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  # Importar BeautifulSoup
import time

def get_distrowatch_news():
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

    return news_list

if __name__ == '__main__':
    news = get_distrowatch_news()

    if news:
        print("Noticias obtenidas:")
        for item in news:
            print(item)
    else:
        print("No se encontraron noticias.")