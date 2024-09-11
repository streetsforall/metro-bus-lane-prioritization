# Bus Route Performance Analysis

## Data Sources

1. Bus Speed Data:
   - `182_Midday_variance.geojson`
   - `182_Midday_speeds.geojson`
   - `182_PM_Peak_speeds.geojson`
   - `182_AM_Peak_speeds.geojson`

[source](https://rt--cal-itp-data-analyses.netlify.app/district_07-los-angeles/18__speedmaps__district_07-los-angeles__itp_id_182)

2. Line-level Ridership Data:
   - `ridership.json`

3. Stops
 - `stops.geojson`

4. Stop-level boardings
 - `Average_weekday_ridership.geojson`

5. Average length of trip per bus route
 - `Ridership Report - Monthly Line Level (NTD).xlsx`

## Overview

This project analyzes bus route performance in terms of speed and passenger time lost. It combines speed data from different times of day (AM peak, midday, PM peak) with ridership information to calculate metrics such as:

- Passenger hours wasted
- Passenger hours wasted per mile traveled
- Total ridership hours lost per route
- Performance comparisons across different time periods

The analysis identifies routes and segments with the highest impact on passenger travel times, providing insights for potential service improvements.

### Stop-level Ridership Simulation

To generate stop level ridership for each bus route, we approximate using the following process:

 - Use the stop-level boardings and add those boardings to the line at each stop in sequence
   - For stops with multiple lines serving, distribute boardings based on the proportion of overall line ridership
 - Iterate through the stops for each line in sequence, adding the boardings for the corresponding line and, using the average length of journey on that line, remove the riders that have been on the line for that length

## Output

The script generates a GeoJSON file (`bus_segments.geojson`) containing detailed segment-level data and aggregated route-level statistics. It is uploaded zipped.