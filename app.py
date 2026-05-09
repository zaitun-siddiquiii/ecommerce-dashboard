import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Commerce Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/ecommerce_cleaned.csv")
    rfm = pd.read_csv("data/cleaned/rfm_segments.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df, rfm

df, rfm = load_data()

REVENUE_COL = "amount"
QUANTITY_COL = "qty"
REGION_COL = "ship_state"
PRODUCT_COL = "sku"

# ─────────────────────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(124,58,237,0.20), transparent 30%),
        radial-gradient(circle at bottom right, rgba(59,130,246,0.18), transparent 35%),
        linear-gradient(135deg, #050816 0%, #0B1120 40%, #111827 100%);
    color: white;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.82);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.06);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero {
    position: relative;
    padding: 5rem 4rem;
    border-radius: 32px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(22px);
    overflow: hidden;
    margin-top: 1rem;
}

.hero::before {
    content: "";
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(124,58,237,0.35), transparent 70%);
    top: -120px;
    right: -100px;
    filter: blur(30px);
}

.hero::after {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(59,130,246,0.25), transparent 70%);
    bottom: -140px;
    left: -120px;
    filter: blur(30px);
}

.hero-title {
    font-size: 5rem;
    font-weight: 900;
    line-height: 1;
    background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 35%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    z-index: 10;
}

.hero-sub {
    color: #CBD5E1;
    font-size: 1.15rem;
    margin-top: 1.8rem;
    max-width: 900px;
    line-height: 1.9;
    position: relative;
    z-index: 10;
}

.kpi-strip {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
    position: relative;
    z-index: 10;
}

.kpi-pill {
    padding: 0.8rem 1.2rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    color: white;
    font-size: 0.95rem;
    backdrop-filter: blur(14px);
}

.metric-card {
    background: rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 1.8rem;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-8px);
    border: 1px solid rgba(124,58,237,0.45);
    box-shadow: 0 25px 50px rgba(0,0,0,0.35);
}

.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
}

.metric-label {
    color: #94A3B8;
    font-size: 0.9rem;
}

.metric-value {
    font-size: 2.4rem;
    font-weight: 800;
    margin-top: 1rem;
    color: white;
}

.metric-delta {
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-weight: 600;
}

.delta-up {
    color: #34D399;
}

.delta-down {
    color: #F87171;
}

.glass {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 26px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    margin-top: 1rem;
}

.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
}

.section-subtitle {
    font-size: 0.9rem;
    color: #64748B;
    margin-top: -0.7rem;
    margin-bottom: 1rem;
}

[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.04);
    border-radius: 20px;
    overflow: hidden;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    color: white;
}

.stMultiSelect > div > div {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

.insight-box {
    padding: 1.5rem;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(124,58,237,0.12));
    border: 1px solid rgba(255,255,255,0.08);
    color: #E2E8F0;
    line-height: 1.8;
}

.search-result-badge {
    background: rgba(139,92,246,0.2);
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 12px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    color: #C084FC;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.filter-chip {
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    color: #93C5FD;
    display: inline-block;
    margin: 2px;
}

.sidebar-filter-count {
    background: rgba(139,92,246,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    color: #C084FC;
}

.tab-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #CBD5E1;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    color: #94A3B8;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: rgba(139,92,246,0.25) !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR — Enhanced with date range + search + export
# ─────────────────────────────────────────────────────────────
st.sidebar.markdown("## ◈ Commerce Intelligence")
st.sidebar.markdown("---")

# Year filter
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("📅 Select Years", years, default=years)

# Month range slider
st.sidebar.markdown("**Month Range**")
month_range = st.sidebar.slider(
    "Select Month Range",
    min_value=1,
    max_value=12,
    value=(1, 12),
    format="%d"
)

st.sidebar.markdown("---")

# Region filter
regions = sorted(df[REGION_COL].dropna().unique())
selected_regions = st.sidebar.multiselect("🗺️ Select Regions", regions, default=regions)

# Category filter
categories = sorted(df["category"].dropna().unique())
selected_categories = st.sidebar.multiselect("🏷️ Select Categories", categories, default=categories)

st.sidebar.markdown("---")

# Product search
product_search = st.sidebar.text_input("🔍 Search Product (SKU)", placeholder="e.g. SKU-1234")

st.sidebar.markdown("---")

# Active filter summary
active_filters = []
if len(selected_years) < len(years):
    active_filters.append(f"{len(selected_years)} years")
if len(selected_regions) < len(regions):
    active_filters.append(f"{len(selected_regions)} regions")
if len(selected_categories) < len(categories):
    active_filters.append(f"{len(selected_categories)} categories")
if month_range != (1, 12):
    active_filters.append(f"Months {month_range[0]}–{month_range[1]}")

if active_filters:
    st.sidebar.markdown("**Active Filters:**")
    chips_html = " ".join([f'<span class="filter-chip">{f}</span>' for f in active_filters])
    st.sidebar.markdown(chips_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────
filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df[REGION_COL].isin(selected_regions)) &
    (df["category"].isin(selected_categories)) &
    (df["month"] >= month_range[0]) &
    (df["month"] <= month_range[1])
]

