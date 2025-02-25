import streamlit as st
from styles import page_setup,hide_navbar,unhide_nav_bar
import json
import sqlite3


st.markdown(unhide_nav_bar(), unsafe_allow_html=True)
# Display other content
st.write("# Welcome to HandSpeak! ✋🗣")
st.markdown(
    """
    <div class="section" style="background-color: #EAF2F8;">
        <h2 class="header">👐 About HandSpeak</h2>
        <p>HandSpeak is an innovative platform designed to bridge the communication gap 
        between the deaf community and non-sign language users. By leveraging AI-powered technology, 
        HandSpeak converts sign language into text and speech, making communication seamless and inclusive.</p>
    </div>

    <div class="section" style="background-color: #FEF5E7;">
        <h2 class="header">🎯 What's Inside?</h2>
        <ul>
            <li><span class="highlight">Learn Alphabets:</span> Understand and master individual sign language letters.</li>
            <li><span class="highlight">Learn Words:</span> Build vocabulary with commonly used sign language words.</li>
            <li><span class="highlight">Quiz Mode:</span> Challenge yourself and test your sign language knowledge.</li>
        </ul>
    </div>

    <div class="section" style="background-color: #EBF5FB;">
        <h2 class="header">🌟 Key Features</h2>
        <ul>
            <li>AI-powered sign recognition for accurate translations.</li>
            <li>Interactive learning modules with real-time feedback.</li>
            <li>Engaging quizzes to reinforce knowledge.</li>
            <li>Speech and text output for enhanced accessibility.</li>
            <li>Customizable language and voice settings.</li>
        </ul>
    </div>

    <div class="section" style="background-color: #FDEDEC;">
        <h2 class="header">📩 Contact Us</h2>
        <p>Have questions or feedback? We'd love to hear from you!</p>
    </div>
    """,
    unsafe_allow_html=True,
)
