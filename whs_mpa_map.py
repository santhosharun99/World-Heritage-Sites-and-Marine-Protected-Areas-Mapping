import geopandas as gpd
import pandas as pd
import xml.etree.ElementTree as ET
import plotly.express as px

# Step 1: Load the MPA shapefile into a GeoDataFrame
# Change the path to where the shapefile is stored on your local machine
shapefile_path = '/path/to/your/MPA_shapefile.shp'  # Replace with your actual file path
mpa_gdf = gpd.read_file(shapefile_path)

# Step 2: Check the CRS (Coordinate Reference System) of the MPA data
# This ensures that the data is in the correct coordinate system (WGS84 - EPSG:4326)
print("MPA CRS:", mpa_gdf.crs)

# If the CRS is not EPSG:4326 (WGS84), reproject to EPSG:4326
if mpa_gdf.crs != "EPSG:4326":
    print("Reprojecting MPA data to EPSG:4326...")
    mpa_gdf = mpa_gdf.to_crs(epsg=4326)

# Step 3: Parse GeoRSS for World Heritage Sites (WHS)
# Function to parse the GeoRSS file and extract the names and coordinates of WHS
def parse_georss(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'ns0': 'http://www.w3.org/2003/01/geo/wgs84_pos#'}
    sites = []

    # Extract site name and coordinates for each WHS
    for item in root.findall('.//item'):
        site_name = item.find('title').text
        lat_elem = item.find('ns0:lat', ns)
        long_elem = item.find('ns0:long', ns)

        # Check if coordinates are available, and if not, skip the site
        if lat_elem is not None and long_elem is not None:
            try:
                latitude = lat_elem.text.strip() if lat_elem is not None else None
                longitude = long_elem.text.strip() if long_elem is not None else None

                if latitude and longitude:
                    latitude = float(latitude)
                    longitude = float(longitude)
                    sites.append({"site_name": site_name, "latitude": latitude, "longitude": longitude})
                else:
                    print(f"Missing coordinates for {site_name}, skipping...")
            except (ValueError, AttributeError):
                print(f"Invalid coordinates for {site_name}, skipping...")
        else:
            print(f"Missing coordinates for {site_name}, skipping...")

    return pd.DataFrame(sites)

# Path to the GeoRSS file containing WHS data (replace with your actual path)
georss_file_path = '/path/to/your/whcgeorss-en.xml'  # Replace with your actual file path
whs_df = parse_georss(georss_file_path)

# Convert World Heritage Sites to GeoDataFrame
whs_gdf = gpd.GeoDataFrame(whs_df, geometry=gpd.points_from_xy(whs_df.longitude, whs_df.latitude))
whs_gdf.set_crs("EPSG:4326", inplace=True)

# Step 4: Filter World Heritage Sites to only include those in the UK
# Set UK bounding box to filter out sites outside of the UK
uk_bounds = [-10, 50, 2, 60]  # Bounding box for UK: min longitude, min latitude, max longitude, max latitude
whs_gdf_uk = whs_gdf.cx[uk_bounds[0]:uk_bounds[2], uk_bounds[1]:uk_bounds[3]]

# Step 5: Create an interactive map with Plotly
# Plot MPAs as polygons on the map
fig = px.choropleth_mapbox(mpa_gdf, geojson=mpa_gdf.geometry, color=mpa_gdf.geometry.apply(lambda x: 1), # Dummy color for MPA polygons
                           locations=mpa_gdf.index, hover_name="SITE_NAME", color_continuous_scale="Blues",
                           mapbox_style="carto-positron", title="Marine Protected Areas (MPA)")

# Add World Heritage Sites (WHS) as points on the map
fig.add_scattermapbox(lat=whs_gdf_uk['latitude'], lon=whs_gdf_uk['longitude'],
                     mode='markers', marker=dict(size=5, color='green'), name="World Heritage Sites (WHS)")

# Step 6: Add nearest MPA names and distances to the map
# Add annotations to show the distance and nearest MPA for each WHS
for _, row in whs_gdf_uk.iterrows():
    fig.add_annotation(
        x=row['longitude'], y=row['latitude'],
        text=f"{row['site_name']}",
        showarrow=True,
        arrowhead=3, ax=0, ay=-40,
        font=dict(size=10, color="black", family="Arial")
    )

# Step 7: Update the layout for the map (center the map on the UK)
fig.update_layout(mapbox_center={"lat": 51.5074, "lon": -0.1278}, mapbox_zoom=6)

# Step 8: Show the interactive plot
try:
    fig.show()
except Exception as e:
    print(f"Error displaying plot: {e}")

# Step 9: Save the map to HTML
fig.write_html("interactive_whs_sac_uk_map_with_counts_and_distances.html")
print("Interactive map saved as 'interactive_whs_sac_uk_map_with_counts_and_distances.html'.")
