import pickle

from catboost import CatBoostClassifier
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from .base import BaseChoiceTagger
from .base import extract_words
from .base import STOP_WORDS_ALIR3Z4


class CatBoostClassifierTagger(BaseChoiceTagger):
    default_stop_words = STOP_WORDS_ALIR3Z4
    words_alphabet = "abcdefghijklmnopqrstuvwxyz-'"
    default_tags_candidates = [
        'alt.atheism',
        'sci.space',
        'soc.religion.christian',
        'sci.med',
        'talk.politics.guns',
        'sci.electronics',
    ]

    def __init__(
        self,
        tags: list[str] = None,
        stop_words=None,
        clf_pretrained=None,
        confidence_measures=None,
        use_gpu=False,
    ):
        super().__init__(tags=tags or self.default_tags_candidates)
        self.stop_words = stop_words or self.default_stop_words
        if confidence_measures:
            self.confidence_measures = confidence_measures
        else:
            self.confidence_measures = 1 / len(self.tags)

        self.twenty_train = fetch_20newsgroups(
            subset='train', categories=self.tags, shuffle=True,
        )
        self.train_data = [
            ' '.join(
                extract_words(
                    z, self.words_alphabet, min_length=1, stop_words=self.stop_words,
                ),
            )
            for z in self.twenty_train.data
        ]

        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(self.train_data)

        self.tfidf_transformer = TfidfTransformer()
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(
            X_train_counts,
        )

        if clf_pretrained:
            self.clf = clf_pretrained
        else:
            if use_gpu:
                self.clf = CatBoostClassifier(
                    task_type='GPU', devices='0:1', num_trees=100, depth=11,
                )
            else:
                self.clf = CatBoostClassifier(num_trees=100, depth=11)
            self.clf.fit(
                self.X_train_tfidf,
                self.twenty_train.target, silent=False,
            )

    def save_model(self, model_name='tagger_model.pkl'):
        with open(model_name, 'wb') as file:
            pickle.dump(self.clf, file)

    def load_model(self, model_name='tagger_model.pkl'):
        with open(model_name, 'rb') as file:
            self.clf = pickle.load(file)

    def ret_model(self):
        return self.clf

    def get_model(self, clf):
        self.clf = clf

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        texts = [
            ' '.join(
                extract_words(
                    z, self.words_alphabet, min_length=1, stop_words=self.stop_words,
                ),
            )
            for z in texts
        ]
        X_new_counts = self.count_vect.transform(texts)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        predicted = []
        for text_probs in self.clf.predict_proba(X_new_tfidf):
            tmp = []
            for num, j in enumerate(text_probs):
                if j >= self.confidence_measures:
                    tmp.append(num)
            predicted.append(tmp)
        tags = [
            [
                self.twenty_train.target_names[category]
                for category in text_ind_cat
            ]
            for text_ind_cat in predicted
        ]
        return tags
