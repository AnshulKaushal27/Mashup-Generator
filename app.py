import streamlit as st
from mashup import create_mashup
import os
import shutil

st.set_page_config(
    page_title="Songs Mashup Generator",
    page_icon="🎵",
    layout="centered"
)

# Spotify UI Styling
st.markdown("""
<style>
body { background-color: #000000; color: white; }
h1 { color: #1DB954; text-align: center; }
.stButton>button {
    background-color: #1DB954;
    color: black;
    border-radius: 30px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #1ed760;
}
</style>
""", unsafe_allow_html=True)

st.title("🎵 Songs Mashup Generator")

if "processing" not in st.session_state:
    st.session_state.processing = False

singer_name = st.text_input("🎤 Singer Name")
num_videos = st.slider("🎶 Number of Songs", 1, 5, 3)

length_option = st.radio(
    "🎧 Select Audio Length",
    ["Custom Duration", "Full Song"]
)

if length_option == "Custom Duration":
    duration = st.slider("⏱ Duration per Song (seconds)", 5, 60, 20)
else:
    duration = 0

output_filename = st.text_input("📁 Output File Name", "spotify_mashup")

if st.session_state.processing:
    st.warning("Mashup is currently generating... Please wait.")

if st.button("Generate Mashup 🎧") and not st.session_state.processing:

    if singer_name and output_filename:

        st.session_state.processing = True

        with st.spinner("Creating your mashup... 🎧"):
            mp3_file, zip_file, temp_dir = create_mashup(
                singer_name,
                num_videos,
                duration,
                output_filename
            )

        st.session_state.processing = False

        if mp3_file and os.path.exists(mp3_file):

            st.success("Mashup Created Successfully! 🎉")

            st.audio(mp3_file)

            with open(zip_file, "rb") as file:
                st.download_button(
                    label="Download ZIP 📦",
                    data=file,
                    file_name=os.path.basename(zip_file),
                    mime="application/zip"
                )

            # Clean temporary folder after use
            shutil.rmtree(temp_dir, ignore_errors=True)

        else:
            st.error("Something went wrong. Please try again.")

    else:
        st.warning("Please fill all fields.")
