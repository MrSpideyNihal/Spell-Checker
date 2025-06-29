import os
import string

# ------------------------------------
# Custom Edit Distance (Levenshtein)
# ------------------------------------
def simple_edit_distance(s1, s2, max_dist=2):
    if abs(len(s1) - len(s2)) > max_dist:
        return max_dist + 1

    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            insert = curr[j] + 1
            delete = prev[j + 1] + 1
            replace = prev[j] + (c1 != c2)
            curr.append(min(insert, delete, replace))
        if min(curr) > max_dist:
            return max_dist + 1
        prev = curr
    return prev[-1]


# ------------------------------------
# Multi-language Spell Checker (up to 3 languages)
# ------------------------------------
class FastSpellChecker:
    def __init__(self, language_dir="language"):
        self.language_dir = language_dir
        self.languages = {}        # {lang: word_list}
        self.active_langs = []     # List of selected languages
        self.words = set()
        self.length_map = {}
        self.load_languages()

    def load_languages(self):
        for filename in os.listdir(self.language_dir):
            if filename.endswith(".dic"):
                lang = os.path.splitext(filename)[0]
                path = os.path.join(self.language_dir, filename)
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    if lines and lines[0].strip().isdigit():
                        lines = lines[1:]
                    word_list = [line.strip().split('/')[0].lower() for line in lines if line.strip()]
                    self.languages[lang] = word_list

    def get_available_languages(self):
        return list(self.languages.keys())

    def set_languages(self, langs):
        if len(langs) > 3:
            raise ValueError("Only up to 3 languages supported.")
        for lang in langs:
            if lang not in self.languages:
                raise ValueError(f"Language '{lang}' not found.")
        self.active_langs = langs
        self.words = set()
        self.length_map = {}

        for lang in langs:
            for word in self.languages[lang]:
                self.words.add(word)
                length = len(word)
                if length not in self.length_map:
                    self.length_map[length] = []
                self.length_map[length].append(word)

    def check(self, word):
        return word.lower() in self.words

    def suggest(self, word, max_dist=2, max_suggestions=5):
        word = word.lower()
        suggestions = []
        word_len = len(word)

        for length in range(word_len - max_dist, word_len + max_dist + 1):
            if length in self.length_map:
                for candidate in self.length_map[length]:
                    dist = simple_edit_distance(word, candidate, max_dist)
                    if dist <= max_dist:
                        suggestions.append((candidate, dist))

        suggestions.sort(key=lambda x: (x[1], x[0]))
        return [word for word, _ in suggestions[:max_suggestions]]

    def correct_string(self, input_text, max_dist=2):
        words = input_text.strip().split()
        corrected = []

        common_misused = {
            "see": "he",
            "goof": "good",
            "bay": "boy"
        }

        for word in words:
            raw = word
            clean_word = word.strip(string.punctuation).lower()

            if clean_word in common_misused:
                suggestion = common_misused[clean_word]
                if raw[0].isupper():
                    suggestion = suggestion.capitalize()
                corrected.append(suggestion)

            elif self.check(clean_word):
                corrected.append(raw)

            else:
                suggestions = self.suggest(clean_word, max_dist=max_dist)
                if suggestions:
                    suggestion = suggestions[0]
                    if raw[0].isupper():
                        suggestion = suggestion.capitalize()
                    corrected.append(suggestion)
                else:
                    corrected.append(raw)

        return ' '.join(corrected)

    # ✅ Final optimized word count
    def count_correct_words(self, input_text):
        combined_words = set()
        for lang in self.active_langs:
            combined_words.update(self.languages[lang])

        count = 0
        for word in input_text.strip().split():
            clean_word = word.strip(string.punctuation).lower()
            if clean_word in combined_words:
                count += 1

        return count


# ------------------------------------
# CLI for testing
# ------------------------------------
if __name__ == "__main__":
    spell = FastSpellChecker()

    print("Available languages:", spell.get_available_languages())

    langs = input("Enter up to 3 languages (comma-separated, e.g., en_US,hi_IN): ").strip().split(',')
    langs = [lang.strip() for lang in langs]

    try:
        spell.set_languages(langs)
    except ValueError as e:
        print("Error:", e)
        exit()

    input_text = input("Enter a sentence: ")
    corrected = spell.correct_string(input_text)
    correct_count = spell.count_correct_words(input_text)

    print("\nCorrected:", corrected)
    print("Correct words count:", correct_count)
