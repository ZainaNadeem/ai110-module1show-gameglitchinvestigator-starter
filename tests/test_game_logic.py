from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# ── Starter tests ────────────────────────────────────────────────────────────

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# ── Bug 1 fix: hints were backwards ─────────────────────────────────────────
# Before the fix, check_guess returned "Too High" when guess < secret and
# "Too Low" when guess > secret.  These tests confirm the corrected direction.

def test_hint_direction_too_high():
    """Guess of 60 vs secret of 50: player is too high, must go lower."""
    assert check_guess(60, 50) == "Too High"

def test_hint_direction_too_low():
    """Guess of 9 vs secret of 50: player is too low, must go higher."""
    assert check_guess(9, 50) == "Too Low"

# ── Bug 2 fix: type-switching secret caused wrong comparisons ────────────────
# Original code converted the secret to a string on even attempts, so
# lexicographic ordering was used instead of numeric ordering.
# e.g. str(50) = "50"; "9" > "50" alphabetically → wrong "Too High" outcome.
# After the fix, check_guess always compares integers.

def test_no_string_comparison_edge_case():
    """Guess of 9 vs integer secret 50 must be Too Low, not Too High."""
    # This was the classic failure: "9" > "50" lexicographically is True,
    # so the old code returned "Too High" — the wrong answer.
    assert check_guess(9, 50) == "Too Low"

def test_no_string_comparison_large_vs_small():
    """Guess of 100 vs secret 9 must be Too High (not confused by digit length)."""
    assert check_guess(100, 9) == "Too High"

# ── parse_guess ───────────────────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False

def test_parse_decimal_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

# ── get_range_for_difficulty ──────────────────────────────────────────────────

def test_hard_range_wider_than_normal():
    """Hard should have a wider range than Normal to actually be harder."""
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100
