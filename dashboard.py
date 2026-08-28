import html
from datetime import datetime

import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from rapidfuzz import process, utils


st.set_page_config(
    page_title="FinTech Analytics",
    page_icon="📊",
    layout="wide"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #0b1220 0%, #05070a 55%, #030407 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: #101827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

div[data-testid="stMetricContainer"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.35rem 1.5rem;
    box-shadow: 0 16px 40px rgba(0,0,0,0.28);
}

div[data-testid="stMetricLabel"] p {
    color: #94a3b8 !important;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc !important;
}

.chart-card,
.news-card,
.snapshot-card {
    background: linear-gradient(180deg, rgba(18,27,45,0.78), rgba(10,15,27,0.58));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
}

.news-card {
    margin-bottom: 0.8rem;
}

.news-source {
    color: #38bdf8;
    font-size: 0.78rem;
    font-weight: 700;
}

.news-time {
    color: #64748b;
    font-size: 0.78rem;
}

.news-title {
    color: #f8fafc;
    font-size: 1.05rem;
    font-weight: 700;
    text-decoration: none;
}

.news-summary {
    color: #94a3b8;
    font-size: 0.88rem;
    line-height: 1.55;
    margin-top: 0.45rem;
}

.dev-card {
    margin-top: 2rem;
    padding: 0.9rem;
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    background: rgba(255,255,255,0.035);
}

.dev-label {
    color: #94a3b8;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.dev-name {
    color: #f8fafc;
    font-size: 0.9rem;
    font-weight: 700;
}

.dev-build {
    float: right;
    color: #38bdf8;
    font-size: 0.72rem;
}

.marquee-box {
    overflow: hidden;
    white-space: nowrap;
    background: rgba(7,11,20,0.72);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 0.85rem 1rem;
    margin-bottom: 1.5rem;
}

.marquee-track {
    display: inline-block;
    animation: market-scroll 32s linear infinite;
}

.ticker-item {
    display: inline-block;
    margin-right: 3.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #e2e8f0;
}

.ticker-up { color: #2dd4bf; }
.ticker-down { color: #fb7185; }

.quote-status {
    color: #64748b;
    font-size: 0.76rem;
    margin-top: -0.4rem;
    margin-bottom: 0.7rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 0.55rem 1rem;
    color: #94a3b8;
}

.stTabs [aria-selected="true"] {
    color: #f8fafc !important;
    background: rgba(56,189,248,0.10) !important;
    border-color: rgba(56,189,248,0.28) !important;
}

@keyframes market-scroll {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=86400)
def company_index():
    return {
        "apple": "AAPL", "amazon": "AMZN", "nvidia": "NVDA",
        "microsoft": "MSFT", "google": "GOOGL", "alphabet": "GOOGL",
        "tesla": "TSLA", "meta": "META", "facebook": "META",
        "netflix": "NFLX", "intel": "INTC", "jpmorgan chase": "JPM",
        "jp morgan": "JPM", "jpmorgan": "JPM", "disney": "DIS",
        "nike": "NKE", "starbucks": "SBUX", "mcdonalds": "MCD",
        "coca cola": "KO", "coca-cola": "KO", "pepsi": "PEP",
        "walmart": "WMT", "visa": "V", "mastercard": "MA",
        "exxon mobil": "XOM", "chevron": "CVX", "home depot": "HD",
        "costco": "COST", "procter and gamble": "PG", "pfizer": "PFE",
        "johnson and johnson": "JNJ", "bank of america": "BAC",
        "goldman sachs": "GS", "morgan stanley": "MS",
        "american express": "AXP", "salesforce": "CRM", "oracle": "ORCL",
        "adobe": "ADBE", "cisco": "CSCO", "advanced micro devices": "AMD",
        "amd": "AMD", "qualcomm": "QCOM", "t mobile": "TMUS",
        "t-mobile": "TMUS", "verizon": "VZ", "at&t": "T",
        "unitedhealth": "UNH", "eli lilly": "LLY", "thermo fisher": "TMO",
        "boeing": "BA", "caterpillar": "CAT", "general electric": "GE",
        "ford": "F", "general motors": "GM", "sony": "SONY",
        "toyota": "TM", "honda": "HMC", "ferrari": "RACE",
        "adidas": "ADDYY"
    }


def get_ticker(query):
    query = query.strip()

    if not query:
        return None

    index = company_index()
    direct_ticker = query.upper()

    if direct_ticker in index.values():
        return direct_ticker

    normalized_query = query.lower()

    if normalized_query in index:
        return index[normalized_query]

    match = process.extractOne(
        normalized_query,
        index.keys(),
        processor=utils.default_process,
        score_cutoff=82
    )

    if match:
        return index[match[0]]

    return direct_ticker


@st.cache_data(ttl=3600)
def usd_rate(currency):
    if not currency or currency == "USD":
        return 1.0

    try:
        history = yf.Ticker(f"{currency}USD=X").history(period="5d")
        if not history.empty:
            return float(history["Close"].iloc[-1])
    except Exception:
        pass

    return 1.0


@st.cache_data(ttl=300)
def get_market_history(ticker, period="1mo"):
    return yf.Ticker(ticker).history(period=period)


@st.cache_data(ttl=300)
def get_stock_info(ticker):
    return yf.Ticker(ticker).info


@st.cache_data(ttl=60)
def get_live_quote(ticker):
    stock = yf.Ticker(ticker)
    price = None
    previous_close = None

    # Try the latest quote first.
    try:
        fast = stock.fast_info
        price = fast.get("last_price") or fast.get("lastPrice")
        previous_close = (
            fast.get("previous_close")
            or fast.get("previousClose")
            or fast.get("regular_market_previous_close")
        )
    except Exception:
        pass

    # Fall back to the latest intraday bar.
    if price is None:
        try:
            intraday = stock.history(period="1d", interval="1m", prepost=False)
            if not intraday.empty:
                price = float(intraday["Close"].iloc[-1])
        except Exception:
            pass

    # Use the regular market quote if needed.
    if price is None:
        try:
            info = stock.info
            price = (
                info.get("regularMarketPrice")
                or info.get("currentPrice")
            )
            previous_close = previous_close or (
                info.get("regularMarketPreviousClose")
                or info.get("previousClose")
            )
        except Exception:
            pass

    return {
        "price": float(price) if price is not None else None,
        "previous_close": float(previous_close) if previous_close is not None else None,
        "updated_at": datetime.now().strftime("%I:%M:%S %p")
    }


@st.cache_data(ttl=120)
def get_ticker_strip():
    symbols = [
        "JPM", "DIS", "NVDA", "TSLA", "AMZN",
        "GOOGL", "AAPL", "MSFT", "META", "NFLX"
    ]

    items = []

    for symbol in symbols:
        try:
            quote = get_live_quote(symbol)
            current = quote["price"]
            previous = quote["previous_close"]

            if current is None:
                continue

            change = (current - previous) if previous is not None else 0

            if change >= 0:
                change_html = f'<span class="ticker-up">+{change:.2f} ▲</span>'
            else:
                change_html = f'<span class="ticker-down">{change:.2f} ▼</span>'

            items.append(
                f'<span class="ticker-item">'
                f'{symbol} {current:.2f} {change_html}'
                f'</span>'
            )
        except Exception:
            continue

    if not items:
        return (
            '<div class="marquee-box">'
            '<span class="ticker-item">Market data is temporarily unavailable.</span>'
            '</div>'
        )

    content = "".join(items)

    return f"""
    <div class="marquee-box">
        <div class="marquee-track">
            {content}{content}
        </div>
    </div>
    """


def normalize_news_item(item):
    content = item.get("content", item)

    provider = content.get("provider", {})
    if isinstance(provider, dict):
        source = provider.get("displayName") or provider.get("name") or "News"
    else:
        source = item.get("publisher") or "News"

    canonical_url = content.get("canonicalUrl", {})
    if isinstance(canonical_url, dict):
        link = canonical_url.get("url")
    else:
        link = canonical_url

    link = link or item.get("link") or item.get("url") or "#"

    title = content.get("title") or item.get("title") or "Untitled article"
    summary = content.get("summary") or item.get("summary") or ""

    published = (
        content.get("pubDate")
        or content.get("displayTime")
        or item.get("providerPublishTime")
        or ""
    )

    return {
        "title": str(title),
        "summary": str(summary),
        "source": str(source),
        "published": str(published),
        "link": str(link)
    }


@st.cache_data(ttl=300)
def get_company_news(ticker):
    try:
        raw_news = yf.Ticker(ticker).get_news(count=10, tab="news")
        return [normalize_news_item(item) for item in raw_news]
    except Exception:
        return []


@st.cache_data(ttl=300)
def get_market_news():
    try:
        search = yf.Search("stock market", news_count=10)
        raw_news = getattr(search, "news", []) or []
        if raw_news:
            return [normalize_news_item(item) for item in raw_news]
    except Exception:
        pass

    try:
        raw_news = yf.Ticker("SPY").get_news(count=10, tab="news")
        return [normalize_news_item(item) for item in raw_news]
    except Exception:
        return []


def render_news_card(article):
    title = html.escape(article["title"])
    source = html.escape(article["source"])
    published = html.escape(article["published"])
    summary = html.escape(article["summary"])
    link = html.escape(article["link"], quote=True)

    summary_html = ""
    if summary:
        summary_html = f'<div class="news-summary">{summary}</div>'

    st.markdown(
        f"""
        <div class="news-card">
            <div>
                <span class="news-source">{source}</span>
                <span class="news-time"> · {published}</span>
            </div>
            <div style="margin-top:0.35rem;">
                <a class="news-title" href="{link}" target="_blank">
                    {title}
                </a>
            </div>
            {summary_html}
        </div>
        """,
        unsafe_allow_html=True
    )


with st.sidebar:
    st.markdown("## 🏦 FINTECH ANALYTICS")
    st.divider()

    search_input = st.text_input(
        "🔍 Search company name or ticker",
        value="JPM",
        placeholder="AAPL, Apple, Tesla..."
    )

    st.caption("Press Enter to apply")
    st.divider()

    st.markdown("""
    <div class="dev-card">
        <div class="dev-label">ENGINEERING PORTFOLIO</div>
        <div style="margin-top:8px;">
            <span class="dev-name">Dhairya</span>
            <span class="dev-build">Build v2.3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


active_ticker = get_ticker(search_input)

if not active_ticker:
    st.info("Enter a company name or ticker to get started.")
    st.stop()


try:
    history = get_market_history(active_ticker, "1mo")

    if history.empty:
        st.warning(
            f"No market data was found for '{search_input}'. "
            "Try another company name or ticker."
        )
        st.stop()

    info = get_stock_info(active_ticker)
    quote = get_live_quote(active_ticker)

    company_name = (
        info.get("longName")
        or info.get("shortName")
        or active_ticker
    )

    currency = info.get("currency") or "USD"
    fx_rate = usd_rate(currency)

    fallback_price = float(history["Close"].iloc[-1])

    raw_price = quote["price"] or fallback_price
    raw_high = (
        info.get("fiftyTwoWeekHigh")
        or float(history["High"].max())
    )

    price_usd = float(raw_price) * fx_rate
    high_usd = float(raw_high) * fx_rate
    pe_ratio = info.get("trailingPE")

    history = history.reset_index()
    history["Close_USD"] = history["Close"] * fx_rate

    st.markdown(get_ticker_strip(), unsafe_allow_html=True)

    dashboard_tab, news_tab = st.tabs([
        "📊 Dashboard",
        "📰 News"
    ])

    with dashboard_tab:
        st.markdown("## 📊 Live Financial Analytics Platform")
        st.markdown(
            f"""
            <p style="color:#94a3b8; margin-top:-10px;">
            Tracking <b>{company_name}</b> ({active_ticker}) ·
            Values converted from <b>{currency} to USD</b>
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="quote-status">Latest quote checked at {quote["updated_at"]}</div>',
            unsafe_allow_html=True
        )

        metric_1, metric_2, metric_3 = st.columns(3)

        metric_1.metric(
            "CURRENT PRICE (USD)",
            f"${price_usd:,.2f}"
        )

        metric_2.metric(
            "P/E RATIO",
            f"{pe_ratio:,.2f}" if pe_ratio is not None else "N/A"
        )

        metric_3.metric(
            "52-WEEK HIGH (USD)",
            f"${high_usd:,.2f}"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        left_chart, right_chart = st.columns(2)

        with left_chart:
            st.markdown(
                '<div class="chart-card"><h4>📈 30-Day Stock Price Trend (USD)</h4>',
                unsafe_allow_html=True
            )

            price_chart = go.Figure()

            price_chart.add_trace(
                go.Scatter(
                    x=history["Date"],
                    y=history["Close_USD"],
                    mode="lines",
                    fill="tozeroy",
                    line=dict(color="#2dd4bf", width=3),
                    fillcolor="rgba(45,212,191,0.05)",
                    hovertemplate=(
                        "<b>Date:</b> %{x|%b %d, %Y}"
                        "<br><b>Price:</b> $%{y:,.2f}"
                        "<extra></extra>"
                    )
                )
            )

            price_chart.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=360,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(color="#94a3b8")
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.07)",
                    zeroline=False,
                    tickprefix="$",
                    tickfont=dict(color="#94a3b8")
                )
            )

            st.plotly_chart(price_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with right_chart:
            st.markdown(
                '<div class="chart-card"><h4>📊 30-Day Daily Trading Volume</h4>',
                unsafe_allow_html=True
            )

            volume_chart = go.Figure()

            volume_chart.add_trace(
                go.Bar(
                    x=history["Date"],
                    y=history["Volume"],
                    marker_color="#38bdf8",
                    opacity=0.85,
                    hovertemplate=(
                        "<b>Date:</b> %{x|%b %d, %Y}"
                        "<br><b>Volume:</b> %{y:,}"
                        "<extra></extra>"
                    )
                )
            )

            volume_chart.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=360,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(color="#94a3b8")
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.07)",
                    zeroline=False,
                    tickfont=dict(color="#94a3b8")
                )
            )

            st.plotly_chart(volume_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with news_tab:
        st.markdown(f"## 📰 News Center")
        st.markdown(
            f"""
            <p style="color:#94a3b8; margin-top:-10px;">
            Latest headlines related to <b>{company_name}</b> and the broader market.
            </p>
            """,
            unsafe_allow_html=True
        )

        company_news_tab, market_news_tab = st.tabs([
            f"🏢 {active_ticker} News",
            "🌐 Market News"
        ])

        with company_news_tab:
            articles = get_company_news(active_ticker)

            if articles:
                for article in articles:
                    render_news_card(article)
            else:
                st.info("No recent company news is available right now.")

        with market_news_tab:
            articles = get_market_news()

            if articles:
                for article in articles:
                    render_news_card(article)
            else:
                st.info("No recent market news is available right now.")

except Exception as error:
    st.error(f"Could not load market data: {error}")
