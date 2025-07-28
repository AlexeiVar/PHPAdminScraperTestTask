import requests
from bs4 import BeautifulSoup
import dotenv
import os

dotenv.load_dotenv()

if __name__ == "__main__":
    with requests.Session() as s:
        # Парсер для супа
        parser = 'html.parser'
        # Получение токена для входа
        response = s.get(os.getenv('URL'))
        if response.status_code != 200:
            raise ConnectionError('Ошибка подключения к серверу')
        soup = BeautifulSoup(response.text, parser)
        token = soup.find('input', {'name': 'token'}).get('value')
        # Создаем тело запроса для входа
        body = {
            'pma_username': os.getenv('LOGIN'),
            'pma_password': os.getenv('PASSWORD'),
            'token': token
        }
        # Посылаем запрос на вход
        response = s.post(os.getenv('URL'), data=body)
        # Проверяем вошли или нет, поскольку так или иначе будет приходить 200 код
        if "list-group" not in response.text:
            raise ConnectionError('Не удалось войти на сайт')
        db = 'testDB'
        table = 'users'
        # Получаем нужную таблицу из нужной БД
        response = s.get(f'{os.getenv("URL")}/index.php?route=/sql&server=1&db={db}&table={table}')
        # Обрабатываем запрос и получаем по итогу строки
        soup = BeautifulSoup(response.text, parser)
        table = soup.find('tbody')
        rows = table.find_all('tr')
        data = []
        for row in rows:
            # Поскольку таблица проста, можно получить оба хранимых данных при помощи простого поиска по типу даты
            name = row.find('td', {'data-type': 'blob'}).text
            id = row.find('td', {'data-type': 'int'}).text
            data.append({'id': id, 'name': name})

        print(data)
