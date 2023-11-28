import time
from multiprocessing import Pool

import requests


def main():
    url = "https://pokeapi.co/api/v2/pokemon/{}"
    total_number = 200
    start = time.time()
    with Pool(5) as p:
        # [1,2,3,4,5,6]
        # map -> [1,2] [3,4] [5,6] -> assignes to each process
        # imap -> [1,2] -> assignes to the first process -> the second process asks for data -> [3,4] -> assignes to the second process
        _ = p.map(
            requests.get, [url.format(idx) for idx in range(total_number)], chunksize=2
        )
        # _ = p.imap(requests.get, [url.format(idx) for idx in range(total_number)], chunksize=2)
        # _ = p.imap_unordered(
        #     requests.get, [url.format(idx) for idx in range(total_number)], chunksize=2
        # )

    end = time.time()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
