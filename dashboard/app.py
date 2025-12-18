import os
import re
import math
import pandas as pd
import streamlit as st
import plotly.express as px

import folium
from streamlit_folium import st_folium


# ----------------------------
# Helper functions
# ----------------------------

def find_dataset_pairs(datasets_dir: str):
    """
    Look inside the datasets folder and find matching pairs like:
    stores1.csv + customers1.csv, stores2.csv + customers2.csv, ...
    so we can switch datasets from the dashboard easily.
    """
    stores = {}
    customers = {}

    # if folder doesn't exist, just return empty and stop later
    if not os.path.exists(datasets_dir):
        return []

    for f in os.listdir(datasets_dir):
        # match filenames like stores46.csv / customers46.csv
        m1 = re.match(r"stores(\d+)\.csv$", f)
        m2 = re.match(r"customers(\d+)\.csv$", f)
        if m1:
            k = int(m1.group(1))
            stores[k] = os.path.join(datasets_dir, f)
        if m2:
            k = int(m2.group(1))
            customers[k] = os.path.join(datasets_dir, f)

    # only keep dataset numbers that exist in BOTH files
    ks = sorted(set(stores.keys()) & set(customers.keys()))
    return [(k, stores[k], customers[k]) for k in ks]


def haversine_km(lon1, lat1, lon2, lat2):
    # distance between 2 points on earth using lat/lon (in KM)
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def normalize(series):
    # normalize values to [0,1] so different features can be combined in one score
    # if all values are same, just return 0.5 for everyone (so it doesn't break)
    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())


# ----------------------------
# Streamlit page setup
# ----------------------------
st.set_page_config(page_title="Food Waste App - Admin Dashboard", layout="wide")

st.title("Food Waste App - Admin Analytics Dashboard")
st.caption(
    "This dashboard is mainly for analysis: food-waste potential (bags available) + customer satisfaction "
    "(ratings + customer valuations), and how recommendations change when we change priorities."
)

# project root is wherever i run streamlit from (should be the repo root)
project_root = os.getcwd()
datasets_dir = os.path.join(project_root, "datasets")

pairs = find_dataset_pairs(datasets_dir)

# if no dataset files exist, stop early
if not pairs:
    st.error("I couldn’t find datasets. Make sure you have: datasets/storesX.csv and datasets/customersX.csv")
    st.stop()


# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Dataset")

# build labels like: Dataset 46 (stores46.csv + customers46.csv)
pair_labels = [f"Dataset {k} (stores{k}.csv + customers{k}.csv)" for (k, _, _) in pairs]
choice = st.sidebar.selectbox("Choose dataset", pair_labels, index=len(pair_labels) - 1)

chosen_idx = pair_labels.index(choice)
k, stores_path, customers_path = pairs[chosen_idx]

st.sidebar.markdown("---")
st.sidebar.header("Recommendation priorities (weights)")

# top N stores to display in recommendation output
top_n = st.sidebar.slider("Top-N recommended stores", 3, 15, 10)

# weights for each part of the scoring function (i can tune these to see how rankings change)
w_rating = st.sidebar.slider("Weight: overall satisfaction (store rating)", 0.0, 1.0, 0.30, 0.05)
w_price  = st.sidebar.slider("Weight: affordability (lower price)", 0.0, 1.0, 0.20, 0.05)
w_value  = st.sidebar.slider("Weight: personalized satisfaction (customer valuation)", 0.0, 1.0, 0.25, 0.05)
w_bags   = st.sidebar.slider("Weight: waste reduction (more bags rescued)", 0.0, 1.0, 0.20, 0.05)
w_dist   = st.sidebar.slider("Weight: accessibility (closer distance)", 0.0, 1.0, 0.05, 0.05)

# quick reminder for myself what bags@9AM means
st.sidebar.markdown("---")
st.sidebar.info(
    "Note:\n"
    "- bags @9AM means food that is available early (so if no one claims it, it can be wasted)\n"
    "- higher bags = higher waste potential, but also higher chance to rescue more food"
)


# ----------------------------
# Load data
# ----------------------------
# read the chosen stores/customers CSV
stores = pd.read_csv(stores_path)
customers = pd.read_csv(customers_path)

# make sure lat/lon are numeric, if something is wrong it becomes NaN
for col in ["longitude", "latitude"]:
    stores[col] = pd.to_numeric(stores[col], errors="coerce")
    customers[col] = pd.to_numeric(customers[col], errors="coerce")

