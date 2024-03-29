import re

import requests
from bs4 import BeautifulSoup, Tag

from .locale import _Da, _En, _Sv
from .utils import _get_soup


class Wiktionary:
    """
    A class for interacting with Wiktionary to retrieve linguistic information.

    Parameters
    ----------
    locale:
        The locale to be used for language-specific operations.
    """

    def __init__(self, locale: str = "en"):
        """
        Initialize the Wiktionary class with the specified locale.

        Parameters
        ----------
        locale:
            The locale to be used for language-specific operations.
        """
        self.locale = self._localize(locale)

    @staticmethod
    def _localize(locale: str):
        if locale not in ["en", "sv", "da"]:
            msg = f"Unsupported locale: {locale}"
            raise ValueError(msg)

        if locale == "sv":
            return _Sv()

        if locale == "da":
            return _Da()

        return _En()

    def _extract_definition(self, x: str) -> str:
        # Remove [1], [from 19th cent], etc
        pat = re.compile(r"\[.*\]")
        return re.sub(pat, "", x[0])

    def _extract_root(self, definition: str) -> str | None:
        matches = re.findall(self.locale.inflection_pattern, definition)
        return matches[0] if matches else None

    def _parse_lemmas(self, ol_tag: Tag, word: str) -> set[str]:
        lemmas = set()

        entry_items = ol_tag.find_all("li", recursive=False)

        for item in entry_items:
            sub_ol_tag = item.find("ol", recursive=False)
            if sub_ol_tag:
                # If there is a nested entry, we collapse it into the current entry
                lemmas.update(self._parse_lemmas(sub_ol_tag, word))
                continue

            txt = item.get_text()

            txt_split = txt.split("\n")

            definition = self._extract_definition(txt_split)
            lemma = self._extract_root(definition)

            if lemma:
                lemmas.add(lemma)
            else:
                lemmas.add(word)

        return lemmas

    def _parse_description(self, ol_tag: Tag):
        descriptions = []

        entry_items = ol_tag.find_all("li", recursive=False)

        for item in entry_items:
            item_class = item.attrs.get("class")
            if item_class and "mw-empty-elt" in item_class:
                continue

            sub_ol_tag = item.find("ol", recursive=False)
            if sub_ol_tag:
                # If there is a nested entry, we collapse it into the current entry
                descriptions += self._parse_description(sub_ol_tag)
                continue

            txt = item.get_text()

            txt_split = txt.split("\n")

            definition = self._extract_definition(txt_split)

            dl = item.find("dl", recursive=False)

            synonyms = []
            antonyms = []
            usage = []

            if dl:
                synonyms = self.locale.extract_synonyms(dl)
                antonyms = self.locale.extract_antonyms(dl)
                usage = self.locale.extract_usage(dl)

            description = {
                "definition": definition,
                "synonyms": synonyms,
                "antonyms": antonyms,
                "usage": usage,
            }

            descriptions.append(description)

        return descriptions

    def _parse_soup_for_lemmas(
        self, soup: BeautifulSoup, word: str, language_id: str
    ) -> set[str]:
        lemmas = set()

        language_tag = soup.find(id=language_id)

        if language_tag is None:
            return lemmas

        language_tag_parent = language_tag.find_parent()

        if language_tag_parent is None:
            return lemmas

        language_tag_parent_siblings = language_tag_parent.next_siblings

        for entry in language_tag_parent_siblings:
            if isinstance(entry, Tag):
                if entry.name == "h2":
                    break

                if entry.name in ["h3", "h4"]:
                    span_tag = entry.find_next("span")
                    if (
                        isinstance(span_tag, Tag)
                        and span_tag.get_text().lower() in self.locale.class_list
                    ):
                        ol_tag = entry.find_next("ol")

                        if isinstance(ol_tag, Tag):
                            lemmas.update(self._parse_lemmas(ol_tag, word))

        return lemmas

    def _parse_soup(
        self, soup: BeautifulSoup, word: str, language_from: str
    ) -> dict | None:
        language_id = self.locale.language_map[language_from]
        language_tag = soup.find(id=language_id)

        if language_tag is None:
            return None

        language_tag_parent = language_tag.find_parent()

        if language_tag_parent is None:
            return None

        pronunciation = self.locale.extract_pronunciation(language_tag_parent)
        pronunciation.sort()

        glossary_entry = {
            "word": word,
            "language": language_from,
            "pronunciation": pronunciation,
            "parts": [],
        }

        parts = []

        language_tag_parent_siblings = language_tag_parent.find_next_siblings()

        if language_tag_parent_siblings is None:
            return None

        for tag in language_tag_parent_siblings:
            if isinstance(tag, Tag):
                if tag.name == "h2":
                    break

                if tag.name in ["h3", "h4"]:
                    span_tag = tag.find_next("span")
                    if (
                        isinstance(span_tag, Tag)
                        and span_tag.get_text().lower() in self.locale.class_list
                    ):
                        lexical_class = span_tag.get_text().lower()

                        class_synonyms = self.locale.extract_class_synonyms(tag)

                        ol_tag = tag.find_next("ol")

                        if isinstance(ol_tag, Tag):
                            entries = self._parse_description(ol_tag)

                            if len(entries) > 0:
                                part = {
                                    "class": lexical_class,
                                    "entries": entries,
                                    "synonyms": class_synonyms,
                                }

                                parts.append(part)

        glossary_entry["parts"] = parts

        return glossary_entry

    def lemmatize(
        self,
        word: str,
        language_from: str | None = None,
        session: requests.Session | None = None,
    ) -> set[str]:
        """
        Lemmatize a given word in a specified language or in the default language
        if none is specified.

        Parameters
        ----------
        word
            The word to be lemmatized.

        language_from
            The language in which the word is to be lemmatized.
            If not provided, the language of the Wiktionary will be used.

        session
            A `requests.Session` object to be used for the request. If not provided,
            a new session will be created.

        Returns
        -------
        set[str]
            A set of lemmas for the given word.

        Raises
        ------
        ValueError
            If the specified language is not in the language map.

        """
        if language_from is None:
            language_from = self.locale.language

        if language_from not in self.locale.language_map:
            msg = "Language not in language map"
            raise ValueError(msg)

        language_id = self.locale.language_map[language_from]

        soup = _get_soup(
            word, f"https://{self.locale.language}.wiktionary.org/w/api.php", session
        )

        if soup is None:
            return set()

        return self._parse_soup_for_lemmas(soup, word, language_id)

    def lookup(
        self,
        word: str,
        language_from: str | None = None,
        session: requests.Session | None = None,
    ) -> dict | None:
        """
        Look up a word.

        Parameters
        ----------
        word
            The word to look up.

        language_from
            The language in which to look up the word. If not specified,
            the language of the Wiktionary is used.

        session
            A `requests.Session` object to be used for the request. If not provided,
            a new session will be created each time the function is used.

        Returns
        -------
        dict or None
            A dictionary containing the word's information if the word is found,
            `None` otherwise.

        Raises
        ------
        ValueError
            If the specified language is not in the language map.

        """
        if language_from is None:
            language_from = self.locale.language

        if language_from not in self.locale.language_map:
            msg = "Language not in language map"
            raise ValueError(msg)

        soup = _get_soup(
            word, f"https://{self.locale.language}.wiktionary.org/w/api.php", session
        )

        if soup is None:
            return None

        return self._parse_soup(soup, word, language_from)
