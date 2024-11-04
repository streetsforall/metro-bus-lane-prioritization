import geopandas as gpd
import pandas as pd
from collections import defaultdict
import numpy as np
import json
from shapely.ops import unary_union
import pyproj
import pygeoops as pgeo
import geopandas as gpd
import pyproj
from shapely.geometry import LineString, Polygon
import random
import matplotlib.pyplot as plt

path_pref = "/Users/joeyshoyer/Downloads/"

# Load the stops.geojson manually
with open(path_pref + "stops.geojson") as f:
    stops_data = json.load(f)

# Manually extract stop_id, stop_name, route_ids, and coordinates
stops_list = []
for feature in stops_data['features']:
    stop_id = int(feature['properties'].get('stop_id'))
    stop_name = feature['properties'].get('stop_name')
    route_ids = feature['properties'].get('route_ids')
    
    stops_list.append({
        'stop_id': stop_id,
        'stop_name': stop_name,
        'route_ids': route_ids,
    })

# Convert to DataFrame if needed
stops_df = pd.DataFrame(stops_list)

# Inspect the DataFrame
print(stops_df)

# Define the function to handle conversion for a single route_id
def safe_convert(route_id):
    try:
        return int(route_id.split('-')[0])
    except (ValueError, AttributeError):
        return np.nan

# Function to apply conversion to each item in the list
def convert_route_ids(route_ids):
    if isinstance(route_ids, list):
        return [safe_convert(route_id) for route_id in route_ids]
    return route_ids

stops_df['route_ids'] = stops_df['route_ids'].apply(convert_route_ids)

# Create a dictionary to map stop_id to route_ids
stop_to_routes = stops_df.set_index('stop_id')['route_ids'].to_dict()

ridership_data = gpd.read_file(path_pref + "Average_weekday_ridership.geojson")

# Load the GeoJSON files
variance_gdf = gpd.read_file(path_pref + "182_Midday_variance.geojson")
midday_gdf = gpd.read_file(path_pref + "182_Midday_speeds.geojson")
pm_peak_gdf = gpd.read_file(path_pref + "182_PM_Peak_speeds.geojson")
am_peak_gdf = gpd.read_file(path_pref + "182_AM_Peak_speeds.geojson")
# Remove rows with missing or None values in stop_id or route_id for each GeoDataFrame
variance_gdf = variance_gdf.dropna(subset=['stop_id', 'route_id'])
midday_gdf = midday_gdf.dropna(subset=['stop_id', 'route_id'])
pm_peak_gdf = pm_peak_gdf.dropna(subset=['stop_id', 'route_id'])
am_peak_gdf = am_peak_gdf.dropna(subset=['stop_id', 'route_id'])
# Create the new column in each GeoDataFrame
variance_gdf['stop_route_id'] = variance_gdf['stop_id'].astype(str) + '_' + variance_gdf['route_id'].astype(str)
midday_gdf['stop_route_id'] = midday_gdf['stop_id'].astype(str) + '_' + midday_gdf['route_id'].astype(str)
pm_peak_gdf['stop_route_id'] = pm_peak_gdf['stop_id'].astype(str) + '_' + pm_peak_gdf['route_id'].astype(str)
am_peak_gdf['stop_route_id'] = am_peak_gdf['stop_id'].astype(str) + '_' + am_peak_gdf['route_id'].astype(str)
# Create the new column in each GeoDataFrame
midday_gdf['stop_route_dir_id'] = midday_gdf['stop_id'].astype(str) + '_' + midday_gdf['route_id'].astype(str) + '_' + midday_gdf['direction_id'].astype(str)
pm_peak_gdf['stop_route_dir_id'] = pm_peak_gdf['stop_id'].astype(str) + '_' + pm_peak_gdf['route_id'].astype(str) + '_' + pm_peak_gdf['direction_id'].astype(str)
am_peak_gdf['stop_route_dir_id'] = am_peak_gdf['stop_id'].astype(str) + '_' + am_peak_gdf['route_id'].astype(str) + '_' + am_peak_gdf['direction_id'].astype(str)
variance_gdf = variance_gdf.drop(columns=["geometry", 'id', 'shape_id', 'stop_sequence', 'fast_slow_ratio', 'trips_per_hour', 'miles_from_last', 'route_short_name', 'route_id', 'stop_name', 'stop_id'])
midday_gdf = midday_gdf.drop(columns=['id', 'shape_id', 'fast_slow_ratio', 'trips_per_hour', 'time_formatted', 'organization_name', 'p20_mph', 'p80_mph'])
pm_peak_gdf = pm_peak_gdf.drop(columns=["geometry", 'id', 'shape_id', 'stop_sequence', 'direction_id', 'fast_slow_ratio', 'trips_per_hour', 'miles_from_last', 'time_formatted', 'organization_name', 'route_short_name', 'route_id', 'stop_name', 'p20_mph', 'p80_mph', 'stop_id'])
am_peak_gdf = am_peak_gdf.drop(columns=["geometry", 'id', 'shape_id', 'stop_sequence', 'direction_id', 'fast_slow_ratio', 'trips_per_hour', 'miles_from_last', 'time_formatted', 'organization_name', 'route_short_name', 'route_id', 'stop_name', 'p20_mph', 'p80_mph', 'stop_id'])

