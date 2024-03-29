"""Tests for wikiglot."""
import importlib.resources as resources

from bs4 import BeautifulSoup

from wikiglot import Wiktionary


def test_full_parse():
    """Basic regression test for Swedish wiktionary."""
    path = resources.files("tests.data.da") / "hund.html"
    with path.open() as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    wiki = Wiktionary("da")
    out = wiki._parse_soup(soup, "hund", "da")

    ref = {
        "word": "hund",
        "language": "da",
        "pronunciation": ["[ˈhunˀ]"],
        "parts": [
            {
                "class": "substantiv",
                "entries": [
                    {
                        "definition": "(zoologi): et pattedyr af underarten Canis lupus familiaris.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["Jeg er ikke bange for hunde."],
                    },
                    {
                        "definition": "(slang): 100 DKK-seddel (bruges ikke i flertal)",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["Vil du låne mig en hund?"],
                    },
                ],
                "synonyms": [
                    "(hunhund): en tæve",
                    "(unge): en hvalp",
                    "(nedsættende): en køter",
                    "(slang om lille hund): en tæppetisser",
                    "(babysprog): en vovse",
                    "(babysprog): en vovhund",
                ],
            }
        ],
    }

    assert ref == out
