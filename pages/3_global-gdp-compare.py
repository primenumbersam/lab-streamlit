import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Main title
st.title(":earth_americas: Global GDP Dashboard")

# -----------------------------------------------------------------------------
# Functions

@st.cache_data
def get_gdp_data():
    # Adjusted path for working inside pages/ directory
    DATA_FILENAME = Path(__file__).parent.parent / 'data/data-gdp.csv'
    if not DATA_FILENAME.exists():
        st.error(f"Data file not found at {DATA_FILENAME}")
        return pd.DataFrame()
        
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    return gdp_df

gdp_df = get_gdp_data()

if gdp_df.empty:
    st.stop()

# -----------------------------------------------------------------------------
# Draw page

st.markdown("""
Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. 
This dashboard allows you to compare economic growth across different countries over several decades.
""")

""
""

min_value = int(gdp_df['Year'].min())
max_value = int(gdp_df['Year'].max())

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = sorted(gdp_df['Country Code'].unique())

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['KOR', 'USA', 'CHN', 'JPN', 'DEU', 'GBR']) # Added KOR for context

""
""

# Filter data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')
st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
    use_container_width=True
)

""
""

first_year_data = gdp_df[gdp_df['Year'] == from_year]
last_year_data = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP Comparison (Current: {to_year} vs Base: {from_year})', divider='gray')

cols = st.columns(min(len(selected_countries), 4))
for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]
    with col:
        try:
            val_start = first_year_data[first_year_data['Country Code'] == country]['GDP'].iat[0]
            val_end = last_year_data[last_year_data['Country Code'] == country]['GDP'].iat[0]
            
            last_gdp_billions = val_end / 1000000000
            
            if math.isnan(val_start) or val_start == 0:
                growth = 'n/a'
                delta_color = 'off'
            else:
                growth = f'{val_end / val_start:,.2f}x'
                delta_color = 'normal'
            
            st.metric(
                label=f'{country} GDP',
                value=f'${last_gdp_billions:,.0f}B',
                delta=growth,
                delta_color=delta_color
            )
        except (IndexError, KeyError):
            st.metric(label=f'{country} GDP', value="n/a")
