
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    providers = pd.read_csv(DATA_DIR / "cleaned_providers.csv")
    receivers = pd.read_csv(DATA_DIR / "cleaned_receivers.csv")
    food = pd.read_csv(DATA_DIR / "cleaned_food_listings.csv", parse_dates=["Expiry_Date"])
    claims = pd.read_csv(DATA_DIR / "cleaned_claims.csv", parse_dates=["Timestamp"])
    return providers, receivers, food, claims

def main():
    st.title("Local Food Wastage Management — Dashboard")
    st.caption("Clean data → insights → action")

    # Try load data
    try:
        providers, receivers, food, claims = load_data()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        st.stop()

    # --- Filters
    with st.sidebar:
        st.header("Filters")
        city = st.multiselect("City / Location", sorted(food["Location"].dropna().unique().tolist()))
        meal = st.multiselect("Meal Type", sorted(food["Meal_Type"].dropna().unique().tolist()))
        ftype = st.multiselect("Food Type", sorted(food["Food_Type"].dropna().unique().tolist()))
        status = st.multiselect("Claim Status", sorted(claims["Status"].dropna().unique().tolist()))

    f = food.copy()
    if city: f = f[f["Location"].isin(city)]
    if meal: f = f[f["Meal_Type"].isin(meal)]
    if ftype: f = f[f["Food_Type"].isin(ftype)]

    c = claims.copy()
    if status: c = c[c["Status"].isin(status)]

    # --- KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Food Listings", int(len(f)))
    with col2:
        exp_today = int((f["Expiry_Date"].dt.date == pd.Timestamp("today").date()).sum())
        st.metric("Expiring Today", exp_today)
    with col3:
        completed_rate = 0.0
        if len(c) > 0:
            completed_rate = (c["Status"].eq("Completed").mean()) * 100
        st.metric("Claims Completed (%)", f"{completed_rate:.1f}%")
    with col4:
        unique_providers = int(f["Provider_ID"].nunique())
        st.metric("Active Providers", unique_providers)

    st.divider()

    # --- Charts (built-in Altair via st.bar_chart for simplicity)
    # City-wise listings
    city_counts = f.groupby("Location")["Food_ID"].nunique().sort_values(ascending=False)
    st.subheader("Listings by City")
    st.bar_chart(city_counts)

    # Meal type distribution
    meal_counts = f.groupby("Meal_Type")["Food_ID"].nunique().sort_values(ascending=False)
    st.subheader("Listings by Meal Type")
    st.bar_chart(meal_counts)

    # Food type distribution
    ftype_counts = f.groupby("Food_Type")["Food_ID"].nunique().sort_values(ascending=False)
    st.subheader("Listings by Food Type")
    st.bar_chart(ftype_counts)

    st.divider()

    # --- Tables
    with st.expander("Food Listings (filtered)"):
        st.dataframe(f.sort_values(["Expiry_Date","Location","Meal_Type"]), use_container_width=True)
    with st.expander("Claims (filtered)"):
        st.dataframe(c.sort_values("Timestamp", ascending=False), use_container_width=True)
    with st.expander("Providers"):
        st.dataframe(providers, use_container_width=True)
    with st.expander("Receivers"):
        st.dataframe(receivers, use_container_width=True)

    st.divider()
    st.caption("Tip: Use sidebar filters to segment by city, meal type, food type, and claim status.")

if __name__ == "__main__":
    main()
