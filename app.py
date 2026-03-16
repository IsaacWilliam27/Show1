import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, save_game_score, HINT_MESSAGES

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")


def get_streak(score_history: list) -> tuple[int, str]:
    """
    Return (streak_length, streak_type) derived from score_history.

    Counts how many of the most recent games share the same outcome.

    Returns:
        tuple: (count, "win") | (count, "loss") | (0, "none")
    """
    if not score_history:
        return 0, "none"
    last_outcome = score_history[-1]["outcome"]
    count = 0
    for record in reversed(score_history):
        if record["outcome"] == last_outcome:
            count += 1
        else:
            break
    streak_type = "win" if last_outcome == "won" else "loss"
    return count, streak_type


def render_streak_banner(streak_length: int, streak_type: str) -> None:
    """Inject a CSS-animated streak banner above the game."""
    if streak_length < 2:
        return

    if streak_type == "win":
        emoji = "🔥" * min(streak_length, 5)
        label = f"WIN STREAK  ×{streak_length}"
        css = """
        @keyframes fire-pulse {
            0%   { box-shadow: 0 0 8px #ff4500, 0 0 20px #ff6600; }
            50%  { box-shadow: 0 0 20px #ff0000, 0 0 40px #ff4500; }
            100% { box-shadow: 0 0 8px #ff4500, 0 0 20px #ff6600; }
        }
        .streak-banner {
            animation: fire-pulse 1.2s ease-in-out infinite;
            background: linear-gradient(135deg, #ff4500 0%, #ff8c00 50%, #ffd700 100%);
            border-radius: 12px;
            padding: 14px 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: 0.05em;
            text-shadow: 0 1px 4px rgba(0,0,0,0.4);
            margin-bottom: 8px;
        }
        """
    else:
        emoji = "❄️" * min(streak_length, 5)
        label = f"LOSS STREAK  ×{streak_length}"
        css = """
        @keyframes ice-pulse {
            0%   { box-shadow: 0 0 8px #00bfff, 0 0 20px #1e90ff; }
            50%  { box-shadow: 0 0 20px #87cefa, 0 0 40px #00bfff; }
            100% { box-shadow: 0 0 8px #00bfff, 0 0 20px #1e90ff; }
        }
        .streak-banner {
            animation: ice-pulse 1.6s ease-in-out infinite;
            background: linear-gradient(135deg, #0a2a6e 0%, #1565c0 50%, #82b1ff 100%);
            border-radius: 12px;
            padding: 14px 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 700;
            color: #e3f2fd;
            letter-spacing: 0.05em;
            text-shadow: 0 1px 4px rgba(0,0,0,0.5);
            margin-bottom: 8px;
        }
        """

    st.markdown(
        f"<style>{css}</style>"
        f'<div class="streak-banner">{emoji}  {label}  {emoji}</div>',
        unsafe_allow_html=True,
    )


st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.sidebar.divider()
st.sidebar.subheader("Past Games")
if st.session_state.get("score_history"):
    for record in reversed(st.session_state.score_history):
        icon = "✅" if record["outcome"] == "won" else "❌"
        st.sidebar.caption(
            f"{icon} Game {record['game']} · {record['difficulty']} · "
            f"Score: {record['score']} · Attempts: {record['attempts']}"
        )
else:
    st.sidebar.caption("No games played yet.")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "score_history" not in st.session_state:
    st.session_state.score_history = []

streak_length, streak_type = get_streak(st.session_state.score_history)
render_streak_banner(streak_length, streak_type)

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        message = HINT_MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.session_state.score_history = save_game_score(
                st.session_state.score_history,
                score=st.session_state.score,
                outcome="won",
                attempts=st.session_state.attempts,
                difficulty=difficulty,
            )
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.session_state.score_history = save_game_score(
                    st.session_state.score_history,
                    score=st.session_state.score,
                    outcome="lost",
                    attempts=st.session_state.attempts,
                    difficulty=difficulty,
                )
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
