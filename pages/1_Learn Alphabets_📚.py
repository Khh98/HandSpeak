import streamlit as st
import cv2
import time
import sqlite3
import datetime
from model_utils import prediction_model
from components import progress_bar, update_video
from styles import page_setup, page_with_webcam_video  # Import your functions

print(datetime.datetime.now())

if "page" not in st.session_state or st.session_state["page"] != "learnpage":
    cv2.destroyAllWindows()
    st.session_state["page"] = "learnpage"
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)

# ✅ Database Connection
conn = sqlite3.connect("signlingo.db")
c = conn.cursor()

# ✅ Remove `current_user` since there's no login system
current_user = None  # ❌ No longer needed

# ✅ Apply Page Styling
st.markdown(page_setup(), unsafe_allow_html=True)
st.markdown(page_with_webcam_video(), unsafe_allow_html=True)

if "alphabet" not in st.session_state:
    st.session_state["alphabet"] = 0

# ✅ Alphabet List
ALPHABET_LIST = {
    0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
    8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O",
    15: "P", 16: "R", 17: "S", 18: "T", 19: "U", 20: "V", 21: "W",
    22: "X", 23: "Y",
}
NUM_ALPHABETS = len(ALPHABET_LIST)

# ✅ Layout for Video & Progress
col1, col2 = st.columns([0.5, 0.5])
with col1:
    video_placeholder = st.empty()  # To display video
    video_placeholder.markdown(
        update_video(ALPHABET_LIST[st.session_state["alphabet"]]),
        unsafe_allow_html=True,
    )
with col2:
    webcam_placeholder = st.empty()  # To display webcam

matched_placeholder = st.empty()

# ✅ Creating the Progress Bar
prob = 0
progress_bar_placeholder = st.empty()

# ✅ Webcam Capture & Processing Loop
while True and st.session_state.page == "learnpage":
    if cap is not None or cap.isOpened():
        ret, frame = cap.read()
    else:
        st.write("Loading...")

    if ret:
        character = ALPHABET_LIST[st.session_state["alphabet"]]
        frame, prob = prediction_model(frame, character)

        webcam_placeholder.image(frame, channels="BGR")

        progress_bar_placeholder.markdown(
            progress_bar(prob),
            unsafe_allow_html=True,
        )

        if prob == 100:
            st.balloons()
            video_placeholder.empty()

            try:
                # ✅ Fixed Query (Remove `username`)
                c.execute(
                    """INSERT INTO Alphabet (letter) VALUES (?)""",
                    (character,),
                )
                conn.commit()
            except Exception as e:
                print(e)

            st.session_state["alphabet"] = (st.session_state["alphabet"] + 1) % NUM_ALPHABETS

            time.sleep(2)

            video_placeholder.markdown(
                update_video(ALPHABET_LIST[st.session_state["alphabet"]]),
                unsafe_allow_html=True,
            )

cap.release()
cv2.destroyAllWindows()
conn.close()
