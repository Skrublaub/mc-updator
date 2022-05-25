import requests
import json

from typing import Any

from backend.constants import MC_RELEASES_URL_BASE, RELEASES_PER_PAGE, NAME_MATCH


def format_api_link(page_number: int = 1, amt_per_page: int = RELEASES_PER_PAGE) -> str:
    """
    Formats a github api call link.

    Args:
        page_number: What page number to get
        amt_per_page: How many per page to return

    Returns:
        str: A formatted api git call
    """
    return f'{MC_RELEASES_URL_BASE}?per_page={amt_per_page}&page={page_number}'


def get_versions(amt_pages: int) -> list[tuple[str, str, list[Any]]]:
    """
    Gets the versions and id available to download.
    The args will be used later

    Args:
        amt_pages (int): The amount of pages to look through
        page_number (int): What page to start counting on

    Returns:
        list[tuple[str, str, list[Any]]]: Info about releases
            Index 0: Release version name
            Index 1: Release id
            Index 2: Assets
    """
    versions_list: list[tuple[str, str, list[Any]]] = []

    # add support for more than dev and latest release later
    # for page_number in range(amt_pages):
    page_number: int = 0
    r = requests.get(format_api_link(page_number=(page_number + 1)))
    r.raise_for_status()

    r_json = json.loads(r.text)

    for release in r_json:
        versions_list.append((release['name'], release['id'], release['assets']))

    return versions_list


def get_amt_pages() -> int:
    """
    Gets the amount of pages by parsing the headers of a given request.

    Returns:
        int: Amount of total pages
    """
    r = requests.get(format_api_link())
    r.raise_for_status()

    # r.headers is a dictionary
    # string parsing for final page number
    return int(r.headers['link'].split()[2][-3])


def find_zip(assets: list[Any]) -> str:
    for asset in assets:
        if asset['name'] == NAME_MATCH:
            return asset['browser_download_url']

    raise IndexError(f"No {NAME_MATCH} found in the assets")