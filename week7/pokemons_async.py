import asyncio
import typing as tp
from argparse import ArgumentParser, Namespace
from io import BytesIO
from pathlib import Path

import httpx
import tqdm.asyncio
from PIL import Image


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--root",
        required=False,
        type=str,
        default="images",
        help="Root directory of the dataset",
    )
    return parser.parse_args()


async def download_image_path_and_pokemon_name(
    url: str, idx: int, client: httpx.AsyncClient
) -> tp.Tuple[str, str]:
    url_ = url.format(idx)
    response = await client.get(url=url_, timeout=5.0)
    pokemon_response = response.json()
    image_path = pokemon_response["sprites"]["other"]["official-artwork"][
        "front_default"
    ]
    return (image_path, pokemon_response["name"])


async def download_and_save_pokemon_image(
    name: Path, path: str, client: httpx.AsyncClient
) -> None:
    with BytesIO() as writer:
        async with client.stream("GET", path, timeout=10.0) as response:
            async for chunk in response.aiter_bytes():
                writer.write(chunk)
            writer.seek(0)

            # with open(name, "wb") as f:
            #     f.write(writer)
            Image.open(writer).save(name)


async def download(url: str, root: Path, total_number: int):
    async with httpx.AsyncClient() as client:
        tasks = []
        # create tasks
        for idx in range(1, total_number + 1):
            tasks.append(
                asyncio.create_task(
                    download_image_path_and_pokemon_name(
                        url=url, idx=idx, client=client
                    )
                )
            )

        # wait for them
        name2path = dict()

        # for f in asyncio.as_completed(tasks):
        for f in tqdm.asyncio.tqdm.as_completed(tasks):
            image_path, name = await f
            name2path[name] = image_path

        download_tasks = []
        for name, path in name2path.items():
            download_tasks.append(
                asyncio.create_task(
                    download_and_save_pokemon_image(root / f"{name}.png", path, client)
                )
            )

        for f in tqdm.asyncio.tqdm.as_completed(download_tasks):
            await f


def main():
    args = get_args()
    root = Path(args.root)
    root.mkdir(exist_ok=True)

    url = "https://pokeapi.co/api/v2/pokemon/{}"
    # total_number = 897
    total_number = 100
    asyncio.run(download(url, root, total_number))


if __name__ == "__main__":
    main()
