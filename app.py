import streamlit as st
from streamlit_mic_recorder import mic_recorder
import whisper
from pydub import AudioSegment
import tempfile
import os

# Set page config
st.set_page_config(page_title="Speech to Text with Whisper", layout="centered")
st.title("🎙️ Speech to Text App (Mic + Upload)")
st.markdown("Convert your voice to text using OpenAI's Whisper model.")

# Load Whisper model once (cache for performance)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# --------------------------
# 🎤 Microphone Recording
# --------------------------
st.subheader("🎙️ Record from Microphone")

audio = mic_recorder(
    start_prompt="🎙️ Click to Start Recording",
    stop_prompt="🛑 Click to Stop Recording",
    key="recorder",
    use_container_width=True,
)

if audio:
    st.audio(audio["bytes"], format="audio/wav")
    # Save recorded bytes to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio["bytes"])
        tmp_path = tmp.name

    with st.spinner("Transcribing your voice..."):
        result = model.transcribe(tmp_path)
        st.success("✅ Transcription Complete")
        st.markdown("**📝 Transcribed Text:**")
        st.write(result["text"])

    os.remove(tmp_path)

# --------------------------
# 📤 Upload Audio File
# --------------------------
st.markdown("---")
st.subheader("📤 Or Upload an Audio File")

uploaded_audio = st.file_uploader(
    "Upload audio file (MP3, WAV, OGG, M4A)", type=["mp3", "wav", "ogg", "m4a"]
)

if uploaded_audio:
    st.audio(uploaded_audio)

    # Save uploaded audio to temp
    suffix = os.path.splitext(uploaded_audio.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_audio.read())
        tmp_path = tmp.name

    # Convert to WAV using pydub
    wav_path = tmp_path + ".wav"
    audio_segment = AudioSegment.from_file(tmp_path)
    audio_segment.export(wav_path, format="wav")

    with st.spinner("Transcribing uploaded audio..."):
        result = model.transcribe(wav_path)
        st.success("✅ Transcription Complete")
        st.markdown("**📝 Transcribed Text:**")
        st.write(result["text"])

    os.remove(tmp_path)
    os.remove(wav_path)
