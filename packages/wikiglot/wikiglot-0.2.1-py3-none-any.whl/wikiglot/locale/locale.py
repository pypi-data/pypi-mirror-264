import re
from abc import ABC, abstractmethod

from bs4 import Tag


class _Locale(ABC):
    def __init__(
        self,
        language: str,
        language_map: dict[str, str],
        class_list: list[str],
        inflection_pattern: str,
        synonym_pattern: str | None,
    ):
        self.language = language
        self.language_map = language_map
        self.class_list = class_list
        self.inflection_pattern = re.compile(inflection_pattern, flags=re.IGNORECASE)
        self.synonym_pattern = synonym_pattern

    @abstractmethod
    def extract_pronunciation(self, language_tag_parent: Tag) -> list[str]:
        pass

    @abstractmethod
    def extract_synonyms(self, dl: Tag) -> list[str]:
        pass

    @abstractmethod
    def extract_class_synonyms(self, class_tag: Tag) -> list[str]:
        pass

    @abstractmethod
    def extract_antonyms(self, dl: Tag) -> list[str]:
        pass

    @abstractmethod
    def extract_usage(self, dl: Tag) -> list[str]:
        pass
