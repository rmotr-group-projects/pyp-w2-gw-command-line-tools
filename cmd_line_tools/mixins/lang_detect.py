class LangDetectMixin(object):
    #words here ought be lowercase and punctuation free
    #and will be assumed to be such
    #LANGUAGES = []
    def detect_language(self, text):
        counts = {lang['name']:0 for lang in self.LANGUAGES}
        def cleaner(word):
            return ''.join(c.lower() for c in word if c.isalpha())
        words = [cleaner(w) for w in text.split()]
        for w in words:
            for lang in self.LANGUAGES:
                if w in lang['common_words']:
                    counts[lang['name']] += 1
        return max(counts, key = counts.get)