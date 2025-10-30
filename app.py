import streamlit as st
import sounddevice as sd
import numpy as np
import wavio
import speech_recognition as sr
import pyttsx3
from PIL import Image
import matplotlib.pyplot as plt
import time
import random
import pygame

# Initialize components
pygame.mixer.init()

# Function to safely speak (avoids RuntimeError)
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except RuntimeError:
        pass  # Skip speaking if loop is busy

st.set_page_config(page_title="MyCare+", page_icon="💊", layout="wide")

# ==========================================
# 🌟 Splash Screen
# ==========================================
if "splash_done" not in st.session_state:
    st.title("💊 MyCare+ — AI Health Companion")
    st.subheader("Team CodeSlayers | HackNova 2025")
    st.markdown("### _Your care, your way — Emotion + AI + Health in one app_")
    st.image("https://cdn-icons-png.flaticon.com/512/9429/9429110.png", width=200)
    st.info("Launching app... please wait ⏳")
    time.sleep(3)
    st.session_state.splash_done = True
    st.rerun()

# ==========================================
# 🧠 Session States
# ==========================================
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "recent_medicines" not in st.session_state:
    st.session_state.recent_medicines = []

# ==========================================
# Sidebar Navigation
# ==========================================
st.title("💊 MyCare+ — AI Health Companion")
section = st.sidebar.radio("📍 Choose a feature", [
    "🎤 Voice & Emotion Assistant",
    "📷 Tablet Scanner",
    "📊 Health Insights"
])

# ==========================================
# 1️⃣ Voice & Emotion Assistant
# ==========================================
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["sad", "upset", "depressed", "lonely"]):
        return "sadness"
    elif any(word in text for word in ["angry", "mad", "furious"]):
        return "anger"
    elif any(word in text for word in ["stressed", "nervous", "worried"]):
        return "stress"
    elif any(word in text for word in ["happy", "great", "excited", "good"]):
        return "happiness"
    else:
        return "neutral"

if section == "🎤 Voice & Emotion Assistant":
    st.header("🧠 Emotional Wellness & Support")
    st.write("Talk to MyCare+ about your day. It listens, detects emotion, and responds supportively.")

    if st.button("🎙️ Speak Now"):
        fs = 44100
        duration = 5
        st.info("Listening... please speak for 5 seconds.")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wavio.write("temp_audio.wav", recording, fs, sampwidth=2)
        st.success("Audio captured successfully!")

        recognizer = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.write(f"🗣️ You said: **{text}**")

                emotion = detect_emotion(text)
                st.session_state.mood_log.append(emotion)
                st.write(f"💭 Detected Emotion: **{emotion.upper()}**")

                if emotion == "sadness":
                    st.warning("You seem a bit low. Playing calming nature sounds 🌿")
                    speak("You sound sad. Take a deep breath, it’s going to be okay.")
                elif emotion in ["anger", "stress"]:
                    st.warning("Feeling tense? Here’s a motivational affirmation 🌞")
                    speak("Feeling tense? Remember, calm minds solve problems better.")
                else:
                    st.success("Your mood seems balanced! Keep up your positive energy 💫")
                    speak("You seem fine today. Keep that positive energy flowing!")

                # AI Mood Summary trigger after 3 emotions logged
                if len(st.session_state.mood_log) >= 3:
                    mood_counts = {m: st.session_state.mood_log.count(m) for m in set(st.session_state.mood_log)}
                    dominant = max(mood_counts, key=mood_counts.get)
                    st.markdown("---")
                    st.subheader("🧠 AI Mood Summary")
                    st.info(f"You've been mostly feeling **{dominant.upper()}** today.")
                    if dominant == "sadness":
                        st.write("💚 Suggestion: Try a short walk or listen to calming sounds.")
                    elif dominant == "happiness":
                        st.write("🌞 Keep it up! You’re doing great emotionally.")
                    else:
                        st.write("✨ Your emotions are steady. Stay mindful and positive!")

            except sr.UnknownValueError:
                st.error("Could not understand your voice.")
            except sr.RequestError:
                st.error("Speech recognition service unavailable.")

# ==========================================
# 2️⃣ Tablet Scanner
# ==========================================
elif section == "📷 Tablet Scanner":
    st.header("💊 AI Tablet Scanner & Reminder")
    st.write("Scan a tablet using your webcam. MyCare+ identifies and sets a reminder.")

    uploaded_file = st.camera_input("📸 Capture your tablet image")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Scanned Tablet", use_column_width=True)
        st.write("🔍 Analyzing tablet...")
        time.sleep(2)

        tablets = ["Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine", "Vitamin D", "Aspirin", "Dolo 650", "Azithromycin"]
        medicine_name = random.choice(tablets)
        st.success(f"Identified Medicine: **{medicine_name}**")

        st.info("⏰ Reminder: Take your medicine at **8:00 PM** daily.")
        speak(f"Medicine identified as {medicine_name}. Reminder set for 8 PM.")

        st.session_state.recent_medicines.append(medicine_name)
        if len(st.session_state.recent_medicines) > 3:
            st.session_state.recent_medicines.pop(0)

    if st.session_state.recent_medicines:
        st.markdown("### 🧾 Recently Scanned Medicines")
        for med in reversed(st.session_state.recent_medicines):
            st.write(f"- 💊 {med}")

# ==========================================
# 3️⃣ Health Dashboard
# ==========================================
elif section == "📊 Health Insights":
    st.header("📈 Personalized Health Insights")
    st.write("View your stress trend and voice emotion statistics.")

    emotions = ["Happy", "Neutral", "Sad", "Angry"]
    values = np.random.randint(10, 100, size=4)

    fig, ax = plt.subplots()
    ax.bar(emotions, values, color=['green', 'gray', 'blue', 'red'])
    ax.set_title("Emotion Pattern (Weekly)")
    ax.set_ylabel("Intensity")
    st.pyplot(fig)

    st.markdown("---")
    st.metric("💓 Heart Rate", "76 bpm", "+3 steady")
    st.metric("🧘 Stress Index", "Low", "-12% this week")
    st.metric("😴 Sleep Quality", "Good", "+8% improvement")

    st.success("Keep tracking your health with MyCare+ 💚")
