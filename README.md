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
| # | Bug | Location |
|---|-----|----------|
| 1 | **Hints were backwards** — "Go HIGHER!" fired when the guess was *above* the secret, sending the player in the wrong direction every time. | `app.py` → `check_guess` |
| 2 | **Secret type-switched on even attempts** — the secret was cast to `str` on even-numbered guesses, so Python used lexicographic ordering (`"9" > "50"` = True) instead of numeric ordering, making the game unwinnable half the time. | `app.py` lines 158–163 |
| 3 | **Hard difficulty was easier than Normal** — Hard had a range of 1–50 (smaller than Normal's 1–100) despite offering fewer attempts. | `app.py` → `get_range_for_difficulty` |

### Fixes applied
- **Bug 1:** Swapped the comparison branches in `check_guess` so `guess > secret` → `"Too High"` and `guess < secret` → `"Too Low"`.
- **Bug 2:** Removed the even/odd type-switch block entirely. The secret is always compared as an integer.
- **Bug 3:** Changed Hard's range to `1–200`, making it genuinely harder than Normal's `1–100`.
- **Refactor:** All four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) were moved from `app.py` into `logic_utils.py` so they can be unit-tested independently of the Streamlit UI.
- **Tests:** Added 11 new pytest cases (14 total) targeting each bug fix. Run with `venv/bin/python -m pytest tests/ -v`.

## 📸 Demo

> **pytest results — all 14 tests passing**

```
============================= test session starts ==============================
tests/test_game_logic.py::test_winning_guess                         PASSED
tests/test_game_logic.py::test_guess_too_high                        PASSED
tests/test_game_logic.py::test_guess_too_low                         PASSED
tests/test_game_logic.py::test_hint_direction_too_high               PASSED
tests/test_game_logic.py::test_hint_direction_too_low                PASSED
tests/test_game_logic.py::test_no_string_comparison_edge_case        PASSED
tests/test_game_logic.py::test_no_string_comparison_large_vs_small   PASSED
tests/test_game_logic.py::test_parse_valid_integer                   PASSED
tests/test_game_logic.py::test_parse_empty_string                    PASSED
tests/test_game_logic.py::test_parse_non_numeric                     PASSED
tests/test_game_logic.py::test_parse_decimal_truncates               PASSED
tests/test_game_logic.py::test_hard_range_wider_than_normal          PASSED
tests/test_game_logic.py::test_easy_range                            PASSED
tests/test_game_logic.py::test_normal_range                          PASSED
============================== 14 passed in 0.01s ==============================
```

*(Replace this block with a real screenshot of your terminal once you have run `pytest` locally — use your OS snipping tool or `Cmd+Shift+4` on macOS.)*

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
