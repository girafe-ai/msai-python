from abc import ABC, abstractmethod
from collections import Counter

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

example = '''
In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations. Design patterns are formalized best practices that the programmer can use to solve common problems when designing an application or system.

Object-oriented design patterns typically show relationships and interactions between classes or objects, without specifying the final application classes or objects that are involved. Patterns that imply mutable state may be unsuited for functional programming languages. Some patterns can be rendered unnecessary in languages that have built-in support for solving the problem they are trying to solve, and object-oriented patterns are not necessarily suitable for non-object-oriented languages.

Design patterns may be viewed as a structured approach to computer programming intermediate between the levels of a programming paradigm and a concrete algorithm.
'''

# https://github.com/igorbrigadir/stopwords/blob/master/en/alir3z4.txt
with open('stopwords.txt') as stop_words_file:
    STOP_WORDS_ALIR3Z4 = stop_words_file.read().split('\n')

# https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt
with open('popular-words.txt') as popular_words_file:
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


class MostFrequentWordsTagger(BaseSeparateTagger):
    default_stop_words = STOP_WORDS_ALIR3Z4
    words_alphabet = 'abcdefghijklmnopqrstuvwxyz-\''

    def __init__(self, stop_words: list = None, max_tags_per_text: int = 5):
        self.stop_words = stop_words or self.default_stop_words
        self.max_tags_per_text = max_tags_per_text

    def get_tags_from_text(self, text: str) -> list[str]:
        words = extract_words(text, alphabet=self.words_alphabet, min_length=3, stop_words=self.stop_words)
        words_counter = Counter(words)

        # TODO improve heuristics
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


class FindSpecialWordsTagger(BaseSeparateTagger, BaseChoiceTagger):
    default_tags_candidates = POPULAR_TAGS
    words_alphabet = 'abcdefghijklmnopqrstuvwxyz-\''

    def __init__(self, tags: list[str] = None, max_tags_per_text: int = 5):
        super().__init__(tags=tags or self.default_tags_candidates)
        self.max_tags_per_text = max_tags_per_text

    def get_tags_from_text(self, text: str) -> list[str]:
        words = extract_words(text, alphabet=self.words_alphabet, min_length=3)

        found_tags = []
        for tag in self.tags:
            found_tags.append((tag, words.count(tag)))

        found_tags.sort(key=lambda o: o[1], reverse=True)
        found_tags = found_tags[:self.max_tags_per_text]

        return [tag for tag, count in found_tags]


class SGDClassifierTagger(BaseChoiceTagger):
    default_tags_candidates = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

    def __init__(self, tags: list[str] = None):
        # TODO load weights only, don't train classifier here

        super().__init__(tags=tags or self.default_tags_candidates)

        self.twenty_train = fetch_20newsgroups(subset='train', categories=self.tags, shuffle=True, random_state=42)

        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(self.twenty_train.data)

        self.tfidf_transformer = TfidfTransformer()
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)

        self.clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)
        self.clf.fit(self.X_train_tfidf, self.twenty_train.target)

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        X_new_counts = self.count_vect.transform(texts)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        # TODO predict probability and filter by threshold
        predicted = self.clf.predict(X_new_tfidf)
        tags = [[self.twenty_train.target_names[category]] for category in predicted]
        return tags


print(MostFrequentWordsTagger().get_tags([example]))
print(FindSpecialWordsTagger().get_tags([example]))
print(SGDClassifierTagger().get_tags([example]))
print(SGDClassifierTagger().get_tags(['God is love', 'OpenGL on the GPU is fast']))