# convert important columns to numeric (sometimes they can be strings in CSV)
stores["average_overall_rating"] = pd.to_numeric(stores["average_overall_rating"], errors="coerce")
stores["price"] = pd.to_numeric(stores["price"], errors="coerce")
stores["average_bags_at_9AM"] = pd.to_numeric(stores["average_bags_at_9AM"], errors="coerce")


# ----------------------------
# KPI Row (quick summary at the top)
# ----------------------------
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Stores", f"{stores.shape[0]:,}")
k2.metric("Customers", f"{customers.shape[0]:,}")
k3.metric("Avg satisfaction (rating)", f"{stores['average_overall_rating'].mean():.2f}")
k4.metric("Avg price", f"{stores['price'].mean():.2f}")
k5.metric("Potential wasted food (bags @9AM)", f"{stores['average_bags_at_9AM'].sum():,.0f}")

st.markdown("---")


# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "Map", "Recommendation Explorer"])


# ----------------------------
# Overview tab
# ----------------------------
with tab1:
    st.subheader("Customer satisfaction overview (store ratings)")
    c1, c2 = st.columns([1, 1])

    with c1:
        # show the top 10 stores by rating (overall satisfaction)
        top = stores.sort_values("average_overall_rating", ascending=False).head(10)
        fig = px.bar(
            top,
            x="store_name",
            y="average_overall_rating",
            hover_data=["branch", "price", "average_bags_at_9AM"],
            title="Top 10 stores by customer satisfaction (rating)",
            labels={"average_overall_rating": "Satisfaction (rating)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # price distribution (just to see if prices are spread out or weird)
        fig = px.histogram(
            stores,
            x="price",
            nbins=20,
            title="Price distribution",
            labels={"price": "Price"}
        )
        st.plotly_chart(fig, use_container_width=True)

    # bubble chart: price vs rating, bubble size shows bags (waste potential)
    st.subheader("Waste potential vs price vs satisfaction (bubble size = potential wasted food)")
    fig = px.scatter(
        stores,
        x="price",
        y="average_overall_rating",
        size="average_bags_at_9AM",
        hover_data=["store_name", "branch"],
        title="Tradeoff: affordability vs satisfaction (size shows food waste potential)",
        labels={
            "price": "Price",
            "average_overall_rating": "Satisfaction (rating)",
            "average_bags_at_9AM": "Potential wasted food (bags @9AM)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # top waste potential stores (highest bags @ 9AM)
    st.subheader("Stores with highest food waste potential (bags @9AM)")
    top_waste = stores.sort_values("average_bags_at_9AM", ascending=False).head(10)
    fig = px.bar(
        top_waste,
        x="store_name",
        y="average_bags_at_9AM",
        title="Top 10 stores by potential wasted food",
        labels={"average_bags_at_9AM": "Potential wasted food (bags @9AM)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # tradeoff plot: satisfaction vs waste potential
    st.subheader("Trade-off: customer satisfaction vs food waste potential")
    fig = px.scatter(
        stores,
        x="average_bags_at_9AM",
        y="average_overall_rating",
        size="price",
        hover_data=["store_name", "branch"],
        title="Do high-waste stores also have high customer satisfaction?",
        labels={
            "average_bags_at_9AM": "Potential wasted food (bags @9AM)",
            "average_overall_rating": "Satisfaction (rating)",
            "price": "Price"
        }
    )
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Map tab
# ----------------------------
with tab2:
    st.subheader("Geographic map: stores + optional customers sample")

    # this map is just to visualize where stores are located and why distance matters
    st.write(
        "The map shows store locations and why accessibility (distance) affects recommendations. "
        "You can also show a sample of customers to see clustering."
    )

    show_customers = st.checkbox("Show a random sample of customers (100)", value=False)

    # center the map around the average store location
    center_lat = float(stores["latitude"].mean())
    center_lon = float(stores["longitude"].mean())
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # add store markers (bigger circles)
    for _, row in stores.dropna(subset=["latitude", "longitude"]).iterrows():
        popup = (
            f"<b>{row.get('store_name','')}</b><br>"
            f"Branch: {row.get('branch','')}<br>"
            f"Satisfaction (rating): {row.get('average_overall_rating','')}<br>"
            f"Price: {row.get('price','')}<br>"
            f"Potential wasted food (bags @9AM): {row.get('average_bags_at_9AM','')}"
        )
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            popup=popup
        ).add_to(m)

    # optional: add customer sample markers (small circles)
    if show_customers:
        sample = customers.dropna(subset=["latitude", "longitude"]).sample(min(100, len(customers)), random_state=7)
        for _, row in sample.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=2
            ).add_to(m)

    st_folium(m, width=1100, height=600)


# ----------------------------
# Recommendation Explorer tab
# ----------------------------
with tab3:
    st.subheader("Pick a customer and see recommendations")

    # explain what the score is doing (for the reader/TA)
    st.write(
        "Recommendations balance customer satisfaction (ratings + customer valuation), "
        "affordability, food waste reduction (bags @9AM), and accessibility (distance)."
    )

    customer_ids = customers["customer_id"].tolist()
    cust_id = st.selectbox("Customer ID", customer_ids, index=0)

    # get that customer's row and location
    cust_row = customers[customers["customer_id"] == cust_id].iloc[0]
    clat, clon = float(cust_row["latitude"]), float(cust_row["longitude"])

    # build a dictionary: store_id -> valuation for this customer
    # columns look like store100_valuation, store200_valuation, etc.
    valuation_map = {}
    for col in customers.columns:
        m = re.match(r"store(\d+)_valuation$", col)
        if m:
            sid = int(m.group(1))
            valuation_map[sid] = float(cust_row[col])

    # copy stores and compute distance + valuation
    tmp = stores.copy()
    tmp["dist_km"] = tmp.apply(lambda r: haversine_km(clon, clat, r["longitude"], r["latitude"]), axis=1)
    tmp["valuation"] = tmp["store_id"].apply(lambda sid: valuation_map.get(int(sid), 0.0))

    # normalize features so i can combine them (higher = better)
    tmp["n_rating"] = normalize(tmp["average_overall_rating"].fillna(0.0))
    tmp["n_value"]  = normalize(tmp["valuation"].fillna(0.0))
    tmp["n_bags"]   = normalize(tmp["average_bags_at_9AM"].fillna(0.0))

    # for price and distance: lower is better, so we normalize then invert
    tmp["n_price"] = 1.0 - normalize(tmp["price"].fillna(tmp["price"].median()))
    tmp["n_dist"]  = 1.0 - normalize(tmp["dist_km"].fillna(tmp["dist_km"].median()))

    # final weighted score (based on the sidebar weights)
    tmp["score"] = (
        w_rating * tmp["n_rating"] +
        w_price  * tmp["n_price"] +
        w_value  * tmp["n_value"] +
        w_bags   * tmp["n_bags"] +
        w_dist   * tmp["n_dist"]
    )

    # take top N
    ranked = tmp.sort_values("score", ascending=False).head(top_n)

    st.write("Recommended stores (with satisfaction + waste info)")

    # show table in a readable way
    st.dataframe(
        ranked[[
            "store_id", "store_name", "branch",
            "average_overall_rating", "valuation",
            "price", "average_bags_at_9AM",
            "dist_km", "score"
        ]].rename(columns={
            "average_overall_rating": "Satisfaction (rating)",
            "valuation": "Personalized satisfaction (valuation)",
            "price": "Price",
            "average_bags_at_9AM": "Potential wasted food (bags @9AM)",
            "dist_km": "Distance (km)",
            "score": "Final score"
        }).reset_index(drop=True)
    )

    # show the selected customer + recommended stores on map
    st.write("Customer + recommended stores on a map")
    m2 = folium.Map(location=[clat, clon], zoom_start=12)

    folium.Marker(
        location=[clat, clon],
        popup=f"Customer {cust_id}",
        icon=folium.Icon()
    ).add_to(m2)

    for _, row in ranked.dropna(subset=["latitude", "longitude"]).iterrows():
        popup = (
            f"<b>{row.get('store_name','')}</b><br>"
            f"Score: {row.get('score',0):.3f}<br>"
            f"Satisfaction (rating): {row.get('average_overall_rating',0):.2f}<br>"
            f"Personalized valuation: {row.get('valuation',0):.1f}<br>"
            f"Potential wasted food (bags @9AM): {row.get('average_bags_at_9AM',0):.0f}<br>"
            f"Distance (km): {row.get('dist_km',0):.2f}"
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup
        ).add_to(m2)

    st_folium(m2, width=1100, height=550)
