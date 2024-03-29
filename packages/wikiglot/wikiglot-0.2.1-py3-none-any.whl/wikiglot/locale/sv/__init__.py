import importlib.resources as resources
import json
import re

from bs4 import Tag

from ..locale import _Locale


class _Sv(_Locale):
    def __init__(self):
        with resources.path("wikiglot.data", "sv_lang_abbr.json") as data_path:
            language_map = json.loads(data_path.read_text())

        class_list = [
            "adjektiv",
            "adverb",
            "affix",
            "artikel",
            "cirkumposition",
            "efterled",
            "fras",
            "förkortning",
            "förled",
            "infinitivmärke",
            "interjektion",
            "kod",
            "konjunktion",
            "ordspråk",
            "partikel",
            "postposition",
            "preposition",
            "pronomen",
            "räknemarkör",
            "räkneord",
            "substantiv",
            "talesätt",
            "tecken",
            "transkription",
            "verb",
            "verbpartikel",
        ]

        inflection_stumps = [
            "böjningsform av",
            "plural av",
            "avledning till adjektivet",
        ]

        inflection_pattern = r"^(?:" + "|".join(inflection_stumps) + r") (\w+)"

        synonym_patterns = None

        super().__init__(
            "sv",
            language_map,
            class_list,
            inflection_pattern,
            synonym_patterns,
        )

    def extract_class_synonyms(self, class_tag: Tag) -> list[str]:  # noqa: ARG002
        return []

    def extract_synonyms(self, dl: Tag) -> list[str]:
        synonyms: list[str] = []

        item = dl.find("dd", {"class": "template-synonymer"})

        if item is not None:
            pattern = r"Synonym(?:er)?\: ([^;]+)"
            synonyms_string = re.findall(pattern, item.get_text())[0]
            synonyms = synonyms_string.split(", ")

        return synonyms

    def extract_antonyms(self, dl) -> list[str]:
        antonyms: list[str] = []

        item = dl.find("dd", {"class": "template-antonymer"})

        if item is not None:
            pattern = r"Antonym(?:er)?\: ([^;]+)"
            antonyms_string = re.findall(pattern, item.get_text())[0]
            antonyms = antonyms_string.split(", ")

        return antonyms

    def extract_usage(self, dl: Tag) -> list[str]:
        dd = dl.find_all("dd", recursive=False)

        usage = []

        avoid_stumps = [
            "Synonymer:",
            "Hyponymer:",
            "Sammansättningar:",
            "Fraser:",
            "Användning:",
        ]
        avoid_pattern = re.compile(r"^(?:" + "|".join(avoid_stumps) + r") (.+)")

        for dd_i in dd:
            match = re.search(avoid_pattern, dd_i.get_text())
            if match:
                continue

            dl_tag = dd_i.find("dl", recursive=False)

            if dl_tag:
                usage_item = dl_tag.find("dd").find("i")
            else:
                usage_item = dd_i.find("i", recursive=False)

            if usage_item:
                usage.append(usage_item.get_text())

        return usage

    def extract_pronunciation(self, language_tag_parent: Tag) -> list[str]:
        pronunciation = set()
        ul_tag = language_tag_parent.find_next("ul")
        if isinstance(ul_tag, Tag):
            ipa_tag = ul_tag.find_all("span", {"class": "ipa"})
            for ipa in ipa_tag:
                pronunciation.add(f"/{ipa.get_text()}/")
            oo = ul_tag.find_all("span", {"class": "oo-ui-labelElement-label"})
            for o in oo:
                pronunciation.add(f"/{o.get_text()}/")

        return list(pronunciation)
