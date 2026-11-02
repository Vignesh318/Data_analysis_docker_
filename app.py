import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Generate sample dataset
@st.cache_data
def load_data():
    data = {
        "Date": pd.to_datetime([
            "2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08",
            "2026-01-09", "2026-01-10", "2026-01-11", "2026-01-12",
            "2026-01-13", "2026-01-14", "2026-01-15", "2026-01-16",
            "2026-01-17", "2026-01-18", "2026-01-19"
        ]),
        "Fruit": [
            "Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas",
            "Grapes", "Apples", "Bananas", "Oranges", "Grapes", "Apples",
            "Bananas", "Oranges", "Grapes"
        ],
        "City": [
            "San Francisco", "San Francisco", "San Francisco",
            "New York", "Montreal", "New York",
            "San Francisco", "Montreal", "San Francisco",
            "New York", "Montreal", "San Francisco",
            "Montreal", "San Francisco", "New York"
        ],
        "Units Sold": [120, 85, 210, 150, 95, 180, 130, 110, 190, 105, 140, 160, 175, 115, 125],
        "Unit Price ($)": [2.5, 1.8, 1.2, 2.5, 1.8, 1.2, 3.5, 2.5, 1.2, 1.8, 3.5, 2.5, 1.2, 1.8, 3.5]
    }
    df = pd.DataFrame(data)
    df["Total Revenue ($)"] = df["Units Sold"] * df["Unit Price ($)"]
    return df

df_raw = load_data()

# Sidebar for controls and filtering
st.sidebar.image("https://img.icons8.com/color/96/dashboard--v1.png", width=64)
st.sidebar.title("Dashboard Controls")

# City Filter
cities = ["All"] + list(df_raw["City"].unique())
selected_city = st.sidebar.selectbox("Filter by City", cities)

# Fruit Filter
fruits = ["All"] + list(df_raw["Fruit"].unique())
selected_fruit = st.sidebar.selectbox("Filter by Fruit", fruits)

# Filter Data
filtered_df = df_raw.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]
if selected_fruit != "All":
    filtered_df = filtered_df[filtered_df["Fruit"] == selected_fruit]

# Main Page Header
st.markdown('<div class="main-header">📊 Interactive Data Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Fruit Sales Performance & Market Analytics</div>', unsafe_allow_html=True)

# KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df["Units Sold"].sum()
    st.metric("Total Units Sold", f"{total_sales:,}")

with col2:
    total_revenue = filtered_df["Total Revenue ($)"].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col3:
    avg_price = filtered_df["Unit Price ($)"].mean()
    st.metric("Avg Unit Price", f"${avg_price:.2f}" if not pd.isna(avg_price) else "$0.00")

with col4:
    top_fruit = (
        filtered_df.groupby("Fruit")["Units Sold"].sum().idxmax()
        if not filtered_df.empty else "N/A"
    )
    st.metric("Top Selling Fruit", top_fruit)

st.markdown("---")

# Visualizations Section
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏙️ Sales Volume by City & Fruit")
    if not filtered_df.empty:
        fig_bar = px.bar(
            filtered_df,
            x="City",
            y="Units Sold",
            color="Fruit",
            barmode="group",
            hover_data=["Total Revenue ($)"],
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="City",
            yaxis_title="Units Sold"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with col_right:
    st.subheader("🥧 Market Share by Revenue")
    if not filtered_df.empty:
        revenue_by_fruit = filtered_df.groupby("Fruit")["Total Revenue ($)"].sum().reset_index()
        fig_pie = px.pie(
            revenue_by_fruit,
            names="Fruit",
            values="Total Revenue ($)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Trend Chart
st.subheader("📈 Sales Revenue Trend Over Time")
if not filtered_df.empty:
    trend_df = filtered_df.groupby("Date")["Total Revenue ($)"].sum().reset_index()
    fig_line = px.line(
        trend_df,
        x="Date",
        y="Total Revenue ($)",
        markers=True,
        line_shape="spline"
    )
    fig_line.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Date",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Data Table & Summary Tabs
st.markdown("---")
tab1, tab2 = st.tabs(["📋 Raw Dataset", "📐 Statistical Summary"])

with tab1:
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="fruit_sales_data.csv",
        mime="text/csv"
    )

with tab2:
    st.write(filtered_df.describe())
