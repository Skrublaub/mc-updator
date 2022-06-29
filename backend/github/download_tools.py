import requests
import zipfile
import logging

from pathlib import Path

from backend.constants import CHUNK_SIZE


def start_requests_session() -> requests.Session:
    session: requests.Session = requests.Session()
    # get a session object with the 1st page result
    return session


# This function has been replaced by ReleaseAsset.download_asset in items.py
def download_file(url: str, output_path: Path, chunk_size: int = CHUNK_SIZE) -> None:
    """
    Downloads a file in chunks. If output_path is a directory, then
    the last part of the url is taken as the name.

    Useless due to the asset class in items.py. Will leave here for later.

    So if the output path is ./downloads and the url is
    https://github.com/mastercomfig/mastercomfig/releases/download/dev/autoexec.cfg,
    then the final saved file will be at ./downloads/autoexec.cfg

    Args:
        url (str): The url to download
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
        output_path = output_path / Path(url).name  # pathlib works with urls pog

    r: requests.Response = requests.get(url)
    with open(output_path, 'wb') as file:
        logging.info(f"Downloading {url} to {output_path}")
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)

    return


def extract_zip(zip_file: Path, end_dir: Path, create_sub_folder: bool = True) -> Path:
    """
    Extracts a given zip file to a path. If create_sub_folder is True, the file will be
    extracted to end_dir / zip_file.stem. If create_sub_folder is False, the files will
    be extracted to end_dir

    Args:
        zip_file (Path): Path to the zip file
        end_dir (Path): Where to extract the file to
        create_sub_folder (bool): Whether to create a subfolder or not
            in end_dir

    Returns:
        Path: Path to the extracted folder

    Raises:
        NotADirectoryError: If end_dir isn't a directory
    """
    if not end_dir.is_dir():
        raise NotADirectoryError(f"{end_dir} is not a directory")

    if create_sub_folder:
        end_dir = end_dir / zip_file.stem
        end_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Extracting {zip_file} to {end_dir}")
    with zipfile.ZipFile(zip_file, 'r') as extract_file:
        extract_file.extractall(end_dir)

    return end_dir


#def get_

