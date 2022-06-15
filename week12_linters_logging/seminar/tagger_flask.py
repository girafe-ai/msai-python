import os

from flask import Flask
from flask import request
from taggers import FindSpecialWordsTagger
from taggers import MostFrequentWordsTagger
from taggers import PartOfSpeechTagger
from taggers import SGDClassifierTagger

app = Flask(__name__)
tagger_objects = [
    FindSpecialWordsTagger(),
    MostFrequentWordsTagger(), PartOfSpeechTagger(),
    SGDClassifierTagger(),
]


@app.route('/internal/tagging', methods=['POST'])
def tagging():
    texts = request.json['texts']
    tags = [set() for _ in texts]  # [{text1-tag1, text1-tag2, ...}, ...]
    for tagger in tagger_objects:
        result = tagger.get_tags(texts)
        # merge tags of same text from different taggers
        for text_tags_set, text_tags in zip(tags, result):
            text_tags_set |= set(text_tags)

    tags = [list(text_tags_set) for text_tags_set in tags]
    return {
        'tags': tags,
    }


if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    # app.run(port=port, threaded=True)  # threaded variant
    app.run(port=port, threaded=False, processes=4)  # processed variant
