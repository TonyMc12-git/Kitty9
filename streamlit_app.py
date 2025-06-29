import streamlit as st
import random

# Load word list (ensure this file is uploaded alongside your app)
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
    while True:
        letters = random.sample("abcdefghijklmnopqrstuvwxyz", 9)
        center_letter = letters[4]
        yield letters, center_letter

def find_valid_words(letters, center_letter):
    return sorted([
        word for word in WORD_LIST
        if len(word) >= 4
        and center_letter in word
        and set(word).issubset(set(letters))
    ])

# App
st.title("🧠 Target Word Puzzle")

if "game_letters" not in st.session_state:
    gen = generate_letters()
    st.session_state.game_letters, st.session_state.center_letter = next(gen)
    st.session_state.valid_words = find_valid_words(
        st.session_state.game_letters, st.session_state.center_letter
    )
    st.session_state.found_words = set()

letters = st.session_state.game_letters
center = st.session_state.center_letter
valid_words = st.session_state.valid_words
found_words = st.session_state.found_words

# Display 3x3 grid
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

# Game info
st.write(f"**Center Letter:** {center.upper()}")
st.write(f"**Total possible words:** {len(valid_words)}")
if len(valid_words) >= 10:
    st.write(f"⭐ To be Good: {len(valid_words) // 3} words — To be Excellent: {2 * len(valid_words) // 3} words")

# Word input
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

# Found words display
st.markdown(f"### You've found {len(found_words)} word{'s' if len(found_words)!=1 else ''}:")
st.write(", ".join(sorted(found_words)))

# Reset option
if st.button("🔄 New Puzzle"):
    gen = generate_letters()
    st.session_state.game_letters, st.session_state.center_letter = next(gen)
    st.session_state.valid_words = find_valid_words(
        st.session_state.game_letters, st.session_state.center_letter
    )
    st.session_state.found_words = set()
    st.experimental_rerun()