import requests
import json

from typing import Any

from backend.constants import MC_RELEASES_URL_BASE, RELEASES_PER_PAGE
from backend.items import ReleaseItem


def format_api_link(page_number: int = 1, amt_per_page: int = RELEASES_PER_PAGE) -> str:
    """
    Formats a github api call link.

    Args:
        page_number (int): What page number to get
        amt_per_page (int): How many per page to return

    Returns:
        str: A formatted api git call
    """
    return f'{MC_RELEASES_URL_BASE}?per_page={amt_per_page}&page={page_number}'


def get_amt_pages(session: requests.Session) -> int:
    """
    Gets the amount of pages by parsing the headers of a given request.

    Returns:
        int: Amount of total pages
    """
    r = session.get(format_api_link())
    r.raise_for_status()

    # r.headers is a dictionary
    # string parsing for final page number
    return int(r.headers['link'].split()[2][-3])


def make_release(page_json: Any, index: int = 1) -> ReleaseItem:
    return ReleaseItem(page_json[index]["name"], page_json[index]["id"], page_json[index]["assets"])

'''def find_zip(assets: list[Any], choices: list[str]) -> str:
    """
    Looks through the chi
    
    Args:
        assets: 
        choices: 

    Returns:

    """
    for asset in assets:
        if asset['name'] == NAME_MATCH:
            return asset['browser_download_url']

    raise IndexError(f"No {NAME_MATCH} found in the assets")'''
