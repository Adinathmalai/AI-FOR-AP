# frontend/components/MapView.py
import streamlit as st
import pandas as pd
import re
import numpy as np

# Try to import geopy, show error if missing
try:
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
except ImportError:
    st.error("Geopy library not installed. Please run `pip install geopy` in your terminal and restart the app.")
    st.stop()

import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Initialize geocoder with rate limiting
geolocator = Nominatim(user_agent="geoapi_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def map_view(data):
    """Smart map viewer that pins locations with distinct icons"""
    if not data:
        return
    
    def detect_geo_columns(df):
        """Finds latitude/longitude columns using name patterns"""
        lat_pattern = r'lat(?:itude)?'
        lon_pattern = r'lon(?:gitude)?'
        lat_cols = [col for col in df.columns if re.search(lat_pattern, col, re.IGNORECASE)]
        lon_cols = [col for col in df.columns if re.search(lon_pattern, col, re.IGNORECASE)]
        return (lat_cols[0] if lat_cols else None, lon_cols[0] if lon_cols else None)
    
    def detect_city_column(df):
        """Finds columns that likely contain city names"""
        city_patterns = [r'city', r'location', r'place', r'town', r'address']
        for col in df.columns:
            col_lower = col.lower()
            if any(re.search(pattern, col_lower) for pattern in city_patterns):
                return col
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                return col
        return None
    
    def geocode_cities(df, city_column):
        """Convert city names to coordinates"""
        df = df.copy()
        df['latitude'] = np.nan
        df['longitude'] = np.nan
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(df)
        
        for idx, row in enumerate(df.itertuples(), 1):
            try:
                location = geocode(getattr(row, city_column))
                if location:
                    df.at[row.Index, 'latitude'] = location.latitude
                    df.at[row.Index, 'longitude'] = location.longitude
            except Exception:
                continue
            
            # Update progress
            progress = int((idx / total) * 100)
            progress_bar.progress(progress)
            status_text.text(f"Geocoding {idx}/{total} cities...")
        
        progress_bar.empty()
        status_text.empty()
        return df.dropna(subset=['latitude', 'longitude'])
    
    def create_map_with_pins(df, title):
        """Create folium map with distinct pin icons for each location"""
        lat_col, lon_col = detect_geo_columns(df)
        used_geocoding = False
        
        # If no geo columns, try geocoding cities
        if not lat_col or not lon_col:
            city_col = detect_city_column(df)
            if city_col:
                df = geocode_cities(df, city_col)
                lat_col, lon_col = 'latitude', 'longitude'
                used_geocoding = True
            else:
                st.warning(f"No geo columns or city names found in {title}")
                return False
        
        if lat_col and lon_col:
            try:
                if df.empty:
                    st.warning(f"No locations to map in {title}")
                    return False
                
                # Create map centered on first location
                first_location = [df.iloc[0][lat_col], df.iloc[0][lon_col]]
                m = folium.Map(location=first_location, zoom_start=5)
                marker_cluster = MarkerCluster().add_to(m)
                
                # Define distinct pin colors
                colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
                         'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']
                
                # Add pins for each location
                for idx, row in df.iterrows():
                    color = colors[idx % len(colors)]
                    location = [row[lat_col], row[lon_col]]
                    
                    # Get city name for popup
                    city_name = None
                    for col in df.columns:
                        if re.search(r'city|location|place|town|address', col, re.IGNORECASE):
                            city_name = row[col]
                            break
                    if not city_name:
                        city_name = f"Location {idx+1}"
                    
                    folium.Marker(
                        location=location,
                        popup=city_name,
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(marker_cluster)
                
                # Display map
                st.subheader(f"📍 Map for {title}")
                st_folium(m, width=700, height=500)
                
                # Show data table
                with st.expander(f"📊 View Location Data for {title}"):
                    st.dataframe(df)
                
                return True
            except Exception as e:
                st.error(f"Mapping error: {str(e)}")
        return False
    
    maps_displayed = 0
    
    # Handle multiple files
    if isinstance(data, list):
        for file in data:
            if isinstance(file, dict) and file.get('content', {}).get('type') == 'dataframe':
                df = file['content']['data']
                if create_map_with_pins(df, file['name']):
                    maps_displayed += 1
    
    # Handle single DataFrame
    elif isinstance(data, pd.DataFrame):
        if create_map_with_pins(data, "Geospatial Data"):
            maps_displayed += 1
    
    if maps_displayed == 0:
        st.warning("""
        No mappable data found. Files need either:
        - Latitude/Longitude columns (names containing 'lat'/'lon')
        - City names or addresses in a text column
        """)
