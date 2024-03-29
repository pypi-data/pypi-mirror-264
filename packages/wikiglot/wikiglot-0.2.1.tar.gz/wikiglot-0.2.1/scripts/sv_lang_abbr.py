import json
from pathlib import Path

import pyprojroot
import requests
from bs4 import BeautifulSoup

url = "https://sv.wiktionary.org/w/api.php"

params = {
    "action": "parse",
    "page": "Wiktionary:Stilguide/Språknamn",
    "format": "json",
}

response = requests.get(url, params=params)

if response.status_code != 200:
    msg = "API error"
    raise Exception(msg)

data = response.json()

html = data["parse"]["text"]["*"]

soup = BeautifulSoup(html, "html.parser")

table_tag = soup.find("table")

res = [
    (item["data-lang-code"], item["data-lang-name"])
    for item in table_tag.find_all(
        "span", attrs={"data-lang-name": True, "data-lang-code": True}
    )
]

lang_abbr = {}

for r in res:
    lang_abbr[r[0]] = r[1].capitalize()

file_out = pyprojroot.here() / "wikiglot" / "data" / "sv_lang_abbr.json"

file_out.parent.mkdir(parents=True, exist_ok=True)

with Path.open(file_out, "w") as f:
    json.dump(lang_abbr, f)
