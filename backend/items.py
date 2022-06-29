import logging
import requests

from typing import Any
from pathlib import Path

from backend.constants import CHUNK_SIZE


class ReleaseAsset:
    def __init__(self, asset_name: str, asset_id: str, download_url: str) -> None:
        """
        No private variables :/

        Args:
            asset_name: The name of the specific asset
            asset_id: The id of the asset
            download_url: The browser_download_url from the json download
        """
        self.asset_name: str = asset_name
        self.asset_id: str = asset_id
        self.download_url: str = download_url

    def download_asset(self, output_path: Path, chunk_size: int = CHUNK_SIZE) -> None:
        """
        Downloads self.download_url in chunks. If output_path is a directory, then
        the last part of the url is taken as the name.

        So if the output path is ./downloads and the url is
        https://github.com/mastercomfig/mastercomfig/releases/download/dev/autoexec.cfg,
        then the final saved file will be at ./downloads/autoexec.cfg

        Args:
            output_path (Path): Where to download the file
                A full path with a name
                https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name
            chunk_size (int): Chunk size to download the images
                Do this because downloading the files whole is very taxing on the system

        Returns:
            None
        """
        output_path = output_path.resolve()

        if output_path.is_dir():
            logging.info(f"Directory detected: {output_path}")
            output_path = output_path / Path(self.download_url).name  # pathlib works with urls pog

        r: requests.Response = requests.get(self.download_url)
        with open(output_path, 'wb') as file:
            logging.info(f"Downloading {self.download_url} to {output_path}")
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)

        return


class ReleaseItem:
    def __init__(self, release_name: str, release_id: str, unparsed_assets: list[Any]) -> None:
        """
        Args:
            release_name (str): The release name, so 9.7.0, dev, or 9.9.0 and so on
            release_id (str): Id of the specific release
            unparsed_assets (list[any]): The mess of assets json to be parsed and important
                parts saved
        """
        self.release_name: str = release_name
        self.release_id: str = release_id
        self.parsed_assets: list[ReleaseAsset] = []

        for asset in unparsed_assets:
            self.parsed_assets.append(self._sort_asset(asset))

    @staticmethod
    def _sort_asset(asset: dict[Any, Any]) -> ReleaseAsset:
        """
        Parses an asset's json and puts the needed information into a ReleaseAsset

        Args:
            asset (dict[Any, Any]): The asset in question to be parsed

        Returns:
            ReleaseAsset: The parsed, organized, and neet asset
        """
        asset_name: str = asset["name"]
        asset_id: str = asset["id"]
        asset_download_url: str = asset["browser_download_url"]
        return ReleaseAsset(asset_name, asset_id, asset_download_url)

    def list_assets(self) -> None:
        """
        Prints (and logs to a file) the asset names and what index they are in

        TODO: Make it return a list or dict so it may be printed elsewhere. Could also use another function for the dict

        Returns:
            None
        """
        for index, asset in enumerate(self.parsed_assets):
            logging.info(f"{index}: {asset.asset_name}")

    def download_assets(self, download_path: str | Path, choices: list[int]) -> None:
        """
        Where to go through the assets list and download them to any location
        passed through

        Args:
            download_path (str | Path): Where to download the asset to
            choices (list[int]): The numbers corresponding to what you would like to download
                The choices are listed by self.list_assets

        Returns:
            None
        """

        for choice in choices:
            self.parsed_assets[choice].download_asset(Path(download_path))
