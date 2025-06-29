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
# Fast Spell Checker Without Modules
# ------------------------------------
class FastSpellChecker:
    def __init__(self, word_list):
        self.words = set()
        self.length_map = {}

        for word in word_list:
            word = word.strip().lower()
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
            clean_word = word.strip(".,!?\"'").lower()
    
            # Step 1: Use hardcoded replacement if exists
            if clean_word in common_misused:
                suggestion = common_misused[clean_word]
                if raw[0].isupper():
                    suggestion = suggestion.capitalize()
                corrected.append(suggestion)
    
            # Step 2: If correct, keep it
            elif self.check(clean_word):
                corrected.append(raw)
    
            # Step 3: Otherwise suggest spelling fix
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
    
# ------------------------------------
# Test the Spell Checker
# ------------------------------------
if __name__ == "__main__":
    with open("Eng.txt", "r") as file:
        word_list = file.readlines()

    spell = FastSpellChecker(word_list)

    input_text = input("Enter a sentence: ")
    corrected = spell.correct_string(input_text)
    print("Corrected:", corrected)

