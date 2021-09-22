import random
import string


def rand_char(length=32, char_field=string.ascii_letters + string.digits):
    return ''.join(random.choice(char_field) for _ in range(length))
