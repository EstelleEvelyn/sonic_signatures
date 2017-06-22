''' get texts from project gutenberg .py '''

from Gutenberg import*

from gutenberg.acquire import load_extet
from gutenberg.cleanup import strip_headers

text = strip_headers(load_extet(15399)).strip()
print(text)