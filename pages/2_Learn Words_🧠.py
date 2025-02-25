import cv2
import streamlit as st
import time
import sqlite3
from model_utils import prediction_model
from components import progress_bar, update_video, detected_word
from styles import page_setup, page_with_webcam_video

# Initialize page state and camera
if "page" not in st.session_state or st.session_state["page"] != "wordpage":
    cv2.destroyAllWindows()
    st.session_state["page"] = "wordpage"
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)

# Database connection (if used)
conn = sqlite3.connect("signlingo.db")
c = conn.cursor()

st.markdown(page_setup(), unsafe_allow_html=True)
st.markdown(page_with_webcam_video(), unsafe_allow_html=True)

if "word" not in st.session_state:
    st.session_state["word"] = 0
    st.session_state["index"] = 0

WORD_LIST = [
    "CODE", "DATA", "LEARN", "TEST", "IDEA",
    "PYTHON", "HAPPY", "SMART", "QUICK", "BRAIN",
]
NUM_WORD = len(WORD_LIST)

col1, col2 = st.columns([0.5, 0.5])
with col1:
    video_placeholder = st.empty()
    video_placeholder.markdown(
        update_video(WORD_LIST[st.session_state["word"]][st.session_state["index"]]),
        unsafe_allow_html=True,
    )
    matched_placeholder = st.empty()
with col2:
    webcam_placeholder = st.empty()
    progress_bar_placeholder = st.empty()

while True and st.session_state["page"] == "wordpage":
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
    else:
        st.write("Loading...")
        ret = False
    if ret:
        current_word = WORD_LIST[st.session_state["word"]]
        letter = current_word[st.session_state["index"]]
        frame, prob = prediction_model(frame, letter)
        webcam_placeholder.image(frame, channels="BGR")
        matched_placeholder.markdown(
            detected_word(current_word, st.session_state["index"] - 1),
            unsafe_allow_html=True,
        )
        progress_bar_placeholder.markdown(progress_bar(prob), unsafe_allow_html=True)
        if prob == 100:
            st.session_state["index"] += 1
            if st.session_state["index"] == len(current_word):
                try:
                    c.execute(
                        """INSERT INTO Words (username, word) VALUES (?, ?)""",
                        ("demo", current_word),
                    )
                    conn.commit()
                except Exception as e:
                    print(e)
                st.session_state["index"] = 0
                st.session_state["word"] = (st.session_state["word"] + 1) % NUM_WORD
                st.balloons()
                time.sleep(2)
            video_placeholder.empty()
            time.sleep(2)
            matched_placeholder.empty()
            video_placeholder.markdown(
                update_video(WORD_LIST[st.session_state["word"]][st.session_state["index"]]),
                unsafe_allow_html=True,
            )
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
conn.close()
