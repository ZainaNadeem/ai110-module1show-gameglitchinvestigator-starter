# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface but the hints and scoring behaved in confusing and incorrect ways. Here are three concrete bugs I found:

**Bug 1: Hints are backwards**
- **Expected:** When my guess is too high, the game should tell me to go *lower*. when my guess is too low, it should tell me to go *higher*.
- **What actually happened:** In `check_guess` (app.py), the messages are flipped — guessing too high shows "📈 Go HIGHER!" and guessing too low shows "📉 Go LOWER!". This sends you in the completely wrong direction every time.

**Bug 2: The secret number switches type on even attempts, breaking comparisons**
- **Expected:** Every guess is compared fairly against the secret number as an integer.
- **What actually happened:** On even-numbered attempts, the code converts `secret` to a string (app.py). The comparison of an integer guess and a string secret uses Python's lexicographical ordering and not numerical ordering. For example, when the secret is `50` as a string and the user guesses `9`, the code compares the string `9` and `50`, finding `9 > 50` because `9 > 5` alphabetically. It outputs "Too High," but in reality, `9` is less than `50`. This game is unwinnable.

**Bug 3: "Hard" difficulty is actually easier than "Normal"**
- **Expected:** Hard difficulty should have a wider number range to make guessing harder.
- **What actually happened:** The range for Hard is `1–50` (app.py), which is *smaller* than Normal's `1–100`. Hard provides fewer tries (5 instead of 8) and a smaller range, which makes it *easier* to guess, contrary to what "Hard" should be implying.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet 4.6, the VS Code extension) as my AI teammate throughout this project.

**Correct suggestion — refactoring logic into `logic_utils.py`:**
I asked the AI to move `check_guess`, `parse_guess`, `get_range_for_difficulty`, and `update_score` out of `app.py` and into `logic_utils.py`, and to fix the backwards-hint bug at the same time. The AI correctly identified that the hint messages were swapped (`"Go HIGHER!"` was firing when `guess > secret`) and rewrote the function so `"Too High"` is returned when the guess exceeds the secret and `"Too Low"` when it falls short. I verified this by reading the new code in (logic_utils.py) and by running `pytest`, which confirmed all hint-direction tests passed.

**Incorrect / misleading suggestion - the `update_score` asymmetry:**
When I asked the AI to explain the scoring logic, it initially described the even/odd attempt penalty for "Too High" as an intentional "streak mechanic." After re-reading the original code carefully, I realized it was just another bug. Guessing too high gave you +5 points on even attempts, which makes no sense for a guessing game. I simplified `update_score` in `logic_utils.py` so that any wrong guess always deducts 5 points and I verified the change made scoring consistent by manually tracing through a few rounds in the debug expander.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only when both automated tests passed *and* I could manually play through the scenario in the live Streamlit app without triggering the wrong behavior.

**Automated tests (`pytest`):**
I ran `venv/bin/python -m pytest tests/test_game_logic.py -v`, which executed 14 tests and reported all passing. The most targeted tests for my two fixes were:
- `test_hint_direction_too_high` and `test_hint_direction_too_low` — directly asserted the corrected hint directions for Bug 1.
- `test_no_string_comparison_edge_case` — asserted that `check_guess(9, 50)` returns `"Too Low"` (not `"Too High"` as the broken string-comparison produced), confirming Bug 2 is gone.
- `test_hard_range_wider_than_normal` — confirmed the Hard difficulty range is now wider than Normal.

**AI help designing tests:**
I asked the AI to generate tests that "specifically target the bugs I just fixed." It suggested using the exact edge case that exposed Bug 2 (`guess=9, secret=50`), which was helpful because I had identified the bug conceptually but hadn't thought to use a single-digit vs two-digit number to expose it as a test case. I verified the test was meaningful by temporarily reverting the fix and confirming the test failed — then re-applying the fix to make it pass again.

---

## 4. What did you learn about Streamlit and state?

Every time a user interacts with a Streamlit widget — clicking a button, changing a dropdown, typing in a text box — Streamlit re-runs the entire Python script from top to bottom. Think of it like refreshing a web page: variables defined with `x = 5` disappear and get re-created fresh each time. `st.session_state` is the exception: it's a persistent dictionary that survives reruns, similar to how a browser stores cookies between page loads. Without session state, the secret number would be re-randomized on every button click (which is actually Bug 2's cousin — the game loses track of context between clicks). Storing `secret`, `attempts`, `score`, and `status` in `st.session_state` is what makes the game remember what happened on previous guesses within the same browser session.

---

## 5. Looking ahead: your developer habits

**One habit I want to reuse:** Writing tests that prove a bug *exists before* fixing it, then confirming the test passes *after*. For Bug 2 (the string-comparison issue), I noted the exact failing case (`check_guess(9, 50)` returning `"Too High"` when it should return `"Too Low"`), wrote `test_no_string_comparison_edge_case` to capture that expectation, temporarily verified it failed, then applied the fix. This "red-then-green" loop gave me confidence the fix was real and not just coincidence.

**One thing I'd do differently:** I'd give the AI a narrower scope on the first prompt. When I asked for help with `update_score`, the AI re-explained a clearly wrong asymmetric penalty as an "intentional streak mechanic." That cost time. In the future I'd ask: *"Is this logic correct for a guessing game where every wrong guess should cost the same?"* — a yes/no framing that forces the AI to evaluate rather than describe.

**How this project changed my thinking:** AI-generated code looks syntactically correct and runs without errors, which makes subtle logic bugs (like reversed comparisons or silent type coercions) much harder to spot than a crash would be. I now treat AI output the same way I'd treat code from a new teammate: read it, understand it, and test the edge cases before trusting it in production.
