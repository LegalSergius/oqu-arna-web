import random

from django.core.cache import cache

LENGHT_CODE = 6

CODE_LIFETIME = 300

def generate_code():
    n = random.randint(1000000, 9999999)
    return str(n)

def save_code(key, code):
    cache.set(key, code, timeout=CODE_LIFETIME)

def get_code(key):
    return cache.get(key)

def delete_code(key):
    cache.delete(key)