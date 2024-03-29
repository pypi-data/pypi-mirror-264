import requests
from bs4 import BeautifulSoup


def _get_soup(
    word: str, url: str, session: requests.Session | None = None
) -> BeautifulSoup | None:
    from . import __version__

    if session is None:
        session = requests.Session()

    params = {
        "action": "parse",
        "page": word.replace(" ", "_"),
        "format": "json",
        "prop": "text",
    }

    headers = {
        "User-Agent": f"Wikiglot/{__version__} (https://github.com/jolars/wikiglot/)"
    }

    response = session.get(url, params=params, headers=headers)

    if response.status_code != 200:
        msg = f"API error for word: {word}"
        raise Exception(msg)

    data = response.json()

    if "error" in data:
        return None

    html = data["parse"]["text"]["*"]

    return BeautifulSoup(html, "html.parser")
