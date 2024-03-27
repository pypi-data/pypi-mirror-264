"""
eageo provides functions for loading shapefile data and constructing folium maps.
"""

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from folium import Choropleth, FeatureGroup, Marker, Icon
from folium.features import GeoJson, GeoJsonTooltip
from importlib.resources import files
from pyeach.extras.loaders import read_txt
import re


def select_geo_data(df, geoid, col, geocol="GEOID", repl="Unknown"):
    """Select the value associated with the geoid and return it as a string if it exists, otherwise returns replacement.

    Args:
        df (pd.DataFrame): Dataframe of descriptive variables linked to geometry.
        geoid (str): ID of geometry to match.
        col (str): Column name of desired data values.
        geocol (str, optional): Column name of geometry IDs. (Defaults to "GEOID")
        repl (str, optional): Replacement for unmatched values. (Defaults to "Unknown")

    Returns:
        str: A string of the value at the geometry ID. 
    """
    try:
        c = str(df[df[geocol]==geoid][col].values[0])
    except IndexError:
        c = repl
    return c


def add_folium_choro(df, col, name, geocol="GEOID", opacity=0.7, colormap="RdBu_r", bins=10):
    """Generate a folium choropleth layer that can be added to an already existing folium map object. The output can be added to a
    folium map object by "add_folium_choro(**kwargs).add_to(FOLIUM_MAP)". More about folium maps can be found here,
    https://python-visualization.github.io/folium/latest/getting_started.html.

    Args:
        df (gpd.GeoDataFrame): GeoPandas Dataframe containing geo location IDs, geometries, and numeric values to determine shape colors.
        col (str): Column name to assign colors from.
        name (str): Name of the folium layer.
        geocol (str, optional): Column name to key on. Geometry must be in the form 'feature.properties.*'. Defaults to "GEOID".
        opacity (float, optional): Color fill opacity. Defaults to 0.7.
        colormap (str, optional): Color scale to use. Defaults to "RdBu_r".
        bins (int, optional): Number of bins to create stepwise gradient. Defaults to 10.

    Returns:
        folilum.Choropleth: Choropleth layer that can added to a folium map.
    """

    geocol_key = f"feature.properties.{geocol}"

    choro = Choropleth(
        name = name,
        geo_data = df,
        data = df,
        columns = [geocol, col],
        key_on=geocol_key,
        legend_name=name,
        fill_opacity=opacity,
        fill_color = colormap,
        bins = bins
    )
    return choro


def add_folium_highlight(df, tooltips):
    """Add highlighting functionality with tooltips to an already existing folium map object. The output can be added to a
    folium map object by "FOLIUM_MAP.add_child(add_folium_highlight(**kwargs))". More about folium maps can be found here,
    https://python-visualization.github.io/folium/latest/getting_started.html.

    Args:
        df (gpd.GeoDataFrame): GeoPandas Dataframe containing geo location IDs, geometries, and numeric values to determine shape colors.
        fields (dict): A dictionary of keys that indicate column names to use as tooltip data, and values that are user friendly descriptions of the columns.

    Returns:
        _type_: _description_
    """

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    fields = list(tooltips.keys()) # extract column names
    aliases = [s + ": " for s in tooltips.values()] # extract and manipulate aliases

    highlight_map = GeoJson(
        df,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=GeoJsonTooltip(
            fields = fields,
            aliases = aliases,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    return highlight_map


def add_folium_markers(name, data, prefix, icon, icon_color, feature_name="Name", lat_name="lat", lon_name="lon"):
    """Add point markers to an already existing folium map object. The output can be added to a
    folium map object by "add_folium_markers(**kwargs).add_to(FOLIUM_MAP)". More about folium maps can be found here,
    https://python-visualization.github.io/folium/latest/getting_started.html.

    Args:
        name (str): Name of the marker(s).
        data (pd.DataFrame): Coordinates DataFrame and location names.
        prefix (str): Prefix for icon.
        icon (str): Icon description.
        icon_color (str): Color of icon.
        feature_name (str, optional): Column name of location names. Defaults to "Name".
        lat_name (str, optional): Column name of latitude values. Defaults to "lat".
        lon_name (str, optional): Column name of longitude values. Defaults to "lon".

    Returns:
        folium.Marker: Marker(s) to add to a folium map.
    """
    markers = FeatureGroup(name = name, overlay = True)
    for i in data.index:
        site = data.loc[i, feature_name]
        lat = float(data.loc[i, lat_name])
        lon = float(data.loc[i, lon_name])

        Marker(
            location=[lat, lon],
            popup=site,
            icon=Icon(prefix=prefix, icon=icon, color = icon_color)
        ).add_to(markers)

    return markers

def map_result(map_df, y, map_size=10):
    """Generate a choropleth map based on a GeoDataFrame.

    Args:
        map_df (gpd.GeoDataFrame): The GeoDataFrame containing geographical data.
        y (str): The column name for the variable to be visualized.
        map_size (int, optional): The size of the resulting map. Defaults to 10.
    """
    map_df = gpd.GeoDataFrame(map_df, crs= {"init": "epsg:4326"}, geometry="geometry")#, crs=4326)
    map_df = map_df.to_crs('EPSG:3857')
    fig, ax = plt.subplots(figsize = (map_size, map_size))
    map_df.plot(
        ax=ax,
        figsize=(5, 5),
        column=y,
        legend=True,
        legend_kwds={'shrink': 0.3},
        alpha=0.75,
    )
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLabels)
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)
    # Remove axis
    ax.set_axis_off()
    ax.set_xlim(map_df.total_bounds[0], map_df.total_bounds[2])
    ax.set_ylim(map_df.total_bounds[1], map_df.total_bounds[3])
    plt.show()

