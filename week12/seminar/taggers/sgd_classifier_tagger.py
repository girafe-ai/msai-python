import pickle
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

from .base import BaseChoiceTagger, BaseTagger


class SGDClassifierTestTagger(BaseChoiceTagger):
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


class SGDClassifierTagger(BaseTagger):
    def __init__(self, classification_threshold=0.2, filename_with_weights="taggers/model_weights.pik"):
        super().__init__()

        self.classification_threshold = classification_threshold
        self.classifier = Pipeline(
            [('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
             ('clf_svm', SGDClassifier(learning_rate='adaptive', eta0=0.1, loss='modified_huber', penalty='elasticnet',
                                       tol=1e-5, alpha=1e-5, max_iter=50, early_stopping=True, random_state=42))])

        twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
        self.targets = twenty_test.target_names

        try:
            self.classifier = pickle.load(open(filename_with_weights, 'rb'))
            print("The model fitted from pre-saved weights")

        except FileNotFoundError as error:
            print("The model needs fitting as no pre-fitted weights are available")
            twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

            self.classifier = self.classifier.fit(twenty_train.data, twenty_train.target)
            predictions = self.classifier.predict(twenty_test.data)
            print(f"Model accuracy:{np.mean(predictions == twenty_test.target):.2f}")

            pickle.dump(self.classifier, open(filename_with_weights, 'wb'))

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        tags = []
        tag_scores = []
        for text in texts:
            predictions = self.classifier.predict_proba([text])[0].tolist()
            sorted_scores = [(predictions[i], predictions.index(predictions[i])) for i in range(len(predictions))]
            sorted_scores = sorted(sorted_scores, reverse=True, key=lambda x: x[0])
            valid_predictions = []
            valid_predictions_scores = []

            for v in range(len(sorted_scores)):
                if sorted_scores[v][0] >= self.classification_threshold:
                    valid_predictions.append(self.targets[sorted_scores[v][1]])
                    valid_predictions_scores.append(sorted_scores[v][0])
            tags.append(valid_predictions)
            tag_scores.append(valid_predictions_scores)

        # return tags, tag_scores
        return tags
