import folium

def generate_map(df, lat_col='latitude', lon_col='longitude'):
    if df.empty:
        return None
    avg_lat = df[lat_col].mean()
    avg_lon = df[lon_col].mean()
    fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)
    for _, row in df.iterrows():
        folium.Marker([row[lat_col], row[lon_col]], tooltip=row.get('towerID', 'Tower')).add_to(fmap)
    return fmap
