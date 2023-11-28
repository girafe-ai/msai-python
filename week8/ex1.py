import time

import requests


def main():
    url = "https://pokeapi.co/api/v2/pokemon/{}"
    total_number = 100
    responses = []
    start = time.time()
    for idx in range(total_number):
        responses.append(requests.get(url.format(idx)))
    end = time.time()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
