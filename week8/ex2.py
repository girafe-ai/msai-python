import time
from concurrent.futures import ThreadPoolExecutor

import requests


def main():
    url = "https://pokeapi.co/api/v2/pokemon/{}"
    total_number = 50
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        responses = executor.map(
            requests.get, [url.format(idx) for idx in range(total_number)]
        )
    end = time.time()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
