import requests
from bs4 import BeautifulSoup

def download_html(URL):
    """Función para descargar el HTML de la página web."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        with requests.Session() as session:
            response = session.get(URL, headers=headers)
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as e:
        print('Error al descargar el HTML:', e)
        return None

def parse_news(html_content, URL):
    """Función para analizar el HTML y obtener las noticias."""
    soup = BeautifulSoup(html_content, 'html.parser')

    get_news = []
    for title in soup.find_all('td', class_='NewsHeadline'):
        link = title.find('a', href=True)
        if link is not None:
            get_news.append(f'*{title.text.strip()}: {URL + link["href"]}')

    return get_news

def get_distrowatch_news(message):
    """Función para obtener las noticias de Distrowatch."""
    # Descargar el HTML
    html_content = download_html('https://distrowatch.com/')
    
    # Verificar si se descargó el HTML correctamente
    if html_content is not None:
        # Parsear el HTML para obtener las noticias
        news_list = parse_news(html_content, 'https://distrowatch.com/')
        return news_list
    else:
        return []