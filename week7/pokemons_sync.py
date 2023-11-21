from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--root",
        required=False,
        type=str,
        default="images-sync",
        help="Root directory of the dataset",
    )
    return parser.parse_args()


def download_and_save(url: Optional[str], path: Path) -> None:
    response = requests.get(url)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)


def main():
    args = get_args()
    # option1: os
    # os.makedirs(args.root, exist_ok=True)

    # option2: pathlib
    root = Path(args.root)
    root.mkdir(exist_ok=True)

    url = "https://pokeapi.co/api/v2/pokemon/{}"
    # total_number = 897
    total_number = 100

    for idx in tqdm(
        range(total_number), desc="Downloading pokemons", total=total_number
    ):
        try:
            response = requests.get(url.format(idx))
            response.raise_for_status()
            pokemon_response = response.json()
        except requests.HTTPError:
            print(f"cannot download {idx}")
            continue
        try:
            pokemon_name = pokemon_response["name"]
            image_path = pokemon_response["sprites"]["other"]["official-artwork"][
                "front_default"
            ]
            download_and_save(image_path, root / f"{pokemon_name}.png")
        except requests.exceptions.MissingSchema:
            print(f"image path is None for {pokemon_name}")
        except requests.HTTPError:
            print(f"cannot download image for {pokemon_name}")
        except KeyError:
            print(f"dict is invalid for {pokemon_name}")


if __name__ == "__main__":
    main()
