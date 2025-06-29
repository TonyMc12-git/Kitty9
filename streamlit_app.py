import streamlit as st
import random
import string

# Load word list
@st.cache_data
def load_words():
    with open("wordlist.txt") as f:
        words = set(word.strip().lower() for word in f if 4 <= len(word.strip()) <= 9)
    return words

# Check if word is plural (simple 's' rule, but allows verbs like 'plays')
def is_plural(word):
    if word.endswith("s") and not word.endswith("ss"):
        base = word[:-1]
        return base in words and not word in allowed_verbs
    return False

# Filter word list with rules
def get_valid_words(letters, center):
    valid = []
    letter_counts = {char: letters.count(char) for char in letters}
    for word in words:
        if center not in word:
            continue
        word_counts = {char: word.count(char) for char in word}
        if any(word_counts[char] > letter_counts.get(char, 0) for char in word_counts):
            continue
        if is_plural(word):
            continue
        valid.append(word)
    return sorted(valid, key=lambda w: (len(w), w))

# Generate a puzzle with at least one 9-letter word
def generate_letters():
    nine_letter_words = [w for w in words if len(w) == 9]
    base_word = random.choice(nine_letter_words)
    letters = list(base_word)
    random.shuffle(letters)
    center = letters[4]
    return letters, center, base_word

# Load data
words = load_words()
allowed_verbs = {w for w in words if w.endswith("s")}  # crude verb whitelist

# State
if "letters" not in st.session_state:
    st.session_state.letters, st.session_state.center, st.session_state.solution_word = generate_letters()
if "found" not in st.session_state:
    st.session_state.found = []

letters = st.session_state.letters
center = st.session_state.center
solution = st.session_state.solution_word
valid_words = get_valid_words(letters, center)

# Header
st.title("Word Puzzle")
st.write("Make words using the letters below. Each word must include the **center letter** and be at least 4 letters long. No proper nouns, plurals, or slang.")

# Grid
st.markdown("### Letters")
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if i == 4:
            st.button(letters[i].upper(), disabled=True, key=f"center_{i}")
        else:
            st.button(letters[i].upper(), disabled=True, key=f"letter_{i}")

# Input
guess = st.text_input("Enter a word:").lower().strip()

if guess:
    if len(guess) < 4:
        st.error("Word must be at least 4 letters long.")
    elif center not in guess:
        st.error(f"Word must include the center letter '{center.upper()}'.")
    elif any(guess.count(c) > letters.count(c) for c in guess):
        st.error("You can only use each letter once.")
    elif guess not in valid_words:
        st.error("Not a valid word.")
    elif guess in st.session_state.found:
        st.warning("Already found.")
    else:
        st.session_state.found.append(guess)
        st.success("Nice!")

# Score
score = len(st.session_state.found)
total = len(valid_words)
good = int(total * 0.3)
excellent = int(total * 0.7)

st.markdown(f"**Score**: {score} / {total}")
st.markdown(f"*Good*: {good} &nbsp;&nbsp;|&nbsp;&nbsp; *Excellent*: {excellent}")

# Celebrations
if score >= excellent:
    st.balloons()
elif score >= good:
    st.success("You're doing great!")

# Words found
with st.expander("Words you’ve found"):
    st.write(", ".join(sorted(st.session_state.found)))

# Debug / Cheat (for dev only)
st.markdown("---")
st.markdown("### Debug (valid words)")
st.markdown(f"**9-letter word:** `{solution.upper()}`")
st.markdown("**All valid words:**")
st.text(", ".join(valid_words))

# Reset
if st.button("New Puzzle"):
    st.session_state.letters, st.session_state.center, st.session_state.solution_word = generate_letters()
    st.session_state.found = []
    st.experimental_rerun()