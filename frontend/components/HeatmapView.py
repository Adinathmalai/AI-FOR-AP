import streamlit as st
import pydeck as pdk
import pandas as pd

def geospatial_heatmap(data):
    st.subheader("🌍 CDR/IPDR Geospatial Heatmap")

    # Check for lat/lon columns
    lat_cols = [col for col in data.columns if "lat" in col.lower()]
    lon_cols = [col for col in data.columns if "lon" in col.lower()]

    if not lat_cols or not lon_cols:
        st.warning("⚠️ No latitude or longitude columns found in the data.")
        return

    lat_col = lat_cols[0]
    lon_col = lon_cols[0]

    geo_data = data.dropna(subset=[lat_col, lon_col])

    # Basic Map
    st.map(geo_data[[lat_col, lon_col]])

    # Heatmap Layer with pydeck
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=geo_data[lat_col].mean(),
            longitude=geo_data[lon_col].mean(),
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=geo_data,
                get_position=f"[{lon_col}, {lat_col}]",
                aggregation=pdk.types.String("MEAN"),
                threshold=1,
                get_weight=1,
            )
        ],
        tooltip={"text": f"Lat: {{{lat_col}}}\nLon: {{{lon_col}}}"}
    ))
