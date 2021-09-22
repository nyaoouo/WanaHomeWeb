from .Config import config
from requests import post

host = config.get('recaptcha', 'host', fallback='')
public_key = config.get('recaptcha', 'public', fallback='')
private_key = config.get('recaptcha', 'private', fallback='')

prepare = host and public_key and private_key

url = r"https://{}/recaptcha/api/siteverify".format(host)


def validate(token: str):
    return post(url, {'secret': private_key, 'response': token}).json()['success']
