import requests
from pathlib import Path
from time import time

BASE_PATH = Path(__file__).parent


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r


def write_file(response):
    filename = BASE_PATH / 'cache' / response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

    print(f'Download took {time() - t0} sec')


if __name__ == '__main__':
    main()
