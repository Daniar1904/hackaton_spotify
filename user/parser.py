from bs4 import BeautifulSoup
from decorator import benchmark
import requests
import csv

count = 0


def get_html(url: str) -> str:
    """
    Получаем html код определенного сайта
    """
    response = requests.get(url)
    return response.text


def get_data(html: str) -> None:
    """
    Фукнция парсер получает все данные с сайта
    """
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    catalog = soup.find('div', class_='page-main__playlist-tracks-list')
    if not catalog:
        return False
    # print(catalog)
    sounds = catalog.find_all('div', class_='d-track typo-track d-track_selectable d-track_with-cover d-track_with-chart')
    for sound in sounds:
        title = sound.find('div', class_='d-track__name').text.strip()

        author = sound.find('span', class_='d-track__artists').text
        if not author:
            author = 'Нет автора'

        try:
            image = sound.find('img', class_='entity-cover__image deco-pane').get('src')
        except:
            image = 'Нет изображения'

        data = {
            'title': title,
            'author': author,
            'img': image
        }
        write_to_csv(data)
    return True


def write_to_csv(data: dict) -> None:
    """Функция для записи данных в csv файл"""
    global count
    with open('file.csv', 'a') as file:
        fieldnames = ['№', 'Название', 'Автор', 'Фото']
        writer = csv.DictWriter(file, fieldnames)
        count += 1
        writer.writerow({
            '№': count,
            'Название': data.get('title'),
            'Автор': data.get('author'),
            'Фото': data.get('img')
        })


def prepare_csv() -> None:
    """Подготавливает csv файл"""
    with open('file.csv', 'w') as file:
        fieldnames = ['№', 'Название', 'Автор', 'Фото']
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow({
            '№': '№',
            'Название': 'Название',
            'Автор': 'Автор',
            'Фото': 'Фото'
        })


@benchmark
def main():
    i = 1
    prepare_csv()
    while True:
        BASE_URL = f'https://music.yandex.ru/chart/'
        html = get_html(BASE_URL)
        is_res = get_data(html)
        if not is_res:
            break
        i += 1

main()