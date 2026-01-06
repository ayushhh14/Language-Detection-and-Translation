import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from langdetect import detect
import tempfile
import os

st.set_page_config(page_title="Voice Language Translator", layout="wide")
st.title("🎤 Voice & Text Language Translator")

translator = Translator()
recognizer = sr.Recognizer()

languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "German": "de",
    "French": "fr"
}

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = {lang: [] for lang in languages}

# ---------------- TEXT TRANSLATION ----------------
st.subheader("✍️ Text Translation")

text_input = st.text_area(
    "Enter text in any language:",
    height=120,
    placeholder="English / हिंदी / Español / Deutsch / Français"
)

text_target_lang = st.selectbox(
    "Translate text to:",
    languages.keys(),
    key="text_lang"
)

if st.button("🌐 Translate Text"):
    if text_input.strip():
        detected = detect(text_input)
        translated = translator.translate(
            text_input, dest=languages[text_target_lang]
        ).text

        st.success("Translation Successful")
        st.write(f"Detected Language: `{detected}`")
        st.write(translated)

        st.session_state.history[text_target_lang].append({
            "type": "Text",
            "input": text_input,
            "output": translated
        })
    else:
        st.warning("Please enter text")

# ---------------- VOICE TRANSLATION ----------------
st.divider()
st.subheader("🎙️ Record Speech Directly")

audio_data = st.audio_input("Click to record and stop when finished")

voice_target_lang = st.selectbox(
    "Translate speech to:",
    languages.keys(),
    key="voice_lang"
)

if audio_data is not None and st.button("🎧 Translate Speech"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data.getbuffer())
        audio_path = tmp.name

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        speech_text = recognizer.recognize_google(audio)

    detected_audio = detect(speech_text)
    translated_audio = translator.translate(
        speech_text, dest=languages[voice_target_lang]
    ).text

    st.success("Speech Translation Successful")
    st.write("Recognized Speech:")
    st.write(speech_text)
    st.write(f"Detected Language: `{detected_audio}`")
    st.write("Translated Text:")
    st.write(translated_audio)

    st.session_state.history[voice_target_lang].append({
        "type": "Speech",
        "input": speech_text,
        "output": translated_audio
    })

    os.remove(audio_path)

# ---------------- HISTORY ----------------
st.divider()
st.subheader("📜 Translation History")

history_lang = st.selectbox(
    "View history for language:",
    languages.keys(),
    key="history_lang"
)

if st.session_state.history[history_lang]:
    for i, item in enumerate(
        reversed(st.session_state.history[history_lang]), 1
    ):
        with st.expander(f"{item['type']} Entry {i}"):
            st.write("Input:")
            st.write(item["input"])
            st.write("Output:")
            st.write(item["output"])
else:
    st.info("No history available yet.")
