import cv2
import streamlit as st
import time
import sqlite3
from model_utils import prediction_model
from components import progress_bar, update_video, detected_word
from styles import page_setup, page_with_webcam_video

# ✅ Ensure session state variables are initialized
if "page" not in st.session_state or st.session_state["page"] != "wordpage":
    # ✅ Properly handle camera reinitialization when switching pages
    if "cap" in st.session_state:
        st.session_state["cap"].release()
        del st.session_state["cap"]
    
    cv2.destroyAllWindows()
    st.session_state["page"] = "wordpage"

# ✅ Always Initialize VideoCapture in session state
if "cap" not in st.session_state:
    st.session_state["cap"] = cv2.VideoCapture(cv2.CAP_DSHOW)

# ✅ Now use `st.session_state["cap"]` instead of `cap`
cap = st.session_state["cap"]

# ✅ Database Connection
conn = sqlite3.connect("signlingo.db")
c = conn.cursor()

# ✅ Apply Page Styling
st.markdown(page_setup(), unsafe_allow_html=True)
st.markdown(page_with_webcam_video(), unsafe_allow_html=True)

if "word" not in st.session_state:
    st.session_state["word"] = 0
    st.session_state["index"] = 0

# ✅ Word List for Learning
WORD_LIST = [
    "CODE", "DATA", "LEARN", "TEST", "IDEA",
    "PYTHON", "HAPPY", "SMART", "QUICK", "BRAIN",
]
NUM_WORD = len(WORD_LIST)

# ✅ Layout for Video & Progress
col1, col2 = st.columns([0.5, 0.5], gap="medium")
with col1:
    video_placeholder = st.empty()  # To display video
    video_placeholder.markdown(
        update_video(WORD_LIST[st.session_state["word"]][st.session_state["index"]]),
        unsafe_allow_html=True,
    )
    matched_placeholder = st.empty()
with col2:
    webcam_placeholder = st.empty()  # To display webcam
    progress_bar_placeholder = st.empty()

# ✅ Webcam Capture & Processing Loop
while True and st.session_state["page"] == "wordpage":
    if "cap" in st.session_state and st.session_state["cap"].isOpened():
        ret, frame = st.session_state["cap"].read()
    else:
        st.write("Loading...")

    if ret:
        current_word_index = st.session_state["word"]

        frame, prob = prediction_model(
            frame, WORD_LIST[st.session_state["word"]][st.session_state["index"]]
        )

        webcam_placeholder.image(frame, channels="BGR")

        matched_placeholder.markdown(
            detected_word(WORD_LIST[current_word_index], st.session_state["index"] - 1),
            unsafe_allow_html=True,
        )

        progress_bar_placeholder.markdown(progress_bar(prob), unsafe_allow_html=True)

        if prob == 100:
            st.session_state["index"] += 1

            if st.session_state["index"] == len(WORD_LIST[st.session_state["word"]]):
                matched_placeholder.markdown(
                    detected_word(
                        WORD_LIST[current_word_index], st.session_state["index"] - 1
                    ),
                    unsafe_allow_html=True,
                )

                try:
                    # ✅ Fixed Query (Removed `username`)
                    c.execute(
                        """INSERT INTO Words (word) VALUES (?)""",
                        (WORD_LIST[st.session_state["word"]],),
                    )
                    conn.commit()
                except Exception as e:
                    print(e)

                st.session_state["index"] = 0
                st.session_state["word"] = (st.session_state["word"] + 1) % NUM_WORD
                st.balloons()

            video_placeholder.empty()

            time.sleep(2)
            matched_placeholder.empty()
            video_placeholder.markdown(
                update_video(WORD_LIST[st.session_state["word"]][st.session_state["index"]]),
                unsafe_allow_html=True,
            )

# ✅ Do not release the camera on every page switch; only release when the app closes
if "cap" in st.session_state:
    st.session_state["cap"].release()
    del st.session_state["cap"]

cv2.destroyAllWindows()
conn.close()
