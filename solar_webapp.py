import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="Solar Energy Dashboard ☀️", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("solar_performance_all_seasons.csv")

df = load_data()

# Sidebar
st.sidebar.title("⚙️ Filters")
season = st.sidebar.selectbox("Select Season", df["season"].unique())
month = st.sidebar.selectbox("Select Month", df[df["season"] == season]["month"].unique())

filtered_df = df[(df["season"] == season) & (df["month"] == month)]

# KPIs
st.markdown(f"## 🔋 Solar Panel Dashboard - {season.capitalize()} | {month}")
col1, col2, col3 = st.columns(3)
col1.metric("🔆 Avg Irradiance", f"{filtered_df['irradiance'].mean():.2f} W/m²")
col2.metric("🌡️ Avg Temperature", f"{filtered_df['ambient_temperature'].mean():.1f} °C")
col3.metric("⚡ Avg Energy Output", f"{filtered_df['kwh'].mean():.2f} kWh")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Data", "📈 Charts", "📝 About & Efficiency Tips"])

with tab1:
    st.write("### Filtered Solar Data")
    st.dataframe(filtered_df)

with tab2:
    st.write("### Energy Output Distribution")
    fig = px.histogram(filtered_df, x="kwh", nbins=30, color="month", title="kWh Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Irradiance vs kWh")
    fig2 = px.scatter(filtered_df, x="irradiance", y="kwh", color="month", size="tilt_angle", title="Irradiance vs Energy Output")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("""
    ### 🧠 Project Summary
    This app simulates solar panel energy output using seasonal environmental data. It allows interactive filtering and visualization of performance metrics.

    **Data includes:**
    - Irradiance
    - Humidity
    - Wind Speed
    - Ambient Temperature
    - Tilt Angle
    - kWh Generated

    ⚠️ *Note: Data is synthetically generated for educational/demo purposes.*

    ---

    ### ⚙️ How to Improve Solar Panel Efficiency

    1. **🧽 Keep Panels Clean**  
       Dirt, dust, or bird droppings can block sunlight. Clean every 2–4 weeks.

    2. **📐 Adjust Tilt Properly**  
       Use the right tilt angle based on season and location.  
       _e.g., for India: latitude ± 15°_ depending on the season.

    3. **🌬️ Allow Ventilation**  
       Heat reduces panel efficiency. Ensure airflow to keep them cool.

    4. **⛔ Avoid Shadows**  
       Shade can drop output significantly — even on part of one panel.

    5. **⚡ Use MPPT Controllers**  
       MPPT tech ensures optimal power extraction, especially in changing sunlight.

    6. **📊 Monitor Your System**  
       Use smart trackers to find faults or drops in performance early.

    7. **🔌 Invest in Good Equipment**  
       Cheap wiring, connectors, or inverters = more energy loss.

    ---

    💡 Small actions = Big boosts. Efficiency can jump **5–25%** just by proper care!
    """)
