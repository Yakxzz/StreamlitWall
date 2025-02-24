import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import os
import platform

# Set page config for mobile-sized window
st.set_page_config(page_title="Wallpapers by Yaksh", layout="centered", initial_sidebar_state="expanded")

# CSS for mobile size, no zoom, and centered window
st.markdown("""
    <style>
        .main {
            max-width: 360px;
            margin: auto;
        }
        img {
            object-fit: cover;
        }
        .stApp {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("Wallpapers by Yaksh")

# Predefined wallpapers
wallpapers = [
    {"name": "Black Headphone", "url": "https://wallpaper.forfun.com/fetch/b1/b10c2b22fc83644699ec4822d102da6b.jpeg?h=900&r=0.5", "tags": ["Aesthetic Music", "Music", "Aesthetic"]},
    {"name": "Glass Guitar", "url": "https://wallpaper.forfun.com/fetch/0e/0ec93d50b4a57269969034140b8fdbde.jpeg?h=900&r=0.5", "tags": ["guitar", "glass"]},
    {"name": "Moon Art", "url": "https://wallpaper.forfun.com/fetch/f6/f639851874060b429f9049beb1cc6149.jpeg?h=900&r=0.5", "tags": ["aesthetic moon", "moon"]},
    {"name": "Flight Art", "url": "https://wallpaper.forfun.com/fetch/5e/5e7a7bf446d1af63d6f94808f5b38374.jpeg?h=900&r=0.5", "tags": ["Flight", "Aeroplane", "Aesthetic", "Colour Art"]},
    {"name": "Moon View", "url": "https://wallpaper.forfun.com/fetch/55/55a75bd94ac9b2cf880285e04f5a4b27.jpeg?h=900&r=0.5", "tags": ["Moon", "Sunset", "Aesthetic Moon", "Aesthetic"]},
    {"name": "Cloud House", "url": "https://wallpaper.forfun.com/fetch/5d/5d3fc070d749acfeb8c707d4460653f5.jpeg?h=900&r=0.5", "tags": ["House", "Sunset House", "Aesthetic House", "Clouds"]}
]

# State management for buttons
if 'downloaded' not in st.session_state:
    st.session_state.downloaded = {}
if 'applied' not in st.session_state:
    st.session_state.applied = {}

# Search bar
search_query = st.text_input("Search Wallpapers", "")

# Filter wallpapers based on search
filtered_wallpapers = [wp for wp in wallpapers if search_query.lower() in wp["name"].lower() or any(search_query.lower() in tag.lower() for tag in wp["tags"])]

# Display wallpapers
if filtered_wallpapers:
    for wp in filtered_wallpapers:
        st.subheader(wp["name"])
        try:
            response = requests.get(wp["url"])
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=wp["name"], use_container_width=True)

            # Open detailed view
            if st.button(f"View {wp['name']}", key=f"view_{wp['name']}"):
                st.session_state.selected_wallpaper = wp
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Error loading image: {e}")
else:
    st.warning("No wallpapers found. Try another search.")

# Detailed wallpaper view
if 'selected_wallpaper' in st.session_state:
    wp = st.session_state.selected_wallpaper
    st.header(wp["name"])
    response = requests.get(wp["url"])
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=wp["name"], use_container_width=True)

    # Check platform-specific directory for existing downloads
    if platform.system() == "Windows":
        download_dir = os.path.join(os.environ['USERPROFILE'], "Downloads")
    else:
        download_dir = os.path.join(os.environ['HOME'], "Downloads")
    file_path = os.path.join(download_dir, f"{wp['name']}.jpg")

    # Download button with limitation
    if st.session_state.downloaded.get(wp["name"], False):
        st.success("Already Downloaded")
    elif os.path.exists(file_path):
        st.success("Already Downloaded in Directory")
    else:
        if st.button("⬇ Download"):
            img.save(file_path)
            st.session_state.downloaded[wp["name"]] = True
            st.success("Downloaded")
            st.toast("Downloaded", icon="✅")

    # Apply button with limitation
    if st.session_state.applied.get(wp["name"], False):
        st.success("Already Applied")
    else:
        if st.button("Apply"):
            st.session_state.applied[wp["name"]] = True
            st.success("Applied as wallpaper (symbolic)")
            st.toast("Applied", icon="🎉")

    # Info button
    if st.button("ℹ Info"):
        st.info(f"Wallpaper Name: {wp['name']}\nTags: {', '.join(wp['tags'])}")

    # Back button
    if st.button("Back"):
        del st.session_state.selected_wallpaper
        st.experimental_rerun()

# Uploaded wallpapers
st.sidebar.header("Upload Your Wallpaper")
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Wallpaper", use_container_width=True)
        if st.sidebar.button("Save Uploaded Wallpaper"):
            save_path = os.path.join("uploaded_wallpapers", uploaded_file.name)
            os.makedirs("uploaded_wallpapers", exist_ok=True)
            img.save(save_path)
            st.sidebar.success(f"Saved to {save_path}")
    except Exception as e:
        st.sidebar.error(f"Error uploading image: {e}")

# Info section
st.sidebar.title("About")
st.sidebar.info("Made by Yaksh\nVersion: 2.3.5")