import unittest

from taggers import CatBoostClassifierTagger
from taggers import FindSpecialWordsTagger
from taggers import MostFrequentWordsTagger
from taggers import PartOfSpeechTagger
from taggers import SGDClassifierTagger
from taggers import SGDClassifierTestTagger
from taggers import TfidfTagger

from .texts_for_test import test_texts


class TestStringMethods(unittest.TestCase):

    def test_most_frequent_words_tagger(self):
        result = MostFrequentWordsTagger().get_tags(test_texts)
        self.assertEqual(
            result,
            [
                ['design', 'patterns'],
                ['healthy'],
                ['missions', 'launch'],
                ['sell', 'floppy', 'disks'],
                ['god'],
            ],
        )

    def test_part_of_speech_tagger(self):
        result = PartOfSpeechTagger().get_tags(test_texts)
        self.assertEqual(
            result,
            [
                ['design', 'software', 'programming', 'application'],
                ['healthy', 'lifestyle', 'life', 'person'],
                ['space', 'rocket', 'launch', 'tourist-focused'],
                [],
                [],
            ],
        )

    def test_tfidf_tagger(self):
        result = TfidfTagger().get_tags(test_texts)
        self.assertEqual(
            result,
            [
                ['design', 'patterns'],
                ['healthy'],
                ['launch', 'missions'],
                ['disks', 'floppy', 'sell'],
                [],
            ],
        )

    def test_find_special_words_tagger(self):
        result = FindSpecialWordsTagger().get_tags(test_texts)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertTrue(any(isinstance(r, list) for r in result))
        # TODO go deeper and check types of string, their length, etc.

    def test_sgd_classifier_test_tagger(self):
        result = SGDClassifierTestTagger().get_tags(test_texts)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertTrue(any(isinstance(r, list) for r in result))
        # TODO go deeper and check types of string, their length, etc.

    def test_sgd_classifier_tagger(self):
        result = SGDClassifierTagger().get_tags(test_texts)
        self.assertEqual(
            result,
            [
                ['comp.graphics', 'sci.electronics'],
                ['sci.med', 'talk.religion.misc'],
                ['sci.space'],
                ['misc.forsale', 'comp.sys.ibm.pc.hardware'],
                ['soc.religion.christian'],
            ],
        )

    @unittest.skip
    def test_cat_boost_classifier_tagger(self):
        result = CatBoostClassifierTagger().get_tags(test_texts)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertTrue(any(isinstance(r, list) for r in result))
        # TODO go deeper and check types of string, their length, etc.


if __name__ == '__main__':
    unittest.main()
