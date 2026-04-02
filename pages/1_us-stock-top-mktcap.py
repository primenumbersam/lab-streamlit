import pandas as pd
import streamlit as st
from PIL import Image
import base64
import io
import os
import datetime

# Page configuration (handled by main app, but we can set title for this page)
# st.set_page_config(layout="wide") # Commented out as it should be in main

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Vykreslení tabulky s logy
st.markdown("<h1 style='text-align: center; font-size: 20px;'>Top Global Companies Ranking</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>By Market Capitalization in Billions of USD</p>", unsafe_allow_html=True)
st.write("")

# Load the data
@st.cache_data
def load_data():
    DATA_PATH = "data/data-stock-us.csv"
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        st.error(f"Data file '{DATA_PATH}' not found.")
        return pd.DataFrame()
    return df

data_raw = load_data().copy()

if data_raw.empty:
    st.stop()

# Convert image to Base64
def image_to_base64(img_path, output_size=(64, 64)):
    # Check if the image path exists
    if os.path.exists(img_path):
        try:
            with Image.open(img_path) as img:
                img = img.resize(output_size)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        except Exception:
            return ""
    return ""

# If 'Logo' column doesn't exist, create one with path to the logos
if 'Logo' not in data_raw.columns:
    output_dir = 'assets/assets-logo'
    data_raw['Logo'] = data_raw['Name'].apply(lambda name: os.path.join(output_dir, f'{name}.png'))

# Convert image paths to Base64
# We use a progress bar as this might take a second
with st.spinner("Processing logos..."):
    data_raw["Logo_Base64"] = data_raw["Logo"].apply(image_to_base64)

image_column = st.column_config.ImageColumn(label="")
nazev_column = st.column_config.TextColumn(label="Company Name")
market_cap_column = st.column_config.TextColumn(label="Market Cap 💬", help="📍**in billions USD**")
price_column = st.column_config.TextColumn(label="Stock Price 💬", help="📍**Closing price from previous day (in USD)**")

# Adjust the index to start from 1 and display only the first 25 companies
data_raw.reset_index(drop=True, inplace=True)
data_display = data_raw.head(25).copy()
data_display.index = data_display.index + 1

data_display = data_display[['Logo_Base64', 'Name', 'Market Cap', 'Price']]

# Display the dataframe
st.dataframe(
    data_display, 
    height=913, 
    use_container_width=True,
    column_config={
        "Logo_Base64": image_column,
        "Name": nazev_column,
        'Market Cap': market_cap_column,
        'Price': price_column
    }
)

# Current date
dnesni_datum = datetime.date.today().strftime("%m.%d.%Y")

st.markdown(f'<span style="font-size: 14px">**Source:** companiesmarketcap.com | **Data as of:** {dnesni_datum} </span>', unsafe_allow_html=True)