# Product search filter (for product section only)
if product_search:
    product_filtered_df = filtered_df[
        filtered_df[PRODUCT_COL].astype(str).str.contains(product_search, case=False, na=False)
    ]
else:
    product_filtered_df = filtered_df

# ─────────────────────────────────────────────────────────────
# KPIs — Current Period
# ─────────────────────────────────────────────────────────────
total_revenue = filtered_df[REVENUE_COL].sum()
total_orders = filtered_df["order_id"].nunique()
avg_order_value = filtered_df[REVENUE_COL].mean() if len(filtered_df) > 0 else 0
units_sold = filtered_df[QUANTITY_COL].sum()

if "customer_id" in filtered_df.columns:
    unique_customers = filtered_df["customer_id"].nunique()
else:
    unique_customers = filtered_df["order_id"].nunique()

# ─────────────────────────────────────────────────────────────
# KPIs — Prior Period (for delta)
# ─────────────────────────────────────────────────────────────
prior_years = [y - 1 for y in selected_years]
prior_df = df[
    (df["year"].isin(prior_years)) &
    (df[REGION_COL].isin(selected_regions)) &
    (df["category"].isin(selected_categories)) &
    (df["month"] >= month_range[0]) &
    (df["month"] <= month_range[1])
]

prior_revenue = prior_df[REVENUE_COL].sum() if len(prior_df) > 0 else None
prior_orders = prior_df["order_id"].nunique() if len(prior_df) > 0 else None
prior_aov = prior_df[REVENUE_COL].mean() if len(prior_df) > 0 else None
prior_units = prior_df[QUANTITY_COL].sum() if len(prior_df) > 0 else None

def delta_html(current, prior, prefix="", suffix="", format_fn=None):
    if prior is None or prior == 0:
        return ""
    pct = ((current - prior) / prior) * 100
    arrow = "▲" if pct >= 0 else "▼"
    cls = "delta-up" if pct >= 0 else "delta-down"
    return f'<div class="metric-delta {cls}">{arrow} {abs(pct):.1f}% vs prior period</div>'

# ─────────────────────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
<div class="hero-title">Commerce Intelligence</div>
<div class="hero-sub">
Premium revenue intelligence platform for sales analytics,
customer segmentation, growth monitoring, regional performance,
and product demand insights.
</div>
<div class="kpi-strip">
<div class="kpi-pill">📦 {total_orders:,}+ Orders</div>
<div class="kpi-pill">💰 ₹{total_revenue/10000000:.2f} Cr Revenue</div>
<div class="kpi-pill">🏷️ {filtered_df['category'].nunique()} Categories</div>
<div class="kpi-pill">🗺️ {filtered_df[REGION_COL].nunique()} Regions</div>
<div class="kpi-pill">📅 Months {month_range[0]}–{month_range[1]}</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# EXPORT BUTTON
# ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

export_col, _ = st.columns([1, 4])
with export_col:
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Export Filtered Data (CSV)",
        data=csv_buffer.getvalue(),
        file_name="commerce_intelligence_export.csv",
        mime="text/csv",
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# KPI CARDS with Delta Badges
# ─────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

