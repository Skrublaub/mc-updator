import requests
import zipfile
import logging
import shutil

from pathlib import Path

from backend.constants import DEFAULT_PRESET


def download_file(url: str, output_path: Path) -> None:
    """
    Downloads a file in chunks

    Args:
        url (str): The url to download
        output_path (Path): Where to download the file
            A full path with a name
            https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name

    Returns:
        None
    """
    r: requests.Response = requests.get(url)
    with open(output_path, 'wb') as file:
        logging.info(f"Downloading mastercomfig.zip to {output_path}")
        for chunk in r.iter_content(chunk_size=8192):
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


def delete_unneeded_prefixes(extracted_dir: Path, prefix_to_keep: str = DEFAULT_PRESET) -> None:
    """
    Looks in extracted_dir and deletes every preset that is not equal to prefix_to_keep

    Args:
        extracted_dir (Path): Path to where the files were extracted to
        prefix_to_keep (str): The prefix to keep
            MUST be in the form of mastercomfig-medium-low-preset
            or mastercomfig-high-preset

    Returns:

    """
    presets_dir: Path = extracted_dir / 'presets'
    if not presets_dir.exists():
        raise FileNotFoundError(f"Can't find {presets_dir} in {extracted_dir}")

    for preset in presets_dir.iterdir():
        if prefix_to_keep == preset.name:
            shutil.rmtree(preset.absolute())

    return


def download_choices(choices: list[tuple[str,str]], output_folder: Path) -> None:
    """
    Downloads all choices selected to a file

    Args:
        choices (list[str]): The urls and names to download. These can be found in the request json.
            index 0: url
            index 1: name
        output_folder (Path): Folder to download the images to.

    Returns:
        None
    """
    for choice in choices:
        download_file(choice[0], output_folder / choice[1])
