import requests
import json

def get_versions(response: requests.Response) -> list[str]:
    """
    Gets a list of the release numbers as strings.

    Returns:
        list[str]: list of strings that hold the available mastercomfig versions
    """
    version_list: list[str] = []

    for releases in get_release_pages(response):
        releases_json = json.loads(releases.text)

        for release in releases_json:
            version_list.append(release['name'])

    return version_list


def get_release_pages(response: requests.Response) -> requests.Response:
    """
    Makes a request to the github api for the entirety of the requests page.
    There will be more string manipulation.

    Args:
        response (requests.Response): Response to get the release pages from because
            the github api doesn't return every release.

    Yields:
        requests.Response: The individual api call for a requests function
    """
    # has no page number to select from, https://api.github.com/repositories/69422496/releases?page=
    page_url_canvas: str = response.headers['Link'].split()[2][1:-3]
    last_page_index: int = int(response.headers['Link'].split()[2][-3])

    for page_num in range(1, last_page_index + 1):
        indiv: requests.Response = requests.get(f'{page_url_canvas}{page_num}')
        indiv.raise_for_status()
        yield indiv