# Check for duplicates in pm_peak_gdf
midday_gdf.drop_duplicates(subset=['stop_route_dir_id'], keep='first', inplace=True)
pm_peak_gdf.drop_duplicates(subset=['stop_route_dir_id'], keep='first', inplace=True)
am_peak_gdf.drop_duplicates(subset=['stop_route_dir_id'], keep='first', inplace=True)
variance_gdf.drop_duplicates(subset=['stop_route_id'], keep='first', inplace=True)

# Merge on stop_name
merged_gdf = midday_gdf.merge(pm_peak_gdf, on="stop_route_dir_id", how="inner", suffixes=('_midday', '_pm'))
merged_gdf = merged_gdf.merge(am_peak_gdf, on="stop_route_dir_id", how="inner", suffixes=('', '_am'))
merged_gdf = merged_gdf.rename(columns={'p50_mph': 'p50_mph_am'})
variance_gdf = variance_gdf.rename(columns={'p20_mph': 'p20_mph_var', 'p80_mph': 'p80_mph_var'})
merged_gdf = merged_gdf.merge(variance_gdf, on="stop_route_id", how="inner", suffixes=('', '_var'))
merged_gdf = merged_gdf.drop(columns=['stop_route_id_midday', 'stop_route_id_pm'])

# Calculate the mean of each p50_mph column
mean_midday = merged_gdf['p50_mph_midday'].mean()
mean_pm = merged_gdf['p50_mph_pm'].mean()
mean_am = merged_gdf['p50_mph_am'].mean()


print(mean_midday, mean_pm, mean_am)

# Calculate the difference from the average for each p50_mph column
# merged_gdf['diff_from_avg_midday'] = mean_midday - merged_gdf['p50_mph_midday']
# merged_gdf['diff_from_avg_pm'] = mean_pm - merged_gdf['p50_mph_pm']
# merged_gdf['diff_from_avg_am'] = mean_am - merged_gdf['p50_mph_am']

merged_gdf['diff_from_avg_midday'] = merged_gdf['p80_mph_var'] - merged_gdf['p50_mph_midday']
merged_gdf['diff_from_avg_pm'] = merged_gdf['p80_mph_var'] - merged_gdf['p50_mph_pm']
merged_gdf['diff_from_avg_am'] = merged_gdf['p80_mph_var'] - merged_gdf['p50_mph_am']

json_df = pd.read_json(path_pref + "ridership.json")
json_df['line_name'] = json_df['line_name'].astype(str)
json_df.head()

# Step 1: Sort by line_name, year, and month in descending order
json_df_sorted = json_df.sort_values(by=['line_name', 'year', 'month'], ascending=[True, False, False])

# Step 2: Drop duplicates based on line_name, keeping the first (most recent) record
json_df_most_recent = json_df_sorted.drop_duplicates(subset='line_name', keep='first')

# Step 3: Inspect the result
print(json_df_most_recent)

json_df_most_recent.info()
json_df_most_recent.sort_values(by='est_wkday_ridership', ascending=False).head(30)
json_df_most_recent = json_df_most_recent.drop(columns=['est_sat_ridership', 'est_sun_ridership', 'year', 'month'])

merged_gdf = merged_gdf.merge(json_df_most_recent, left_on='route_short_name', right_on='line_name', how='left')


# Initialize a dictionary to store boardings for each route at each stop_id
boardings_per_route_stop = defaultdict(lambda: defaultdict(float))

# Ensure line_name is now of int type
json_df_most_recent['line_name'] = json_df_most_recent['line_name'].astype(int)


# Get total ridership per route from json_df_most_recent
total_ridership_per_route = json_df_most_recent.set_index('line_name')['est_wkday_ridership'].to_dict()

# Iterate over the ridership GeoDataFrame
for _, row in ridership_data.iterrows():
    stop_id = row['STOP_ID']
    ons = row['Ons']

    # Get routes serving this stop
    if stop_id in stop_to_routes:
        routes = stop_to_routes[stop_id]
        print(routes)
        
        # Calculate total ridership for normalization
        total_ridership = sum(total_ridership_per_route.get(route, 0) for route in routes)

        # Distribute boardings across routes proportionally
        for route in routes:
            route_ridership = total_ridership_per_route.get(route, 0)
            if total_ridership > 0:
                boarding_per_route = ons * (route_ridership / total_ridership)
                boardings_per_route_stop[stop_id][route] += boarding_per_route


# Load the average trip lengths from Excel
trip_length_df = pd.read_excel(path_pref + "Ridership Report - Monthly Line Level (NTD).xlsx")
trip_length_df

# Drop columns other than 'Year', 'Month No', 'Line', and 'Avg Trip Length'
trip_length_df = trip_length_df[['Year', 'Month No', 'Line', 'Avg Trip Length']]

