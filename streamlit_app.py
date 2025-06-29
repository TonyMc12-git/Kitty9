import streamlit as st
import random
from collections import Counter

# Load the uploaded word list
with open("filtered_scrabble_words.txt", "r") as f:
    WORD_LIST = set(word.strip().lower() for word in f)

def is_valid_word(word, center_letter, puzzle_counter):
    word = word.lower()
    if len(word) < 4:
        return "too_short"
    if center_letter not in word:
        return "missing_center"
    if word not in WORD_LIST:
        return "not_in_list"

    word_counter = Counter(word)
    for letter in word_counter:
        if word_counter[letter] > puzzle_counter.get(letter, 0):
            return "invalid_letters"
    return "valid"

def generate_letters():
    nine_letter_words = [w for w in WORD_LIST if len(w) == 9 and len(set(w)) <= 9]
    while True:
        word = random.choice(nine_letter_words)
        letters = list(word)
        center_letter = random.choice(letters)
        puzzle_counter = Counter(letters)
        return letters, center_letter, puzzle_counter

def find_valid_words(puzzle_letters, center_letter, puzzle_counter):
    valid = []
    for word in WORD_LIST:
        if len(word) >= 4 and center_letter in word:
            wc = Counter(word)
            if all(wc[char] <= puzzle_counter.get(char, 0) for char in wc):
                valid.append(word)
    return valid

# Initialize game session
if "game_letters" not in st.session_state:
    letters, center = generate_letters()
    st.session_state.game_letters = letters
    st.session_state.center_letter = center
    st.session_state.puzzle_counter = Counter(letters)
    st.session_state.valid_words = find_valid_words(letters, center, st.session_state.puzzle_counter)
    st.session_state.found_words = set()

letters = st.session_state.game_letters
center = st.session_state.center_letter
puzzle_counter = st.session_state.puzzle_counter
valid_words = st.session_state.valid_words
found_words = st.session_state.found_words

# UI
st.title("🎯 Target Word Puzzle")

# Display the 3x3 grid
st.markdown("### Letters Grid")
grid_html = "<div style='display: grid; grid-template-columns: repeat(3, 50px); gap: 10px; justify-content: center;'>"
for i, letter in enumerate(letters):
    style = (
        "background-color: #ffeb3b; font-weight: bold;"
        if letter == center else "background-color: #e0e0e0;"
    )
    grid_html += f"<div style='text-align: center; padding: 10px; border-radius: 5px; {style}'>{letter.upper()}</div>"
grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

# Word input
st.write(f"**Center Letter:** {center.upper()}")
st.write(f"**Total possible words:** {len(valid_words)}")
if len(valid_words) >= 10:
    st.write(f"⭐ To be Good: {len(valid_words) // 3} — To be Excellent: {2 * len(valid_words) // 3}")

guess = st.text_input("Enter a word:")
if st.button("Submit"):
    result = is_valid_word(guess, center, puzzle_counter)
    if result == "valid":
        if guess.lower() in found_words:
            st.warning("You've already found that word.")
        else:
            found_words.add(guess.lower())
            st.success("✅ Great word!")
    elif result == "too_short":
        st.error("❌ Must be at least 4 letters.")
    elif result == "missing_center":
        st.error(f"❌ Word must include the center letter: '{center.upper()}'.")
    elif result == "invalid_letters":
        st.error("❌ You've used letters too many times.")
    elif result == "not_in_list":
        st.error("❌ Not a valid word.")

# Found words display
st.markdown(f"### ✅ You've found {len(found_words)} word{'s' if len(found_words)!=1 else ''}:")
st.write(", ".join(sorted(found_words)))

# Debug / cheat mode
if st.checkbox("🔍 Show all valid words (cheat/debug)", value=False):
    nine_letter_words = [w.upper() for w in valid_words if len(w) == 9]
    other_words = sorted([w for w in valid_words if len(w) < 9])

    st.markdown("### 🧠 9-letter word(s):")
    if nine_letter_words:
        st.write(", ".join(nine_letter_words))
    else:
        st.write("None")

    st.markdown("### 🔤 Other valid words:")
    st.write(", ".join(other_words))

# Reset
if st.button("🔄 New Puzzle"):
    letters, center = generate_letters()
    st.session_state.game_letters = letters
    st.session_state.center_letter = center
    st.session_state.puzzle_counter = Counter(letters)
    st.session_state.valid_words = find_valid_words(letters, center, st.session_state.puzzle_counter)
    st.session_state.found_words = set()
    st.experimental_rerun()