import streamlit as st
from google.cloud import speech, translate_v2 as translate, texttospeech
import os
import tempfile

# Function to recognize speech using Google Cloud Speech-to-Text API
def recognize_speech(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, "rb") as audio:
        content = audio.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Function to translate text using Google Cloud Translation API
def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

# Function to synthesize speech using Google Cloud Text-to-Speech API
def synthesize_speech(text, target_language):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=target_language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

# Streamlit interface
st.title("Speech-to-Speech Translation App")

# Audio input
audio_file = st.file_uploader("Upload an audio file", type=["wav"])

if audio_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(audio_file.getvalue())
        temp_file_path = temp_file.name

    # Recognize speech
    recognized_text = recognize_speech(temp_file_path)
    st.write("Recognized Text: ", recognized_text)

    # Select target language
    target_language = st.selectbox("Select target language", ["es", "fr", "de", "zh"])

    # Translate text
    translated_text = translate_text(recognized_text, target_language)
    st.write("Translated Text: ", translated_text)

    # Synthesize speech
    synthesized_speech = synthesize_speech(translated_text, target_language)

    # Save synthesized speech temporarily
    synthesized_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    synthesized_file.write(synthesized_speech)
    synthesized_file_path = synthesized_file.name

    # Play synthesized speech
    st.audio(synthesized_file_path, format="audio/mp3")