# Filter for the year 2023
trip_length_df_2023 = trip_length_df[trip_length_df['Year'] == 2023]

# Group by 'Line' and average the 'Avg Trip Length'
average_trip_length = trip_length_df_2023.groupby('Line')['Avg Trip Length'].mean().to_dict()

# Ensure route_short_name is treated as a string for initial checks
merged_gdf['route_short_name'] = merged_gdf['route_short_name'].astype(str)

# Extract numeric part of route_short_name if needed
# For this example, let's assume route_short_name has a numeric part that we want to convert
# If route_short_name is already numeric, you can skip this step
merged_gdf['route_short_name_numeric'] = merged_gdf['route_short_name'].str.extract('(\d+)').astype(float)

# Convert to integer, handling any potential issues
merged_gdf['route_short_name_numeric'] = merged_gdf['route_short_name_numeric'].fillna(0).astype(int)

merged_gdf['Avg Trip Length'] = merged_gdf['route_short_name_numeric'].map(average_trip_length)

def simulate_single_route(merged_gdf, boardings_per_route_stop, test_route, test_direction):
    
    test_route = int(test_route)

    # Filter the dataframe for the specific route and direction
    route_gdf = merged_gdf[
        (merged_gdf['route_short_name'] == str(test_route)) & 
        (merged_gdf['direction_id'] == test_direction)
    ].sort_values('stop_sequence')

    # Create a dictionary to store segment ridership
    segment_ridership = defaultdict(float)
    
    # Initialize riders on the bus
    riders_on_bus = 0
    # Keep track of where each rider boarded and the distance they’ve traveled
    rider_origins = []
    rider_distances = []
    
    print(f"\nSimulating route {test_route}, direction {test_direction}")
    
    cumulative_distance = 0  # Track cumulative distance for each stop
    
    for _, row in route_gdf.iterrows():
        stop_id = int(row['stop_id'])
        segment_length = row['miles_from_last']
        cumulative_distance += segment_length  # Update cumulative distance
        stop_route_dir_id = row['stop_route_dir_id']
        
        # Simulate riders getting off
        avg_trip_length = row['Avg Trip Length']  # Default to 5 miles if not found
        riders_getting_off = 0
        
        #print(f"Stop {stop_id} Segment Length: {segment_length}")  # Debugging segment length
        
        if avg_trip_length > 0:
            riders_getting_off = sum(1 for dist in rider_distances if dist >= avg_trip_length)
            riders_on_bus -= riders_getting_off
            #print(f"Riders getting off at stop {stop_id}: {riders_getting_off}")  # Debugging riders getting off
            # Remove riders who got off and update distances for remaining riders
            rider_origins = [origin for origin, dist in zip(rider_origins, rider_distances) if dist < avg_trip_length]
            rider_distances = [dist for dist in rider_distances if dist < avg_trip_length]
        
        # Simulate riders getting on
        riders_getting_on = 0
        if stop_id in boardings_per_route_stop and test_route in boardings_per_route_stop[stop_id]:
            riders_getting_on = boardings_per_route_stop[stop_id][test_route]
            riders_on_bus += riders_getting_on
            #print(f"Riders getting on at stop {stop_id}: {riders_getting_on}")  # Debugging riders getting on
            # Add these riders’ starting distances (i.e., zero since they’re boarding now)
            rider_origins.extend([row['stop_sequence']] * int(riders_getting_on))
            rider_distances.extend([0] * int(riders_getting_on))
        
        # Update distances traveled for remaining riders
        rider_distances = [dist + segment_length for dist in rider_distances]
        
        # Store the ridership for this segment (riders on bus * segment length)
        segment_ridership[stop_route_dir_id] = riders_on_bus
        #print(f"Riders on bus after stop {stop_id}: {riders_on_bus}")  # Debugging riders on bus

    return segment_ridership

# Specify the route and direction you want to test
test_route = '4'  # Replace with the route number you want to test
test_direction = 1  # Specify the direction you want to test (e.g., 0 or 1)

# Run the simulation for the single route and direction
segment_ridership_182 = simulate_single_route(merged_gdf, boardings_per_route_stop, test_route, test_direction)

def simulate_all_routes(merged_gdf, boardings_per_route_stop):
    all_segment_ridership = {}
    
    # Get unique combinations of route_short_name and direction_id
    route_directions = merged_gdf[['route_short_name_numeric', 'direction_id']].drop_duplicates()
    
    for _, row in route_directions.iterrows():
        route = row['route_short_name_numeric']
        direction = row['direction_id']
        
        print(f"Simulating route {route}, direction {direction}")
        segment_ridership = simulate_single_route(merged_gdf, boardings_per_route_stop, route, direction)
        all_segment_ridership.update(segment_ridership)
    
    return all_segment_ridership

# Run the simulation for all routes and directions
all_routes_ridership = simulate_all_routes(merged_gdf, boardings_per_route_stop)

merged_gdf['simulated_segment_ridership'] = merged_gdf['stop_route_dir_id'].map(all_routes_ridership)
