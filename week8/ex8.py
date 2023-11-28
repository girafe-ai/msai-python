import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

import requests


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def task(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        result = list(executor.map(requests.get, urls))
    return result


def main():
    url = "https://pokeapi.co/api/v2/pokemon/{}"
    total_number = 200
    start = time.time()

    urls = []
    for idx in range(total_number):
        urls.append(url.format(idx))

    with Pool(5) as p:
        results = p.map(task, list(chunker(urls, 50)))

    end = time.time()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
