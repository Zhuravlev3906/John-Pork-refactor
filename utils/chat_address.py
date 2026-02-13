import re
from typing import Iterable
from rapidfuzz import fuzz, process


class BotAddressDetector:
    _RE_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
    _RE_ELONGATION = re.compile(r"(.)\1{2,}", re.UNICODE)

    def __init__(
        self,
        keywords: Iterable[str],
        threshold: int = 85,
        fuzzy_window: int = 8,
    ) -> None:
        normalized = {self._normalize(k) for k in keywords if k}

        self.single_keywords = {k for k in normalized if " " not in k}
        self.phrase_keywords = {k for k in normalized if " " in k}

        self.threshold = threshold
        self.fuzzy_window = fuzzy_window

        self._phrase_patterns = [
            re.compile(rf"\b{re.escape(phrase)}\b")
            for phrase in self.phrase_keywords
        ]

    @classmethod
    def _normalize(cls, text: str) -> str:
        text = text.lower().strip()
        text = cls._RE_PUNCT.sub("", text)
        text = cls._RE_ELONGATION.sub(r"\1", text)
        return text

    def is_addressing(self, message_text: str) -> bool:
        if not message_text:
            return False

        normalized_text = self._normalize(message_text)
        if not normalized_text:
            return False

        words = normalized_text.split()
        if not words:
            return False

        head = words[: self.fuzzy_window]

        for word in head:
            if word in self.single_keywords:
                return True

        for pattern in self._phrase_patterns:
            if pattern.search(normalized_text):
                return True

        for word in head:
            if len(word) < 3:
                continue

            cutoff = self.threshold if len(word) > 5 else 90

            if process.extractOne(
                word,
                self.single_keywords,
                scorer=fuzz.WRatio,
                score_cutoff=cutoff,
            ):
                return True

        short_head_text = " ".join(head)

        for phrase in self.phrase_keywords:
            if fuzz.token_set_ratio(phrase, short_head_text) >= 88:
                return True

        return False
