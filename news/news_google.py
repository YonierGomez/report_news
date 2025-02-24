import requests
from bs4 import BeautifulSoup
import re

def clean_title(text):
    """Limpia y formatea el título de la noticia"""
    # Separa palabras que están pegadas por cambios de capitalización
    text = re.sub(r'(?<!^)(?=[A-Z][a-z])', ' ', text)
    
    # Elimina "Más" y "Hace X {unidad}" del título
    text = re.sub(r'Más|Hace \d+ \w+', '', text)
    
    # Elimina URLs codificadas
    text = re.sub(r'https?://\S+', '', text)
    
    # Elimina caracteres especiales y espacios múltiples
    text = re.sub(r'[^\w\s\.,:]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def news(URL, DOMAIN):
    """Función para obtener noticias de Google News"""
    try:
        r = requests.get(URL)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        get_news = []
        for r_title in soup.find_all(class_='PO9Zff', limit=15):
            # Obtiene y limpia el título
            title = clean_title(r_title.text)
            
            # Procesa la URL
            url = DOMAIN + r_title.a["href"]
            url = url.replace("./articles/", "")
            
            # Solo agrega la noticia si el título no está vacío después de la limpieza
            if title:
                get_news.append(f'* {title}\n  {url}')
        
        return get_news
    
    except requests.RequestException as e:
        print(f"Error al obtener las noticias: {e}")
        return []

if __name__ == '__main__':
    print('='*100)
    print('Google News - Principales noticias')
    print('='*100)
    
    news_url = 'https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419'
    domain = 'https://news.google.com/articles/'
    
    for new in news(news_url, domain):
        print(new)
        print('='*100)