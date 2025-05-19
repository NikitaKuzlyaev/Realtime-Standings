from app.services.external.settings import Settings

key_filepath = "secrets/key.txt"
secret_filepath = "secrets/secret.txt"

KEY = ""
SECRET = ""

settings = Settings()

def initialize_secrets():
    with open(key_filepath, 'r') as key_file, open(secret_filepath) as secret_file:
        global KEY, SECRET
        KEY = key_file.readline().strip()
        SECRET = secret_file.readline().strip()