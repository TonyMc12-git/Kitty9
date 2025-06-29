
import streamlit as st
import random

# Load and filter word list
@st.cache_data
def load_words():
    with open("wordlist.txt") as f:
        words = [word.strip().lower() for word in f if 4 <= len(word.strip()) <= 9]
    return words

def generate_letters(wordlist):
    nine_letter_words = [word for word in wordlist if len(word) == 9 and len(set(word)) == 9]
    if not nine_letter_words:
        raise ValueError("No suitable 9-letter words found.")
    base_word = random.choice(nine_letter_words)
    letters = list(base_word)
    random.shuffle(letters)
    return letters, base_word

def is_valid(word, letters, center, valid_words):
    if len(word) < 4 or center not in word or word not in valid_words:
        return False
    temp_letters = list(letters)
    try:
        for char in word:
            temp_letters.remove(char)
        return True
    except ValueError:
        return False

# Layout
st.title("Target Word Game")

if "letters" not in st.session_state:
    all_words = load_words()
    st.session_state.letters, st.session_state.solution_word = generate_letters(all_words)
    st.session_state.center = st.session_state.letters[4]
    st.session_state.valid_words = [
        word for word in all_words
        if is_valid(word, st.session_state.letters, st.session_state.center, all_words)
    ]
    st.session_state.found_words = []
    st.session_state.score = 0

# Letter grid display
st.markdown("### Letters")
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        index = i * 3 + j
        if index < 9:
            if index == 4:
                cols[j].button(f"{st.session_state.letters[index]}", disabled=True)
            else:
                cols[j].button(f"{st.session_state.letters[index]}")

# Word entry
st.markdown("### Enter a word:")
word_input = st.text_input("Type a word and press Enter", key="input")

if word_input:
    word = word_input.lower()
    if word in st.session_state.found_words:
        st.warning("Word already found.")
    elif word not in st.session_state.valid_words:
        st.error("Invalid word.")
    else:
        st.session_state.found_words.append(word)
        st.session_state.score += len(word)
        st.success(f"Nice! +{len(word)} points")

# Score display
st.markdown(f"**Score:** {st.session_state.score} / {sum(len(w) for w in st.session_state.valid_words)}")

# Debug / cheat display
with st.expander("Show all valid words (debug/cheat)"):
    all_words = sorted(st.session_state.valid_words, key=lambda w: (len(w), w))
    nine_letter = [w.upper() for w in all_words if len(w) == 9]
    other_words = [w for w in all_words if len(w) != 9]
    st.markdown("**Nine-letter words:**")
    for word in nine_letter:
        st.markdown(f"- {word}")
    st.markdown("**Other valid words:**")
    for word in other_words:
        st.markdown(f"- {word}")