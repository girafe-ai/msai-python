from .base import extract_words, BaseSeparateTagger, BaseChoiceTagger, POPULAR_TAGS


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
            tag_entries = words.count(tag)
            if tag_entries:
                found_tags.append((tag, tag_entries))

        found_tags.sort(key=lambda o: o[1], reverse=True)
        found_tags = found_tags[:self.max_tags_per_text]

        return [tag for tag, count in found_tags]
