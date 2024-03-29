"""Tests for wikiglot."""

import importlib.resources as resources

from bs4 import BeautifulSoup

from wikiglot import Wiktionary


def test_full_parse():
    """Basic regression test for English wiktionary."""
    path = resources.files("tests.data.en") / "dog.html"
    with path.open() as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    wiki = Wiktionary("en")
    out = wiki._parse_soup(soup, "dog", "en")

    ref = {
        "word": "dog",
        "language": "en",
        "pronunciation": ["/dɑɡ/", "/dɒɡ/", "/dɔɡ/"],
        "parts": [
            {
                "class": "noun",
                "entries": [
                    {
                        "definition": "The species Canis familiaris (sometimes designated Canis lupus familiaris), domesticated for thousands of years and of highly variable appearance because of human breeding.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["The dog barked all night long."],
                    },
                    {
                        "definition": "Any member of the family Canidae, including domestic dogs, wolves, coyotes, jackals, foxes, and their relatives (extant and extinct); canid.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(often attributive) A male dog, wolf, or fox, as opposed to a bitch or vixen.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(uncountable) The meat of this animal, eaten as food.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["Did you know that they eat dog in South Korea?"],
                    },
                    {
                        "definition": "(slang, derogatory) A dull, unattractive girl or woman.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["She’s a real dog."],
                    },
                    {
                        "definition": "(slang) A man, guy, chap.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["You lucky dog!"],
                    },
                    {
                        "definition": "(derogatory) Someone who is cowardly, worthless, or morally reprehensible.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["Come back and fight, you dogs!", "You dirty dog."],
                    },
                    {
                        "definition": "(slang) A sexually aggressive man.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "Any of various mechanical devices for holding, gripping, or fastening something, particularly with a tooth-like projection.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": " A click or pallet adapted to engage the teeth of a ratchet wheel, to restrain the back action.",
                        "synonyms": ["click", "pallet", "pawl", "ratchet"],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "A metal support for logs in a fireplace.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["The dogs were too hot to touch."],
                    },
                    {
                        "definition": "(transport, historical) A double-ended side spike driven through a hole in the flange of a rail on a tramway.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(cartomancy) The eighteenth Lenormand card.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "A hot dog: a frankfurter, wiener, or similar sausage; or a sandwich made from this.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(poker slang) An underdog.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(slang, chiefly in the plural) Foot.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["My dogs are barking!"],
                    },
                    {
                        "definition": '(Cockney rhyming slang) (from "dog and bone") Phone or mobile phone.',
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["My dog is dead."],
                    },
                    {
                        "definition": "One of the cones used to divide up a racetrack when training horses.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(film) A flop; a film that performs poorly at the box office.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(firearms, archaic) A cock, as of a gun.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(preceded by definite article) A dance having a brief vogue in the 1960s in which the actions of a dog were mimicked.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                ],
                "synonyms": [],
            },
            {
                "class": "verb",
                "entries": [
                    {
                        "definition": "(transitive) To pursue with the intent to catch.",
                        "synonyms": [
                            "chase",
                            "chase after",
                            "go after",
                            "pursue",
                            "tag",
                            "tail",
                            "track",
                            "trail",
                        ],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(transitive) To follow in an annoying or harassing way.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [
                            "The woman cursed him so that trouble would dog his every step."
                        ],
                    },
                    {
                        "definition": "(transitive, nautical) To fasten a hatch securely.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": ["It is very important to dog down these hatches."],
                    },
                    {
                        "definition": "(intransitive, emerging usage in Britain) To watch, or participate, in sexual activity in a public place.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [
                            "I admit that I like to dog at my local country park."
                        ],
                    },
                    {
                        "definition": "(intransitive, transitive) To intentionally restrict one's productivity as employee; to work at the slowest rate that goes unpunished.",
                        "synonyms": ["soldier", "goldbrick"],
                        "antonyms": [],
                        "usage": [
                            "A surprise inspection of the night shift found that some workers were dogging it."
                        ],
                    },
                    {
                        "definition": "(transitive, slang) To criticize.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                    {
                        "definition": "(transitive, military) To divide (a watch) with a comrade.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    },
                ],
                "synonyms": [],
            },
            {
                "class": "adjective",
                "entries": [
                    {
                        "definition": "(slang) Of inferior quality; dogshit.",
                        "synonyms": [],
                        "antonyms": [],
                        "usage": [],
                    }
                ],
                "synonyms": [],
            },
        ],
    }

    assert ref == out
