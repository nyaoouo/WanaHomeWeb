import configparser
from django.conf import settings

config_file = settings.BASE_DIR / 'config.ini'
config = configparser.ConfigParser()
config.read(config_file,encoding='utf-8')


def save():
    with open(config_file, 'w+',encoding='utf-8') as f:
        config.write(f)
