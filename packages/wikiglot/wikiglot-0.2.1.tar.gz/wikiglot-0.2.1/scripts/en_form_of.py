# https://en.wiktionary.org/wiki/Category:Form-of_templates
import csv
import json
from pathlib import Path

import pyprojroot
import requests
from bs4 import BeautifulSoup

url = "https://en.wiktionary.org/w/api.php"
params = {
    "action": "parse",
    "page": "Category:Form-of_templates",
    "format": "json",
}

response = requests.get(url, params=params)

if response.status_code != 200:
    msg = "API error"
    raise Exception(msg)

data = response.json()
html = data["parse"]["text"]["*"]
soup = BeautifulSoup(html, "html.parser")

table_tag = soup.find_all("table")[1]

tr_tags = table_tag.find_all("tr")

forms_of = []

for row in tr_tags:
    tds = row.find_all("td")
    if len(tds) > 0:
        forms_of.append(tds[0].get_text())

file_out = pyprojroot.here() / "wikiglot" / "data" / "en_form_of.txt"

file_out.parent.mkdir(parents=True, exist_ok=True)

with Path.open(file_out, "w") as f:
    for form_of in forms_of:
        f.write(form_of + "\n")
