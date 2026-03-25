spell-checker
A lightweight spell checker written in pure Python. No pip installs, no external libraries —
just drop in a word list and start checking. It's been tested on dictionaries with over
400,000 words and still returns suggestions in milliseconds.

Why I built this
Most spell checkers either pull in heavy NLP dependencies or rely on OS-level tools.
I wanted something self-contained that I could drop into any Python project without
worrying about the environment. The goal was simple: take a misspelled word, find the
closest real words, and do it fast even on a large dictionary.

How it actually works
The whole thing is built around one idea — edit distance. Given a word you typed,
the algorithm asks: how many changes does it take to turn this into a real word?
There are three types of changes it counts:

Insert — adding a missing letter ("aple" → "apple")
Delete — removing an extra letter ("appple" → "apple")
Replace — swapping a wrong letter ("applo" → "apple")

The word with the fewest changes wins. If multiple words tie, they're sorted alphabetically.

The algorithm, step by step
Edit distance (Levenshtein)
This is the core. For two words s1 and s2, it builds a table where each cell represents
the cost of converting a prefix of one word into a prefix of the other.
prev = [0, 1, 2, ..., len(s2)]     ← base case: converting empty string to s2

for i, char1 in enumerate(s1):
    curr = [i + 1]                  ← cost of converting s1[:i] to empty string

    for j, char2 in enumerate(s2):
        cost    = 0 if char1 == char2 else 1
        insert  = curr[j] + 1           ← add a character
        delete  = prev[j + 1] + 1       ← remove a character
        replace = prev[j] + cost        ← swap a character

        curr[j + 1] = min(insert, delete, replace)

    if min(curr) > max_dist:
        return max_dist + 1         ← early exit — already too far away

    prev = curr

return prev[-1]                     ← final edit distance
The early exit is the key optimization. Once the minimum value in a row already exceeds
the allowed distance, there's no way the final answer will be good enough — so it stops
immediately instead of completing the rest of the table. On a 400k-word dictionary,
this skips an enormous amount of work.

Suggestion search
Before the edit distance even runs, there's a cheaper filter: length difference.
If a candidate word is much shorter or longer than the input, it can't possibly be within
max_dist edits — so it gets skipped without any computation. This alone eliminates
a large chunk of the dictionary on every lookup.
input_word = word.lower()

candidates = []

for word in dictionary:
    if abs(len(word) - len(input_word)) > max_dist:
        continue                        ← length filter, free to compute

    dist = edit_distance(input_word, word, max_dist)

    if dist <= max_dist:
        candidates.append((dist, word))

candidates.sort(key=lambda x: (x[0], x[1]))   ← sort by distance, then alphabetically

return [word for dist, word in candidates[:max_suggestions]]

Setup
No installation needed beyond Python itself.
bashgit clone https://github.com/your-username/spell-checker
cd spell-checker
You'll need a plain text word list — one word per line. The repository is tested with a
standard English dictionary (ENG.txt). You can find one at
dwyl/english-words or use any custom word list.

Usage
pythonfrom main import FastSpellChecker

# Load your word list
with open("ENG.txt", "r") as f:
    word_list = f.readlines()

checker = FastSpellChecker(word_list)
Check a single word:
pythonchecker.suggest("appl")
# ['apple', 'apply', 'applet']

checker.suggest("recieve")
# ['receive']

checker.suggest("teh")
# ['the', 'ten', 'tea']
Correct a full sentence:
pythonchecker.correct_string("see is a goof bay")
# 'he is a good boy'
correct_string() splits the sentence, runs each word through the suggestion engine,
and replaces it with the top match if one is found.

Configuration
Both parameters are optional and have sensible defaults:
ParameterDefaultDescriptionmax_dist2Maximum edit distance to consider a word a valid suggestionmax_suggestions5Number of suggestions to return per word
python# Stricter matching, fewer (but more confident) suggestions
checker = FastSpellChecker(word_list, max_dist=1)

# Fuzzier matching, useful for heavily garbled input
checker = FastSpellChecker(word_list, max_dist=3)
Lowering max_dist also speeds things up — fewer candidates survive the filter.

Limitations
A few things worth knowing before you use this:

No context awareness. Each word is corrected in isolation. The sentence
"I saw the batman" and "I saw the batsman" are treated identically word by word.
If you need context-sensitive correction, you'd need something built on top of this.
Proper nouns and jargon. If a word isn't in your dictionary, it won't be suggested.
For domain-specific use (medical terms, code identifiers, names), you'll want to supply
a custom word list.
Performance scales with dictionary size. The early-exit and length filter make this
practical on large lists, but it's still O(n) over the dictionary per word. For real-time
applications on very large inputs, consider caching results for common words.


File structure
spell-checker/
├── main.py        ← FastSpellChecker class, edit distance, suggestion logic
├── ENG.txt        ← word list (not included — bring your own)
└── README.md

Contributing
If you find a bug or want to suggest an improvement, open an issue or send a pull request.
The codebase is small and straightforward — the core logic is under 100 lines.
