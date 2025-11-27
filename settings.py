import os
from os.path import join, dirname
from dotenv import load_dotenv
import sqlite3

ENV_PATH = join(dirname(__file__), '.env')
DB_PATH = join(dirname(__file__), 'database/source.db')


# ==Загрзука секретов из файла==
load_dotenv(ENV_PATH)

API_TOKEN = os.environ.get("TOKEN")