import pytest

from taggers import (
    CatBoostClassifierTagger,
    FindSpecialWordsTagger,
    MostFrequentWordsTagger, PartOfSpeechTagger, TfidfTagger,
    SGDClassifierTagger, SGDClassifierTestTagger
)
from tests.texts_for_test import test_texts


@pytest.mark.parametrize(
    "texts",
    [
        [],
        ['text'],
        ['test text'],
        ['test', 'text'],
        test_texts,
    ],
)
@pytest.mark.parametrize(
    "tagger",
    [
        MostFrequentWordsTagger(),
        PartOfSpeechTagger(),
        # TfidfTagger(),  TODO
        FindSpecialWordsTagger(),
        # SGDClassifierTestTagger(),  TODO
        SGDClassifierTagger(),
        # CatBoostClassifierTagger()  TODO
    ],
)
def test_taggers(texts, tagger):
    result = tagger.get_tags(texts)
    assert isinstance(result, list)
    assert len(result) == len(texts)
    assert all(isinstance(r, list) for r in result)
    # TODO go deeper and check types of string, their length, etc.
