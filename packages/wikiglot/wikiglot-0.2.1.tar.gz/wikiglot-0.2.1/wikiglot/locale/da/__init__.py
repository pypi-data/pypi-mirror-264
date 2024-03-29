import importlib.resources as resources
import json
import re

from bs4 import Tag

from ..locale import _Locale


class _Da(_Locale):
    def __init__(self):
        language = "da"
        path = resources.files("wikiglot.data") / "da_lang_abbr.json"

        with path.open() as f:
            language_map = json.loads(f.read())

        class_list = [
            "substantiv",
            "verb",
            "adjektiv",
            "adverbium",
            "pronomen",
            "præposition",
            "konjunktion",
            "interjektion",
            "artikel",
            "förkortning",
        ]

        inflection_stumps = [
            "bestemt ental af",
            "bestemt ettal af",
            "bestemt flertal af",
            "ental af",
            "ental bestemt form af",
            "ental ubestemt form af",
            "flertal af",
            "flertal bestemt form af",
            "flertal ubestemt form af",
            "flertal ubestemt form af",
            "genitiv ubestemet ental af",
            "genitiv ubestemet flertal af",
            "ubestemt ental af",
            "ubestemt ettal af",
            "ubestemt flertal af",
        ]
        inflection_pattern = r"^(?:" + "|".join(inflection_stumps) + r") (\w+)"

        synonym_patterns = None

        super().__init__(
            language, language_map, class_list, inflection_pattern, synonym_patterns
        )

    def extract_class_synonyms(self, class_tag: Tag):
        for tag in class_tag.next_siblings:
            if isinstance(tag, Tag):
                if tag.name == "h4":
                    span = tag.find_next("span")
                    if isinstance(span, Tag) and span.get_text() == "Synonymer":
                        for subtag in tag.next_siblings:
                            if isinstance(subtag, Tag):
                                if subtag.name in ["ul", "table"]:
                                    synonyms = subtag.find_all("li")
                                    if len(synonyms) > 0:
                                        synonyms_list = []
                                        for synonym in synonyms:
                                            synonyms_list.append(synonym.get_text())
                                        return synonyms_list
                                if subtag.name in ["h4", "h3", "h2", "h1"]:
                                    break
                elif tag.name == "h3":
                    break

        return []

    def extract_synonyms(self, dl: Tag) -> list[str]:  # noqa: ARG002
        # Danish wiktionary does not have entrywise synonyms
        return []

    def extract_antonyms(self, dl: Tag) -> list[str]:  # noqa: ARG002
        # Danish wiktionary does not have entrywise antonyms
        return []

    def extract_usage(self, dl: Tag) -> list[str]:
        dd = dl.find("dd", recursive=False)

        if isinstance(dd, Tag):
            i_tag = dd.find_all("i", recursive=False)
            return [i.get_text() for i in i_tag]

        return []

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
                        match = re.search(r"udtale?\d?", x, flags=re.IGNORECASE)
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
