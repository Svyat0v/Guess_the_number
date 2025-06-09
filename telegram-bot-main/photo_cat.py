import logging
import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")

url = f'https://api.thecatapi.com/v1/images/search?api_key={API_KEY}'


def get_photo_cat():
    """Получает новое изображение."""
    try:
        response = requests.get(url)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat
