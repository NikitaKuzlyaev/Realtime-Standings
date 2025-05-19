import hashlib
from urllib.parse import urlencode

import requests

from app.repository.auth.auth import set_previous_user_api_request

key_filepath = "secrets/key.txt"
secret_filepath = "secrets/secret.txt"

KEY = ""
SECRET = ""


def initialize_secrets():
    with open(key_filepath, 'r') as key_file, open(secret_filepath) as secret_file:
        global KEY, SECRET
        KEY = key_file.readline().strip()
        SECRET = secret_file.readline().strip()


def generate_api_sig(method_name, secret, params):
    params_sorted = sorted(params.items())
    param_str = urlencode(params_sorted)
    sign_str = f"123456/{method_name}?{param_str}#{secret}"

    return hashlib.sha512(sign_str.encode('utf-8')).hexdigest()


'''
https://codeforces.com/api/contest.status?contestId=566&asManager=true&from=1&count=10
'''


async def send_request_to_codeforces(user_id, secret, method_name, **params):
    rand = "123456"
    params["apiSig"] = rand + generate_api_sig(method_name, secret, params)

    print(params, '\n' * 10)

    url = f"https://codeforces.com/api/{method_name}"

    response = requests.get(url, params=params)

    await set_previous_user_api_request(user_id=user_id)

    if response.status_code == 200:
        print("Request successful.")
        with open('log.txt', 'w') as file:
            file.write(response.text)

        data = response.json()

        return response.text
    else:
        print(f"Failed to fetch data. Status code: {response.status_code} {response.json()}")
        return None


if __name__ == "__main__":
    initialize_secrets()

    while True:
        if input():
            send_request()
