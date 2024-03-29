"""Tests for wikiglot."""
import importlib.resources as resources

from bs4 import BeautifulSoup

from wikiglot import Wiktionary


def test_full_parse():
    """Basic regression test for Swedish wiktionary."""
    path = resources.files("tests.data.sv") / "hund.html"
    with path.open() as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    wiki = Wiktionary("sv")
    out = wiki._parse_soup(soup, "hund", "sv")

    ref = {
        "word": "hund",
        "language": "sv",
        "pronunciation": ["/hɵnd/"],
        "parts": [
            {
                "class": "substantiv",
                "entries": [
                    {
                        "definition": "en underart (Canis lupus familiaris) till arten varg (Canis lupus) inom däggdjursfamiljen hunddjur (Canidae); individ av underarten hund",
                        "synonyms": [
                            "Canis familiaris (äldre klassificering)",
                            "Canis familiaris domesticus (äldre klassificering)",
                        ],
                        "antonyms": [],
                        "usage": ["Går du ut med hunden?"],
                    },
                    {
                        "definition": "(nedsättande, överfört)  skymford för föraktliga personer",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                ],
                "synonyms": [],
            }
        ],
    }

    assert ref == out
