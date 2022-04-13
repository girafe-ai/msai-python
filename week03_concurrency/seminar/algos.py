from abc import ABC, abstractmethod
from collections import Counter

example = '''
In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations. Design patterns are formalized best practices that the programmer can use to solve common problems when designing an application or system.

Object-oriented design patterns typically show relationships and interactions between classes or objects, without specifying the final application classes or objects that are involved. Patterns that imply mutable state may be unsuited for functional programming languages. Some patterns can be rendered unnecessary in languages that have built-in support for solving the problem they are trying to solve, and object-oriented patterns are not necessarily suitable for non-object-oriented languages.

Design patterns may be viewed as a structured approach to computer programming intermediate between the levels of a programming paradigm and a concrete algorithm.
'''

with open('stopwords.txt') as stop_words_file:
    STOP_WORDS_ALIR3Z4 = stop_words_file.read().split('\n')


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', text1_tag2], ...]"""
        ...


class BasePredefinedTagsTagger(BaseTagger, ABC):
    def __init__(self, tags: list[str]):
        self.tags = tags


class MostFrequentWordsTagger(BaseTagger):
    default_stop_words = STOP_WORDS_ALIR3Z4
    words_alphabet = 'abcdefghijklmnopqrstuvwxyz-\''

    def __init__(self, stop_words: list = None, max_tags_per_text: int = 5):
        self.stop_words = stop_words or self.default_stop_words
        self.max_tags_per_text = max_tags_per_text

    def get_tags_from_text(self, text: str) -> list[str]:
        text = ''.join(
            (c if c in self.words_alphabet else ' ')
            for c in text.lower()
        )
        words = text.split()
        words = [
            word
            for word in words
            if word not in self.stop_words and len(word) > 2
        ]

        words_counter = Counter(words)

        # TODO improve
        tags = []
        result = words_counter.most_common()
        if len(result) == 0:
            return []

        word, max_count = result[0]
        i = 0
        while result[i][1] == max_count:
            tags.append(result[i][0])
            i += 1

        return tags[:self.max_tags_per_text]

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        result = []
        for text in texts:
            tags = self.get_tags_from_text(text)
            result.append(tags)
        return result


class FindSpecialWordsTagger(BasePredefinedTagsTagger):
    default_tags_candidates = STOP_WORDS_ALIR3Z4

    def __init__(self, tags: list[str] = None, max_tags_per_text: int = 5):
        super().__init__(tags=tags or self.default_tags_candidates)
        self.max_tags_per_text = max_tags_per_text

    def get_tags_from_text(self, text: str) -> list[str]:
        tags = []  # TODO
        return tags[:self.max_tags_per_text]

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        result = []
        for text in texts:
            tags = self.get_tags_from_text(text)
            result.append(tags)
        return result


print(MostFrequentWordsTagger().get_tags([example]))
