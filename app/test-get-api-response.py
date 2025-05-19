import hashlib
import time
from urllib.parse import urlencode

import requests

from app.schema.codeforces import CodeforcesApiResponseBySubmissions

key_filepath = "secrets/key.txt"
secret_filepath = "secrets/secret.txt"

KEY = ""
SECRET = ""


def initialize_secrets():
    with open(key_filepath, 'r') as key_file, open(secret_filepath) as secret_file:
        global KEY, SECRET
        KEY = key_file.readline().strip()
        SECRET = secret_file.readline().strip()


def generate_api_sig(method_name, params):
    """Создает подпись для запроса (apiSig)"""
    # Формируем строку для подписи
    params_sorted = sorted(params.items())  # Сортируем параметры по ключу и значению
    param_str = urlencode(params_sorted)  # Преобразуем параметры в строку
    sign_str = f"123456/{method_name}?{param_str}#{SECRET}"

    # Генерируем SHA-512 хэш от строки
    return hashlib.sha512(sign_str.encode('utf-8')).hexdigest()


'''
https://codeforces.com/api/contest.status?contestId=566&asManager=true&from=1&count=10
'''


def send_request():
    # Параметры запроса
    method_name = "contest.status"  # Метод, к которому обращаемся
    contest_id = 573081
    from_index = 1
    count = 10

    # Текущее время (для параметра time)
    current_time = int(time.time())

    # Параметры запроса
    params = {
        "contestId": contest_id,
        "apiKey": KEY,
        "time": current_time,
        "from": from_index,
        "count": count
    }

    # Генерация случайного значения для rand (первые 6 символов подписи)
    rand = "123456"  # Можно заменить на случайную строку
    params["apiSig"] = rand + generate_api_sig(method_name, params)

    # URL API Codeforces
    url = f"https://codeforces.com/api/{method_name}"

    # Отправка GET-запроса
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request successful.")
        data = response.json()  # Получаем ответ в формате JSON

        # Маппинг ответа на структуру
        api_response = CodeforcesApiResponseBySubmissions.parse_obj(data)

        # Пример вывода результата
        for submission in api_response.result:
            print(f"Submission ID: {submission.id}, Verdict: {submission.verdict}, Problem: {submission.author.members[0].name} {submission.relative_time_seconds}")

        print(data)
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code} {response.json()}")
        return None


if __name__ == "__main__":
    initialize_secrets()

    while True:
        if input():
            send_request()
