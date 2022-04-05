from abc import ABC, abstractmethod

example = '''
In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations. Design patterns are formalized best practices that the programmer can use to solve common problems when designing an application or system.

Object-oriented design patterns typically show relationships and interactions between classes or objects, without specifying the final application classes or objects that are involved. Patterns that imply mutable state may be unsuited for functional programming languages. Some patterns can be rendered unnecessary in languages that have built-in support for solving the problem they are trying to solve, and object-oriented patterns are not necessarily suitable for non-object-oriented languages.

Design patterns may be viewed as a structured approach to computer programming intermediate between the levels of a programming paradigm and a concrete algorithm.
'''


# def get_tags(text: str) -> list[str]:
#     pass


# def get_tags(texts: list[str]) -> list[list[str]]:  # ['Text1', 'Text2', ...] -> [['text1_tag1', text1_tag2], ...]
#     pass


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', text1_tag2], ...]"""
        ...


class BasePredefinedTagsTagger(BaseTagger, ABC):
    def __init__(self, tags: list[str]):
        self.tags = tags


class MainMultiTagger(BasePredefinedTagsTagger):
    tagger_classes = [Tagger1, Tagger2, ...]

    def __init__(self, tags: list[str]):
        super().__init__(tags=tags)

        self.taggers = []
        for tagger_class in self.tagger_classes:
            if isinstance(tagger_class, BasePredefinedTagsTagger):
                tagger = tagger_class(tags)
            else:
                tagger = tagger_class()
            self.taggers.append(tagger)

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        tags = [set() for _ in texts]
        for tagger in self.taggers:
            texts_tags = tagger.get_tags(texts)
            for text_tags, extracted_text_tags in zip(tags, texts_tags):
                text_tags |= extracted_text_tags

        tags = [list(s) for s in tags]

        return tags
