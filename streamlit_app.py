import streamlit as st
import random

# Load the uploaded word list
with open("filtered_scrabble_words.txt", "r") as f:
    WORD_LIST = set(word.strip().lower() for word in f)

def is_valid_word(word, center_letter, letters):
    if len(word) < 4:
        return "too_short"
    if center_letter not in word:
        return "missing_center"
    if not set(word).issubset(set(letters)):
        return "invalid_letters"
    if word.lower() not in WORD_LIST:
        return "not_in_list"
    return "valid"

def generate_letters():
    nine_letter_words = [w for w in WORD_LIST if len(w) == 9]
    while True:
        word = random.choice(nine_letter_words)
        letters = list(set(word))
        if len(letters) == 9:
            center_letter = random.choice(letters)
            return letters, center_letter

def find_valid_words(letters, center_letter):
    return sorted([
        word for word in WORD_LIST
        if len(word) >= 4 and
        center_letter in word and
        set(word).issubset(set(letters))
    ])

# Initialize session
if "game_letters" not in st.session_state:
    letters, center = generate_letters()
    st.session_state.game_letters = letters
    st.session_state.center_letter = center
    st.session_state.valid_words = find_valid_words(letters, center)
    st.session_state.found_words = set()

letters = st.session_state.game_letters
center = st.session_state.center_letter
valid_words = st.session_state.valid_words
found_words = st.session_state.found_words

# UI
st.title("🎯 Target Word Puzzle")

# Display 3x3 letter grid
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

# Info
st.write(f"**Center Letter:** {center.upper()}")
st.write(f"**Total possible words:** {len(valid_words)}")
if len(valid_words) >= 10:
    st.write(f"⭐ To be Good: {len(valid_words) // 3} — To be Excellent: {2 * len(valid_words) // 3}")

# Word entry
guess = st.text_input("Enter a word:")
if st.button("Submit"):
    result = is_valid_word(guess.lower(), center, letters)
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
        st.error("❌ You can only use the given letters.")
    elif result == "not_in_list":
        st.error("❌ Not a valid word.")

# Found words
st.markdown(f"### ✅ You've found {len(found_words)} word{'s' if len(found_words)!=1 else ''}:")
st.write(", ".join(sorted(found_words)))

# Reveal all valid words (cheat/debug mode)
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
    st.session_state.valid_words = find_valid_words(letters, center)
    st.session_state.found_words = set()
    st.experimental_rerun()