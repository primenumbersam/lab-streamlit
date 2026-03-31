import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Page config for high performance and premium look
st.set_page_config(
    page_title="KOSIS Visual & Wealth Data",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stHeadingContainer h1 {
        color: #1e3a8a;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        margin-bottom: 2rem;
    }
    .embed-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        background: white;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Data: KOSIS + WID")

# 1. KOSIS Embeds
st.subheader("🌐 KOSIS 국가통계포털")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="embed-container">', unsafe_allow_html=True)
    st.markdown("### 📈 경제지표보드")
    components.iframe("https://kosis.kr/visual/economyBoard/index.do?lang=ko", height=600, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="embed-container">', unsafe_allow_html=True)
    st.markdown("### 🌍 세계 속의 한국")
    components.iframe("https://kosis.kr/visual/koreaInWorld/index.do?lang=ko", height=600, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Wealth Inequality Chart (WID Data)
st.divider()
st.subheader("📉 국가별 부의 집중도 비교 (WID Data)")

try:
    # CSV Load - skipping header lines and handling semi-colon delimiter
    # Based on file check: data starts at line 14, columns: Percentile;Year;Korea;Japan;USA;Denmark
    df = pd.read_csv(
        "data/data-wid.csv", 
        sep=";", 
        skiprows=13, 
        names=["Percentile", "Year", "Korea", "Japan", "USA", "Denmark"],
        index_col=False
    )
    
    # Filter and clean
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    
    # Round values and apply Clipping (handling extreme outliers)
    countries = ["Korea", "Japan", "USA", "Denmark"]
    for col in countries:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Apply clipping: 0 to 800 (USA extreme spikes are handled here)
        df[col] = df[col].clip(lower=0, upper=800).round(0)
    
    # Premium Chart using Streamlit native line chart
    chart_data = df.set_index("Year")[countries]
    
    st.line_chart(chart_data, height=450, use_container_width=True)
    
    st.info("💡 데이터 설명: 상위 10%와 하위 50%의 자산 비율(Top 10 / Bottom 50 ratio)을 나타냅니다. USA 데이터와 같은 비정상적 수치(하위 50%의 순자산이 0에 가깝거나 음수인 경우)를 보정하기 위해 0~800 구간으로 Clipping(제한)하여 시각화 함. (출처: WID)")
    
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.warning("CSV 파일 형식이 예상과 다릅니다. 원본 파일을 확인해주세요.")