def nc_va_geos(agg):
    """Obtain geo data from pygris for North Carolina (NC) and Virginia (VA).

    Args:
        agg (str): The level of geographical aggregation, options: "tract", "block", "block_groups", "zipcode", "county".

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the combined geographical data for NC and VA.
    """
    if agg=="tract":
        from pygris import tracts as geo_agg
    elif agg=="block":
        from pygris import blocks as geo_agg
    elif agg=="block_groups":
        from pygris import block_groups as geo_agg
    elif agg=="zipcode":
        from pygris import zctas as geo_agg
    elif agg=="county":
        from pygris import counties as geo_agg
    
    try:
        nc = geo_agg(state = "NC")
        va = geo_agg(state = "VA")
    except ValueError as e: # some need to specify year (most recent zipcode geometry from 2010)
        error_ms = str(e)
        years = [int(x) for x in re.findall("\d{4}", error_ms)]
        max_year = max(years)
        nc = geo_agg(state = "NC", year=max_year)
        va = geo_agg(state = "VA", year=max_year)
    
    try:
        nc_va = pd.concat([nc, va]).drop_duplicates(subset=["GEOID"])
    except KeyError:
        for x in ["10", "20"]:
            nc.columns = nc.columns.str.replace(x, "")
            va.columns = va.columns.str.replace(x, "")
        nc_va = pd.concat([nc, va]).drop_duplicates(subset=["GEOID"])

    nc_va["area"] = nc_va.geometry.area

    return nc_va


def locations(group):
    """Get the coordinates of important Cone Health locations. Options include ED/UC departments, hospitals, PCP, 
    aggregate housing, congregational nursing program, community care, and community food locations.

    Args:
        group (str): Indicator for which group of locations to load. Options include ['ed_uc', 'hospitals', 'pcp', 
        'agg_housing', 'cnp', 'comm_care', 'comm_food'].

    Returns:
        pd.DataFrame: DataFrame of location coordinates.
    """

    groups = {"ed_uc": "ed_uc_locations.txt", 
              "hospitals": "hospital_locations.txt", 
              "pcp": "pcp_locations.txt", 
              "agg_housing": "aggregate_housing_locations.txt", 
              "cnp": "cnp_locations.txt",
              "comm_care": "comm_care_locations.txt",
              "comm_food": "comm_food_locations.txt"}
    assert group in groups, f"group must be one of {list(groups.keys())}"
    
    data_text = files("pyeach.data").joinpath(groups[group])
    df = read_txt(data_text)

    return df