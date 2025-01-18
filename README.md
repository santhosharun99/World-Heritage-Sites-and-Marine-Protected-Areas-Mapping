# World Heritage Sites and Marine Protected Areas Mapping

This project provides an interactive map of **Marine Protected Areas (MPA)** and **World Heritage Sites (WHS)** within the United Kingdom. It visualizes MPAs and WHS on a map, and displays the **distance** between the nearest MPA and WHS.

## Features

- Load MPA and WHS Data: The data is sourced from shapefiles (for MPAs) and GeoRSS (for WHS).
- Map Visualization: Interactive map that displays MPAs and WHS using Plotly.
- Distance Calculation: Distance between WHS and the nearest MPA is calculated.
- Output: The interactive map is saved as an HTML file.

Data Sources

- UNESCO World Heritage Sites:
    - Data for World Heritage Sites was downloaded from the official UNESCO website: 
    [UNESCO World Heritage Sites Dataset](https://ihp-wins.unesco.org/dataset/unesco-world-heritage-sites)
    
- UK Marine Protected Areas:
    - Marine Protected Areas data for the UK was sourced from the Joint Nature Conservation Committee (JNCC):
    [JNCC Marine Protected Areas Dataset](https://hub.jncc.gov.uk/assets/598a60db-9323-4781-b5a8-dcf0ca3b29f9)

## Requirements

The following Python packages are required to run this project:

- `geopandas`: For geospatial data handling.
- `pandas`: For data manipulation.
- `plotly`: For interactive visualizations.
- `xml.etree.ElementTree`: For parsing GeoRSS files.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/santhosharun99/World-Heritage-Sites-and-Marine-Protected-Areas-Mapping.git
cd whs-mpa-map
