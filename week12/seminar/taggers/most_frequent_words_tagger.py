import string
from collections import Counter

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .base import extract_words, BaseTagger, BaseSeparateTagger, STOP_WORDS_ALIR3Z4

# nltk.download()  1st time


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
        while i < len(result) and result[i][1] == max_count:
            tags.append(result[i][0])
            i += 1

        return tags[:self.max_tags_per_text]


class PartOfSpeechTagger(BaseSeparateTagger):
    def __init__(self):
        super().__init__()

    def get_tags_from_text(self, text: str) -> list[str]:
        tkns = nltk.word_tokenize(text)
        part_of_speech = nltk.pos_tag(tkns)
        main_words = [w[0] for w in part_of_speech if
                      w[1] in ['NN', 'JJ']]  # we will use only Nouns (NN) and Adjective (JJ)
        main_words = [n for n in main_words if len(n) > 3]

        main_words = [word for word in main_words if word not in STOP_WORDS_ALIR3Z4]

        number_of_tags = min(4, round(len(main_words) * 0.2))  # get 4 tags or less, if we have short sentences

        vocabl = set(main_words)
        frequency = sorted([(main_words.count(i), i) for i in vocabl], reverse=True)

        return [tg[1] for tg in frequency[:number_of_tags]]


class TfidfTagger(BaseTagger):
    default_stop_words = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))

    def __init__(self, stop_words: list = None, max_tags_per_text: int = 5):
        super().__init__()
        self.stop_words = stop_words or self.default_stop_words
        self.max_tags_per_text = max_tags_per_text
        self.vectorizer = TfidfVectorizer()
        self.corpus_vectorized = None

    def get_tags(self, texts: list[str], k: int = 5,
                 thr: float = 0.8, min_tag_len: int = 4) -> list[list[str]]:
        new_corpus = [' '.join([w for w in nltk.tokenize.word_tokenize(text.lower())
                                if w not in self.stop_words]) for text in texts]
        if not new_corpus:
            return []

        self.corpus_vectorized = self.vectorizer.fit_transform(new_corpus)
        all_words = self.vectorizer.get_feature_names_out()
        result = []
        for i in range(len(texts)):
            tfidf_vector = self.corpus_vectorized[i].toarray()[0]
            best_k_ixes = np.argpartition(tfidf_vector, -k)[-k:]
            scores = tfidf_vector[best_k_ixes]
            best_score = max(scores)
            mask = scores / best_score > thr
            best_ixes = best_k_ixes[mask]

            tags = [w for w in all_words[best_ixes] if len(w) >= min_tag_len]
            result.append(tags)
        return result
