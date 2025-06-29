# 🪄 Spell Checker – A Fast Python Library

A fast, lightweight spell checker built in pure Python — no external modules required.  
It handles large dictionaries and suggests smart corrections using **edit distance**.

---

## 🔍 How It Works

### ✅ 1. Efficient Word Matching Using Edit Distance

We calculate how many changes are needed to convert a user word into each dictionary word using:

- ✏️ Insert  
- ❌ Delete  
- 🔁 Replace  

This is done using a custom **Levenshtein Distance** algorithm optimized with early exit.

---

### 🧠 Edit Distance Algorithm

If absolute length difference > max_dist:
→ Return max_dist + 1 (skip this word)

Initialize prev[] with values from 0 to len(s2)

For each character in s1:
a. Start a new row curr[] with [i + 1]

b. For each character in s2:
i. If characters match, cost = 0
Else, cost = 1
ii. Calculate insert, delete, replace costs
iii. curr[j + 1] = min(insert, delete, replace)

c. If min(curr) > max_dist:
→ Early exit (too different)

d. Set prev = curr

Return prev[-1] as final edit distance

yaml
Copy
Edit

---

### 🔎 Suggestion Search Algorithm

Input:
word_to_check → the user input word
dictionary → list of words
max_dist → allowed edit distance (default: 2)
max_suggestions → number of best matches to return

Steps:

Lowercase the word

For each word in the dictionary:
a. Skip if length difference > max_dist
b. Compute edit distance
c. If distance ≤ max_dist → store it

Sort suggestions by (distance, then alphabet)

Return top N suggestions

python
Copy
Edit

---

## 💡 Example Usage
python
from main import FastSpellChecker
# Load dictionary
with open("dictionary.txt", "r") as f:
    word_list = f.readlines()

checker = FastSpellChecker(word_list)

# Single word check
print(checker.suggest("appl"))  # ['apple', 'apply', 'applet']

# Full sentence correction
text = "see is a goof bay"
print(checker.correct_string(text))  # he is a good boy


✅ Features
⚙️ Pure Python — no third-party libraries

🔠 Fast suggestion system with early-exit

📄 Can handle large dictionaries (tested with 400,000+ words)

🧠 Supports sentence-level correction with correct_string()

🔎 Word distance cutoff to speed up search
