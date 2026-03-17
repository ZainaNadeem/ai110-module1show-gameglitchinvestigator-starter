def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Original code returned (1, 50) for Hard, which is a *smaller* range
        # than Normal (1-100). Hard should have a wider range to match the harder
        # difficulty. Refactored into logic_utils.py using Copilot Agent mode.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Moved from app.py into logic_utils.py using Copilot Agent mode so
    # this logic can be tested independently of the Streamlit UI.
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low"
    """
    # FIXME was here: original code returned "Go HIGHER!" when guess > secret
    # and "Go LOWER!" when guess < secret — exactly backwards.
    #
    # FIX: Corrected the hint direction. When guess > secret the number is too
    # high (player must go lower), and when guess < secret it is too low (player
    # must go higher). Refactored into logic_utils.py and fixed using Copilot
    # Agent mode; verified with pytest and manual play-through.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Moved from app.py into logic_utils.py using Copilot Agent mode.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
