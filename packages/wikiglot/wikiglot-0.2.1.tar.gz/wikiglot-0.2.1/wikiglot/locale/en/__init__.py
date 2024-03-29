import importlib.resources as resources
import json
import re

from bs4 import Tag

from ..locale import _Locale


class _En(_Locale):
    def __init__(self):
        language = "en"

        with resources.path("wikiglot.data", "en_lang_abbr.json") as data_path:
            language_map = json.loads(data_path.read_text())

        class_list = [
            "adjective",
            "adverb",
            "ambiposition",
            "article",
            "circumfix",
            "circumposition",
            "classifier",
            "combining form",
            "conjunction",
            "contraction",
            "counter",
            "determiner",
            "diacritical mark",
            "ideophone",
            "infix",
            "interfix",
            "interjection",
            "letter",
            "ligature",
            "noun",
            "number",
            "numeral",
            "participle",
            "particle",
            "phrase",
            "postposition",
            "prefix",
            "preposition",
            "prepositional phrase",
            "pronoun",
            "proper noun",
            "proverb",
            "punctuation mark",
            "root",
            "suffix",
            "syllable",
            "symbol",
            "verb",
        ]

        inflection_stumps = [
            "abstract noun of",
            "active participle of",
            "alternative plural of",
            "definite singular of",
            r"definite\/plural of",
            "feminine plural of",
            "feminine plural past participle of",
            "feminine singular of",
            "feminine singular past participle of",
            "gerund of",
            "imperative of",
            "indefinite genitive plural of",
            "indefinite genitive singular of",
            "indefinite plural of",
            "inflection of",
            "masculine plural of",
            "masculine plural past participle of",
            "neuter singular of",
            "passive of",
            "past of",
            "past participle definite singular of",
            "past participle form of",
            "past participle of",
            "past participle plural of",
            "past tense of",
            "perfective form of",
            "plural and definite singular attributive of",
            "plural of",
            "present of",
            "present participle and gerund of",
            "present participle of",
            "simple past and past participle of",
            "simple past of",
            "simple past participle of",
            "simple past tense of",
            r"simple past\/past participle of",
            "singular of",
        ]

        inflection_patterns = r"^(?:" + "|".join(inflection_stumps) + r") (\w+)"

        synonym_stumps = [
            "alternative spelling of",
            "nonstandard form of",
            "nonstandard spelling of",
            "spelling of",
            "synonym of",
        ]

        synonym_patterns = r"^(?:" + "|".join(synonym_stumps) + r") (\w+)"

        super().__init__(
            language,
            language_map,
            class_list,
            inflection_patterns,
            synonym_patterns,
        )

    def extract_class_synonyms(self, class_tag: Tag) -> list:  # noqa: ARG002
        return []

    def extract_synonyms(self, dl: Tag) -> list[str]:
        synonyms = []
        item = dl.find("span", {"class": "synonym"})

        if item is not None:
            pattern = re.compile(r"Synonym(?:s)?\: ([^;]+)")
            synonyms_string = re.findall(pattern, item.get_text())[0]
            synonyms = synonyms_string.split(", ")

            # see Thesaurus: word -> word
            thesaurus_pattern = re.compile(r"see Thesaurus:(.*)")

            for i in range(len(synonyms)):
                match = re.search(thesaurus_pattern, synonyms[i])
                if match:
                    synonyms[i] = match.group(1).strip()

        return synonyms

    def extract_antonyms(self, dl) -> list[str]:
        antonyms = []
        item = dl.find("span", {"class": "antonym"})

        if item is not None:
            pattern = re.compile(r"Antonym(?:s)?\: ([^;]+)")
            antonyms_string = re.findall(pattern, item.get_text())[0]
            antonyms = antonyms_string.split(", ")

            # see Thesaurus: word -> word
            thesaurus_pattern = re.compile(r"see Thesaurus:(.*)")

            for i in range(len(antonyms)):
                match = re.search(thesaurus_pattern, antonyms[i])
                if match:
                    antonyms[i] = match.group(1).strip()

        return antonyms

    def extract_usage(self, dl: Tag) -> list[str]:
        items = dl.find_all("i", {"class": "e-example"})
        return [item.get_text() for item in items]

    def extract_pronunciation(self, language_tag_parent: Tag) -> list[str]:
        pronunciation = set()
        language_tag_parent_siblings = language_tag_parent.next_siblings

        for entry in language_tag_parent_siblings:
            if isinstance(entry, Tag):
                if entry.name == "h2":
                    break

                if entry.name in ["h3", "h4"]:
                    span_tag = entry.find_next("span")
                    if span_tag:
                        x = span_tag.get_text()
                        match = re.search(r"pronunciation_?\d?", x, flags=re.IGNORECASE)
                        if match:
                            p_ul_tag = span_tag.find_next("ul")
                            if isinstance(p_ul_tag, Tag):
                                lis = p_ul_tag.find_all("li")
                                for li in lis:
                                    match = re.search("IPA", li.get_text())
                                    if match:
                                        ipa = li.find("span", {"class": "IPA"})
                                        if ipa:
                                            pronunciation.add(ipa.get_text())

        return list(pronunciation)
