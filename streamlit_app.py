import streamlit as st import random import itertools import re

Full English word list (cleaned up from available source)

@st.cache_data def load_word_list(): with open("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt") as f: words = set(line.strip().lower() for line in f if len(line.strip()) >= 4 and line.strip().isalpha()) return words

@st.cache_data def get_valid_nine_letter_word(word_list): nine_letter_words = [w for w in word_list if len(w) == 9 and len(set(w)) == 9] while nine_letter_words: word = random.choice(nine_letter_words) return word return None

def is_valid_word(word, center_letter, available_letters, word_list): if len(word) < 4: return False if center_letter not in word: return False if not all(char in available_letters for char in word): return False if word.endswith('s') and not word.endswith('ss') and not word.endswith('es'): stem = word[:-1] if stem in word_list: return False return word in word_list

@st.cache_data def generate_puzzle(word_list): base_word = get_valid_nine_letter_word(word_list) letters = list(base_word) random.shuffle(letters) center_letter = letters[4] valid_words = set() for l in range(4, 10): for combo in itertools.permutations(letters, l): candidate = ''.join(combo) if is_valid_word(candidate, center_letter, letters, word_list): valid_words.add(candidate) return letters, center_letter, sorted(valid_words)

--- Streamlit App Logic ---

st.set_page_config(page_title="Target Word Puzzle", layout="centered") st.title("🧠 Target Word Puzzle")

if 'game_started' not in st.session_state: st.session_state.game_started = False if 'found_words' not in st.session_state: st.session_state.found_words = set()

word_list = load_word_list()

if not st.session_state.game_started: if st.button("Start New Game"): letters, center_letter, all_valid_words = generate_puzzle(word_list) st.session_state.letters = letters st.session_state.center_letter = center_letter st.session_state.all_valid_words = all_valid_words st.session_state.total = len(all_valid_words) st.session_state.game_started = True st.rerun() else: letters = st.session_state.letters center_letter = st.session_state.center_letter all_valid_words = st.session_state.all_valid_words found_words = st.session_state.found_words total = st.session_state.total

st.subheader("Letters")
cols = st.columns(3)
for i, letter in enumerate(letters):
    style = "font-weight: bold; background-color: #ffe066; padding: 10px; border-radius: 50%;" if letter == center_letter else ""
    cols[i % 3].markdown(f"<div style='text-align: center; font-size: 24px; {style}'>{letter.upper()}</div>", unsafe_allow_html=True)

st.markdown(f"**Center Letter: {center_letter.upper()}**")
st.markdown(f"Total possible words: **{total}**")

new_word = st.text_input("Enter a word:", "").lower().strip()
if st.button("Submit"):
    if new_word in all_valid_words and new_word not in found_words:
        found_words.add(new_word)
        st.success(f"✅ Great! {new_word.upper()} is correct.")
    elif new_word in found_words:
        st.warning("You've already found that word!")
    else:
        st.error("❌ Not a valid word.")

score = len(found_words)
percent = score / total if total else 0
st.markdown(f"### You’ve found {score} words.")

if percent >= 1.0:
    st.balloons()
    st.success("🎉 PERFECT! You've found all the words!")
elif percent >= 0.6:
    st.success("🌟 Excellent!")
elif percent >= 0.3:
    st.info("🙂 Good start!")

st.markdown("---")
st.markdown("### Words You've Found:")
st.write(', '.join(sorted(found_words)))

if st.button("Restart Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

