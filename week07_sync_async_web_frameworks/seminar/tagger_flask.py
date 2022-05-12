from flask import Flask, request

from taggers import MostFrequentWordsTagger, FindSpecialWordsTagger, SGDClassifierTagger

app = Flask(__name__)
taggers = [
    MostFrequentWordsTagger(),
    FindSpecialWordsTagger(),
    SGDClassifierTagger()
]


@app.route("/internal/tagging", methods=['POST'])
def tagging():
    texts = request.json['texts']
    tags = [set() for _ in texts]  # [{text1-tag1, text1-tag2, ...}, ...]
    for tagger in taggers:
        result = tagger.get_tags(texts)
        # merge tags of same text from different taggers
        for text_tags_set, text_tags in zip(tags, result):
            text_tags_set |= set(text_tags)

    tags = [list(text_tags_set) for text_tags_set in tags]
    return {
        'tags': tags
    }


if __name__ == '__main__':
    # app.run(threaded=True)  # threaded variant
    app.run(threaded=False, processes=4)  # processed variant
