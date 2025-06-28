# components/Voiceinput.py
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import os

def record_audio(duration=5, fs=44100):
    """Record audio and return temp filename"""
    st.info("🎙 Recording... Please speak.")
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_filename = temp_file.name
        temp_file.close()
        
        # Record audio
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wav.write(temp_filename, fs, audio)
        st.success("✅ Recording complete")
        return temp_filename
    except Exception as e:
        st.error(f"❌ Recording error: {e}")
        return None

def transcribe_audio(filename):
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "⚠️ Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"❌ Speech recognition service error: {e}"
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        # Clean up temporary file
        try:
            os.unlink(filename)
        except:
            pass

def voice_input_handler():
    """Handle voice input and return the transcription."""
    transcription = ""
    if st.button("🎤 Record Voice"):
        filename = record_audio()
        if filename:
            transcription = transcribe_audio(filename)
            st.markdown("**📝 Transcription Result:**")
            st.success(transcription)
    return transcription
