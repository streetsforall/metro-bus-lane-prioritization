# Bus Route Performance Analysis

## Data Sources

1. Bus Speed Data:
   - `182_Midday_variance.geojson`
   - `182_Midday_speeds.geojson`
   - `182_PM_Peak_speeds.geojson`
   - `182_AM_Peak_speeds.geojson`

[source](https://rt--cal-itp-data-analyses.netlify.app/district_07-los-angeles/18__speedmaps__district_07-los-angeles__itp_id_182)

2. Ridership Data:
   - `ridership.json`

## Overview

This project analyzes bus route performance in terms of speed and passenger time lost. It combines speed data from different times of day (AM peak, midday, PM peak) with ridership information to calculate metrics such as:

- Passenger hours wasted per mile traveled
- Total ridership hours lost per route
- Performance comparisons across different time periods

The analysis identifies routes and segments with the highest impact on passenger travel times, providing insights for potential service improvements.

## Output

The script generates a GeoJSON file (`bus_segments.geojson`) containing detailed segment-level data and aggregated route-level statistics. It is uploaded zipped.