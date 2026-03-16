from logic_utils import check_guess, HINT_MESSAGES

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


def test_hint_messages_not_swapped():
    # Regression test for the high/low hint swap bug.
    # When the guess is too high, the player should be told to go LOWER (not higher).
    # When the guess is too low, the player should be told to go HIGHER (not lower).
    assert "LOWER" in HINT_MESSAGES["Too High"], (
        "Too High hint should tell the player to go LOWER"
    )
    assert "HIGHER" in HINT_MESSAGES["Too Low"], (
        "Too Low hint should tell the player to go HIGHER"
    )
