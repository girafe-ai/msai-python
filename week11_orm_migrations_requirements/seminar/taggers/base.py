from abc import ABC, abstractmethod


# https://github.com/igorbrigadir/stopwords/blob/master/en/alir3z4.txt
with open('taggers/stopwords.txt') as stop_words_file:
    STOP_WORDS_ALIR3Z4 = stop_words_file.read().split('\n')

# https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt
with open('taggers/popular-words.txt') as popular_words_file:
    POPULAR_WORDS = popular_words_file.read().split('\n')

POPULAR_TAGS = list(set(POPULAR_WORDS) - set(STOP_WORDS_ALIR3Z4))


def extract_words(text: str, alphabet: str, min_length: int = 3, stop_words: list[str] = None):
    """Split text into word."""
    stop_words = stop_words or []

    # filter symbols
    text = ''.join(
        (c if c in alphabet else ' ')
        for c in text.lower()
    )

    # split to words
    words = text.split()

    # filter words
    return [
        word
        for word in words
        if word not in stop_words and len(word) >= min_length
    ]


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        ...


class BaseChoiceTagger(BaseTagger, ABC):
    def __init__(self, tags: list[str]):
        self.tags = tags


class BaseSeparateTagger(BaseTagger, ABC):
    @abstractmethod
    def get_tags_from_text(self, text: str) -> list[str]:
        """'Text' -> ['text_tag1', 'text_tag2', ...]"""
        ...

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        result = []
        for text in texts:
            tags = self.get_tags_from_text(text)
            result.append(tags)
        return result
