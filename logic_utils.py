              
#FIXME:logic breaks here
def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive numeric range for a given difficulty level.

    Maps a difficulty label to a (low, high) tuple that defines the
    range of possible secret numbers for that difficulty setting.

    Args:
        difficulty (str): The difficulty level. Must be one of
            ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        tuple[int, int]: A ``(low, high)`` pair representing the
        inclusive lower and upper bounds of the guessing range.

    Raises:
        ValueError: If ``difficulty`` is not a recognised difficulty label.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 10)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    ranges = {
        "Easy": (1, 10),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    if difficulty not in ranges:
        raise ValueError(f"Unknown difficulty: {difficulty!r}. Choose from {list(ranges)}")
    return ranges[difficulty]


def parse_guess(raw: str):
    """
    Parse raw user input into a validated integer guess.

    Strips surrounding whitespace from the input and attempts to
    convert it to an integer. Returns a 3-tuple so the caller can
    branch on success without catching exceptions.

    Args:
        raw (str): The raw string entered by the user. May be
            ``None``, empty, or contain non-numeric characters.

    Returns:
        tuple: A 3-tuple of ``(ok, guess_int, error_message)`` where:

        - ``ok`` (bool): ``True`` if parsing succeeded, ``False`` otherwise.
        - ``guess_int`` (int | None): The parsed integer on success, or
          ``None`` on failure.
        - ``error_message`` (str | None): A human-readable error string on
          failure, or ``None`` on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'Please enter a whole number.')
        >>> parse_guess("  7  ")
        (True, 7, None)
    """
    try:
        return (True, int(raw.strip()), None)
    except (ValueError, AttributeError):
        return (False, None, "Please enter a whole number.")


HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def check_guess(guess, secret):
    """
    Compare a player's guess against the secret number and return an outcome.

    Performs a simple three-way comparison. The return value is a plain
    string so it can be used as a dict key into ``HINT_MESSAGES`` or
    tested directly in assertions.

    Args:
        guess (int | float): The number the player guessed.
        secret (int | float): The target number the player is trying to find.

    Returns:
        str: One of three outcome strings:

        - ``"Win"``      — guess exactly equals the secret.
        - ``"Too High"`` — guess is greater than the secret.
        - ``"Too Low"``  — guess is less than the secret.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
    """
    if guess == secret:
        return "Win"
    elif guess > secret:
        return "Too High"
    else:
        return "Too Low"


def save_game_score(score_history: list, score: int, outcome: str, attempts: int, difficulty: str) -> list:
    """
    Append a completed game's result to the score history list.

    Creates a record for the just-finished game and returns a new list
    with that record appended. The original list is not mutated.

    Args:
        score_history (list): The existing list of past game records,
            where each entry is a dict produced by this function.
        score (int): The final score earned in the completed game.
        outcome (str): The game outcome — ``"won"`` or ``"lost"``.
        attempts (int): The number of attempts used in the completed game.
        difficulty (str): The difficulty setting, e.g. ``"Easy"``, ``"Normal"``,
            or ``"Hard"``.

    Returns:
        list: A new list equal to ``score_history`` plus one appended record.
        Each record is a dict with keys:

        - ``"game"`` (int): 1-based game number.
        - ``"score"`` (int): Final score for the game.
        - ``"outcome"`` (str): ``"won"`` or ``"lost"``.
        - ``"attempts"`` (int): Number of attempts used.
        - ``"difficulty"`` (str): Difficulty level played.

    Examples:
        >>> save_game_score([], 10, "won", 3, "Normal")
        [{'game': 1, 'score': 10, 'outcome': 'won', 'attempts': 3, 'difficulty': 'Normal'}]
        >>> history = save_game_score([], 10, "won", 3, "Normal")
        >>> save_game_score(history, 0, "lost", 8, "Hard")
        [{'game': 1, ...}, {'game': 2, 'score': 0, 'outcome': 'lost', 'attempts': 8, 'difficulty': 'Hard'}]
    """
    record = {
        "game": len(score_history) + 1,
        "score": score,
        "outcome": outcome,
        "attempts": attempts,
        "difficulty": difficulty,
    }
    return score_history + [record]


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate the new cumulative score after a guess attempt.

    Score is only awarded on a win. The bonus decreases by one point
    for each attempt taken, rewarding players who guess in fewer tries.
    The minimum bonus is capped at 0 so the score can never decrease
    on a winning guess.

    Scoring formula::

        bonus = max(0, 10 - attempt_number + 1)
        new_score = current_score + bonus

    Args:
        current_score (int): The player's score before this attempt.
        outcome (str): The outcome string from ``check_guess()``.
            Only ``"Win"`` awards points; all other values are ignored.
        attempt_number (int): The 1-based number of the current attempt.
            Lower values yield a higher bonus.

    Returns:
        int: The updated score. Unchanged if ``outcome`` is not ``"Win"``.

    Examples:
        >>> update_score(0, "Win", 1)
        10
        >>> update_score(0, "Win", 5)
        6
        >>> update_score(20, "Too High", 3)
        20
    """
    if outcome != "Win":
        return current_score
    bonus = max(0, 10 - attempt_number + 1)
    return current_score + bonus
