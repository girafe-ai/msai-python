from abc import ABC, abstractmethod


example = '''
In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations. Design patterns are formalized best practices that the programmer can use to solve common problems when designing an application or system.

Object-oriented design patterns typically show relationships and interactions between classes or objects, without specifying the final application classes or objects that are involved. Patterns that imply mutable state may be unsuited for functional programming languages. Some patterns can be rendered unnecessary in languages that have built-in support for solving the problem they are trying to solve, and object-oriented patterns are not necessarily suitable for non-object-oriented languages.

Design patterns may be viewed as a structured approach to computer programming intermediate between the levels of a programming paradigm and a concrete algorithm.
'''

with open('stopwords.txt') as stop_words_file:
    STOP_WORDS_ALIR3Z4 = stop_words_file.read().split('\n')

print(STOP_WORDS_ALIR3Z4[:100])


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

    def __init__(self, stop_words: list = None):
        self.stop_words = stop_words or self.default_stop_words

    def get_tags_from_text(self, text: str) -> list[str]:
        # TODO main logic
        pass

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        result = []
        for text in texts:
            tags = self.get_tags_from_text(text)
            result.append(tags)
        return result
