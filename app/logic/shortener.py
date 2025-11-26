
import string
from secrets import choice

ALPHABET: str = string.ascii_letters + string.digits

def generate_slug(longurl: str):
    slug = ""
    for _ in range(6):
        slug+=choice(ALPHABET)
    return slug


