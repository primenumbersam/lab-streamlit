---
title: 🚀 Streamlit Multi-Page Lab
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: streamlit
app_file: streamlit_app.py
pinned: false
---

# 🚀 Streamlit Demo: Multi-Page

A comprehensive collection of Streamlit experiments, data dashboards, and AI-powered tools merged into a single multi-page application. This project is designed for rapid prototyping and testing various Streamlit features and open-source templates.

## 🧪 Demos Pages

- **Home**: Interactive Altair charts and selection-enabled dataframes.
- **🌍 Top Stocks**: A visual ranking. Derived from `companiesmarketcap.com` data and logos (provided in CSV). File: `1_us-stock-top-mktcap.py`
- **📈 US Top Stock Peers**: Comparative analysis. Fetches real-time market data using the `yfinance` package. File: `2_us-stock-top-compare.py`
- **🗺️ GDP Dashboard**: Historical GDP analysis. Visualizes pre-saved World Bank data (in CSV). File: `3_global-gdp-compare.py`
- **🤖 Gemini File Q&A**: RAG tool using Gemini 3.1 Flash Lite. File: `4_llm-gemini-rag.py`
- **📊 KOSIS & Wealth Data**: KOSIS visual embed and wealth inequality chart (WID data). File: `5_kr-kosis-embed.py`

## 🏗️ Project Structure

```text
lab-streamlit/
├── assets/
│   └── assets-logo/           # Brand logos for the Top Companies demo
├── data/
│   ├── data-gdp.csv           # World Bank GDP dataset
│   ├── data-stock-us.csv      # Top companies market cap dataset
│   └── data-wid.csv           # World Inequality Database (Wealth)
├── pages/                     # Multi-page implementation
│   ├── 1_us-stock-top-mktcap.py
│   ├── 2_us-stock-top-compare.py
│   ├── 3_global-gdp-compare.py
│   ├── 4_llm-gemini-rag.py
│   └── 5_kr-kosis-embed.py
├── requirements.txt           # Project dependencies
└── streamlit_app.py        # Main entry point & Landing page
```

## 🛠️ Setup & Execution

### Prerequisites
- Python 3.11+
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey) (for Gemini File Q&A)

### Running Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## ⚙️ Configuration
The project is configured for seamless execution in **GitHub Codespaces**. Check `.devcontainer/devcontainer.json` for pre-configured environment settings.

## 📚 References & Credits
This lab integrates and adapts features from the following open-source projects:
- **Top Companies Market Cap**: [bi-cnc/top_companies_market_cap](https://github.com/bi-cnc/top_companies_market_cap)
- **Stock Peer Analysis**: [streamlit/demo-stockpeers](https://github.com/streamlit/demo-stockpeers)
- **GDP Dashboard**: [streamlit/GDP-Dashboard](https://github.com/streamlit/GDP-Dashboard)
- **Gemini File Q&A Source**: Adapted from [streamlit/llm-examples](https://github.com/streamlit/llm-examples) (Original Anthropic version)

---
*Built with ❤️ using Streamlit, Altair, and Google Gemini.*