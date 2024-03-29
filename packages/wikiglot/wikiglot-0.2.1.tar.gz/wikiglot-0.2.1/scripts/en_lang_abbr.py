"""Script to get language abbreviations from English Wiktionary."""
import csv
import json
from pathlib import Path

import pyprojroot
import requests
from bs4 import BeautifulSoup

url = "https://en.wiktionary.org/w/api.php"
params = {
    "action": "parse",
    "page": "Wiktionary:List_of_languages,_csv_format",
    "format": "json",
}

response = requests.get(url, params=params)

if response.status_code != 200:
    msg = "API error"
    raise Exception(msg)

data = response.json()
html = data["parse"]["text"]["*"]
soup = BeautifulSoup(html, "html.parser")
pre_tag = soup.find("pre")
text = pre_tag.get_text()

reader = csv.DictReader(text.split("\n"), delimiter=";")
lang_abbr = {}

for row in reader:
    lang_abbr[row["code"]] = row["canonical name"]

file_out = pyprojroot.here() / "wikiglot" / "data" / "en_lang_abbr.json"

file_out.parent.mkdir(parents=True, exist_ok=True)

with Path.open(file_out, "w") as f:
    json.dump(lang_abbr, f)
