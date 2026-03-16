def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 10),
        "Medium": (1, 50),
        "Hard": (1, 100),
    }
    if difficulty not in ranges:
        raise ValueError(f"Unknown difficulty: {difficulty!r}. Choose from {list(ranges)}")
    return ranges[difficulty]


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    try:
        return (True, int(raw.strip()), None)
    except (ValueError, AttributeError):
        return (False, None, "Please enter a whole number.")


def check_guess(guess, secret):
    """
    Compare guess to secret and return outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win"
    elif guess > secret:
        return "Too High"
    else:
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome != "Win":
        return current_score
    bonus = max(0, 10 - attempt_number + 1)
    return current_score + bonus
