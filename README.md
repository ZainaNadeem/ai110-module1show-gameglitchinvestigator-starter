# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### What the game does
Game Glitch Investigator is a number-guessing game built with Streamlit. The player picks a difficulty (Easy / Normal / Hard), which sets the number range and attempt limit. Each round a secret integer is randomly chosen; the player submits guesses and receives "Too High" / "Too Low" hints until they guess correctly or exhaust their attempts. A running score rewards faster wins.

### Bugs found
1. Backwards hints
Location: app.py → check_guess
The game displayed incorrect guidance to the player. When the guess was higher than the secret number, it incorrectly showed “Go HIGHER!” instead of “Go LOWER!”, and vice versa. This caused players to move in the wrong direction every time.
2. Secret type switching on even attempts
Location: app.py lines 158–163
On even-numbered attempts, the secret number was converted to a string. This caused Python to compare values lexicographically instead of numerically (for example, "9" > "50" evaluates to True), making the game behave incorrectly and sometimes impossible to win.
3. Hard difficulty easier than Normal
Location: app.py → get_range_for_difficulty
The difficulty settings were inconsistent. Hard mode used a smaller number range (1–50) compared to Normal mode (1–100), despite offering fewer attempts. This made Hard mode unintentionally easier than Normal.

### Fixes applied
- **Bug 1:** Swapped the comparison branches in `check_guess` so `guess > secret` → `"Too High"` and `guess < secret` → `"Too Low"`.
- **Bug 2:** Removed the even/odd type-switch block entirely. The secret is always compared as an integer.
- **Bug 3:** Changed Hard's range to `1–200`, making it genuinely harder than Normal's `1–100`.
- **Refactor:** All four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) were moved from `app.py` into `logic_utils.py` so they can be unit-tested independently of the Streamlit UI.
- **Tests:** Added 11 new pytest cases (14 total) targeting each bug fix. Run with `venv/bin/python -m pytest tests/ -v`.

## 📸 Demo


https://github.com/user-attachments/assets/47d89e34-104e-4150-bce0-48f58ceff4ad