cards = [
    ("Revenue", f"₹{total_revenue/100000:.1f}L", delta_html(total_revenue, prior_revenue)),
    ("Orders", f"{total_orders:,}", delta_html(total_orders, prior_orders)),
    ("AOV", f"₹{avg_order_value:.0f}", delta_html(avg_order_value, prior_aov)),
    ("Customers", f"{unique_customers:,}", ""),
    ("Units Sold", f"{units_sold:,}", delta_html(units_sold, prior_units)),
]

for col, card in zip([k1, k2, k3, k4, k5], cards):
    with col:
        st.markdown(f"""
<div class="metric-card">
<div class="metric-label">{card[0]}</div>
<div class="metric-value">{card[1]}</div>
{card[2]}
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS — Main Content
# ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue Analytics",
    "🏷️ Products & Categories",
    "🗺️ Regional Performance",
    "👥 Customer Segments"
])

# ══════════════════════════════════════════════
# TAB 1 — REVENUE ANALYTICS
# ══════════════════════════════════════════════
with tab1:

    # Monthly Revenue Trend
    monthly = (
        filtered_df
        .groupby(["year", "month"])[REVENUE_COL]
        .sum()
        .reset_index()
    )
    monthly["period"] = (
        monthly["year"].astype(str) + "-" +
        monthly["month"].astype(str).str.zfill(2)
    )

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly["period"],
        y=monthly[REVENUE_COL],
        mode="lines+markers",
        name="Revenue",
        line=dict(width=4, color="#8B5CF6"),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(139,92,246,0.12)"
    ))

    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False, color="#CBD5E1"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#CBD5E1"),
        font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )

    st.markdown("""
<div class="glass">
<div class="section-title">Monthly Revenue Trend</div>
<div class="section-subtitle">Revenue aggregated by month across selected filters</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # YoY Comparison Chart
    if len(years) >= 2:
        yoy_data = (
            df[
                (df[REGION_COL].isin(selected_regions)) &
                (df["category"].isin(selected_categories)) &
                (df["month"] >= month_range[0]) &
                (df["month"] <= month_range[1])
            ]
            .groupby(["year", "month"])[REVENUE_COL]
            .sum()
            .reset_index()
        )

        fig_yoy = go.Figure()
        colors_yoy = ["#8B5CF6", "#3B82F6", "#34D399", "#FBBF24", "#F472B6"]
        for i, yr in enumerate(sorted(yoy_data["year"].unique())):
            yr_data = yoy_data[yoy_data["year"] == yr].sort_values("month")
            fig_yoy.add_trace(go.Scatter(
                x=yr_data["month"],
                y=yr_data[REVENUE_COL],
                mode="lines+markers",
                name=str(yr),
                line=dict(width=3, color=colors_yoy[i % len(colors_yoy)]),
                marker=dict(size=7)
            ))

        fig_yoy.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(
                showgrid=False, color="#CBD5E1",
                tickvals=list(range(1, 13)),
                ticktext=["Jan","Feb","Mar","Apr","May","Jun",
                          "Jul","Aug","Sep","Oct","Nov","Dec"]
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#CBD5E1"),
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1)
        )

        st.markdown("""
<div class="glass">
<div class="section-title">Year-over-Year Comparison</div>
<div class="section-subtitle">Monthly revenue stacked across all years for direct comparison</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig_yoy, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue vs Units Scatter
    scatter_data = (
        filtered_df
        .groupby("category")
        .agg(
            revenue=(REVENUE_COL, "sum"),
            units=(QUANTITY_COL, "sum"),
            orders=("order_id", "nunique")
        )
        .reset_index()
    )

    fig_scatter = px.scatter(
        scatter_data,
        x="units",
        y="revenue",
        size="orders",
        color="category",
        hover_name="category",
        size_max=60,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#CBD5E1", title="Units Sold"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#CBD5E1", title="Revenue (₹)"),
        font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )

    st.markdown("""
<div class="glass">
<div class="section-title">Revenue vs Units by Category</div>
<div class="section-subtitle">Bubble size = number of orders. Reveals high-value vs high-volume categories.</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — PRODUCTS & CATEGORIES
# ══════════════════════════════════════════════
with tab2:

    # Product search result badge
    if product_search:
        result_count = len(product_filtered_df[PRODUCT_COL].unique())
        st.markdown(f"""
<div class="search-result-badge">
🔍 Showing {result_count} SKUs matching "{product_search}"
</div>
""", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:
        cat = (
            filtered_df
            .groupby("category")[REVENUE_COL]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig_cat = px.bar(
            cat.head(10),
            x=REVENUE_COL,
            y="category",
            orientation="h",
            color=REVENUE_COL,
            color_continuous_scale="purples"
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=420,
            margin=dict(l=0, r=0, t=20, b=0),
            coloraxis_showscale=False,
            font=dict(color="white")
        )

        st.markdown("""
<div class="glass">
<div class="section-title">Category Revenue</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        cat_units = (
            filtered_df
            .groupby("category")[QUANTITY_COL]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig_cat_units = px.pie(
            cat_units.head(8),
            names="category",
            values=QUANTITY_COL,
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_cat_units.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=420,
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )

        st.markdown("""
<div class="glass">
<div class="section-title">Units Share by Category</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig_cat_units, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Top Products (with search filter applied)
    products = (
        product_filtered_df
        .groupby(PRODUCT_COL)[REVENUE_COL]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )

    fig_prod = px.bar(
        products.sort_values(REVENUE_COL),
        x=REVENUE_COL,
        y=PRODUCT_COL,
        orientation="h",
        color=REVENUE_COL,
        color_continuous_scale="blues"
    )
    fig_prod.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max(400, len(products) * 28),
        margin=dict(l=0, r=0, t=20, b=0),
        coloraxis_showscale=False,
        font=dict(color="white")
    )

    title_suffix = f' — "{product_search}"' if product_search else ""
    st.markdown(f"""
<div class="glass">
<div class="section-title">Top Products{title_suffix}</div>
<div class="section-subtitle">Top 20 SKUs by revenue in selected filters</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Product Summary Table
    st.markdown("<br>", unsafe_allow_html=True)
    product_table = (
        product_filtered_df
        .groupby(PRODUCT_COL)
        .agg(
            Revenue=(REVENUE_COL, "sum"),
            Orders=("order_id", "nunique"),
            Units=(QUANTITY_COL, "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(30)
        .reset_index()
    )
    product_table["AOV (₹)"] = (product_table["Revenue"] / product_table["Orders"]).round(0)
    product_table["Revenue"] = product_table["Revenue"].apply(lambda x: f"₹{x:,.0f}")

    st.markdown("""
<div class="glass">
<div class="section-title">Product Summary Table</div>
<div class="section-subtitle">Top 30 SKUs with key metrics</div>
""", unsafe_allow_html=True)
    st.dataframe(product_table, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — REGIONAL PERFORMANCE
# ══════════════════════════════════════════════
with tab3:

    reg = (
        filtered_df
        .groupby(REGION_COL)[REVENUE_COL]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    r1, r2 = st.columns([1, 1])

    with r1:
        fig_reg_bar = px.bar(
            reg,
            x=REVENUE_COL,
            y=REGION_COL,
            orientation="h",
            color=REVENUE_COL,
            color_continuous_scale="teal"
        )
        fig_reg_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
            margin=dict(l=0, r=0, t=20, b=0),
            coloraxis_showscale=False,
            font=dict(color="white")
        )

        st.markdown("""
<div class="glass">
<div class="section-title">Revenue by Region</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig_reg_bar, use_container_width=True)

    with r2:
        fig_reg_pie = px.pie(
            reg,
            names=REGION_COL,
            values=REVENUE_COL,
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_reg_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=500,
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )

        st.markdown("""
<div class="glass">
<div class="section-title">Regional Contribution</div>
</div>
""", unsafe_allow_html=True)
        st.plotly_chart(fig_reg_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Region x Category Heatmap
    heat_data = (
        filtered_df
        .groupby([REGION_COL, "category"])[REVENUE_COL]
        .sum()
        .reset_index()
    )

    top_regions = reg.head(10)[REGION_COL].tolist()
    top_cats = cat.head(8)["category"].tolist() if "cat" in dir() else categories[:8]

    heat_pivot = (
        heat_data[
            heat_data[REGION_COL].isin(top_regions) &
            heat_data["category"].isin(top_cats)
        ]
        .pivot(index=REGION_COL, columns="category", values=REVENUE_COL)
        .fillna(0)
    )

    fig_heat = px.imshow(
        heat_pivot,
        color_continuous_scale="purples",
        aspect="auto"
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=0, r=0, t=20, b=0),
        font=dict(color="white"),
        coloraxis_showscale=True
    )

    st.markdown("""
<div class="glass">
<div class="section-title">Region × Category Revenue Heatmap</div>
<div class="section-subtitle">Darker = higher revenue concentration. Top 10 regions × Top 8 categories.</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — CUSTOMER SEGMENTS
# ══════════════════════════════════════════════
with tab4:

    if "segment" in rfm.columns:

        seg = (
            rfm
            .groupby("segment")
            .size()
            .reset_index(name="customers")
            .sort_values("customers", ascending=False)
        )

        s1, s2 = st.columns([1.3, 1])

        with s1:
            fig_seg = px.bar(
                seg,
                x="segment",
                y="customers",
                color="customers",
                color_continuous_scale="sunset",
                text="customers"
            )
            fig_seg.update_traces(textposition="outside", textfont_color="white")
            fig_seg.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=420,
                coloraxis_showscale=False,
                font=dict(color="white"),
                margin=dict(l=0, r=0, t=20, b=0)
            )

            st.markdown("""
<div class="glass">
<div class="section-title">Customer Segments</div>
<div class="section-subtitle">RFM-based segmentation: Champions, Loyal, At-Risk, Lost, etc.</div>
""", unsafe_allow_html=True)
            st.plotly_chart(fig_seg, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            # Segment donut
            fig_seg_pie = px.pie(
                seg,
                names="segment",
                values="customers",
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_seg_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                font=dict(color="white"),
                legend=dict(bgcolor="rgba(0,0,0,0)")
            )

            st.markdown("""
<div class="glass">
<div class="section-title">Segment Share</div>
</div>
""", unsafe_allow_html=True)
            st.plotly_chart(fig_seg_pie, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # RFM metrics per segment
        if all(c in rfm.columns for c in ["recency", "frequency", "monetary"]):
            rfm_summary = (
                rfm
                .groupby("segment")
                .agg(
                    Customers=("segment", "count"),
                    Avg_Recency=("recency", "mean"),
                    Avg_Frequency=("frequency", "mean"),
                    Avg_Monetary=("monetary", "mean")
                )
                .round(1)
                .sort_values("Avg_Monetary", ascending=False)
                .reset_index()
            )
            rfm_summary["Avg_Monetary"] = rfm_summary["Avg_Monetary"].apply(lambda x: f"₹{x:,.0f}")

            st.markdown("""
<div class="glass">
<div class="section-title">RFM Metrics by Segment</div>
<div class="section-subtitle">Average Recency (days), Frequency (orders), and Monetary value per segment</div>
""", unsafe_allow_html=True)
            st.dataframe(rfm_summary, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("RFM segment column not found. Ensure rfm_segments.csv contains a 'segment' column.")

# ─────────────────────────────────────────────────────────────
# AI INSIGHTS — Always at bottom
# ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

top_category = cat.iloc[0]["category"] if len(cat) > 0 else "N/A"
top_region = reg.iloc[0][REGION_COL] if len(reg) > 0 else "N/A"
revenue_delta_text = ""
if prior_revenue and prior_revenue > 0:
    delta_pct = ((total_revenue - prior_revenue) / prior_revenue) * 100
    direction = "up" if delta_pct >= 0 else "down"
    revenue_delta_text = f"Revenue is <b>{direction} {abs(delta_pct):.1f}%</b> vs the prior period.<br><br>"

st.markdown(f"""
<div class="insight-box">
<h3 style="margin-top:0;">🧠 Executive Insights</h3>
- Highest revenue contribution came from <b>{top_category}</b> category.<br><br>
- Strongest regional performance observed in <b>{top_region}</b>.<br><br>
- Average order value currently stands at <b>₹{avg_order_value:.0f}</b>.<br><br>
- {revenue_delta_text}Revenue analytics indicate strong category concentration and repeat purchase opportunities.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Commerce Intelligence Dashboard • Streamlit • Plotly • RFM Analytics • YoY Comparison")