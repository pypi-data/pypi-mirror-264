"""Script to get language abbreviations from Danish Wiktionary."""
import json
import re
from pathlib import Path

import pyprojroot
import requests

url = "https://da.wiktionary.org/w/api.php"

params = {
    "action": "parse",
    "page": "Modul:lang/data",
    "format": "json",
    "prop": "wikitext",
    "contentmodel": "text",
}

response = requests.get(url, params=params)

if response.status_code != 200:
    msg = "API error"
    raise Exception(msg)

data = response.json()

html = data["parse"]

res = html["wikitext"]["*"]

pattern = re.compile(r'name\s*=\s*"([^"]+)"\s*,\s*code\s*=\s*"([^"]+)"')
matches = re.findall(pattern, res)

lang_abbr = {}

for match in matches:
    name = match[0]
    code = match[1]

    lang_abbr[code] = name.capitalize()

file_out = pyprojroot.here() / "wikiglot" / "data" / "da_lang_abbr.json"

file_out.parent.mkdir(parents=True, exist_ok=True)

with Path.open(file_out, "w") as f:
    json.dump(lang_abbr, f)
