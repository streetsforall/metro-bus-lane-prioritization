# Bus Route Performance Analysis

## Getting Started

After cloning, run the following to install dependencies and prepare the virtual environment using [Poetry](https://python-poetry.org/):

```shells
$ poetry install
``` 

Depending on your choice of means to run jupyter notebooks locally, you'll need to select the poetry-generated virtualenv as your kernel for running the notebook.

## Data Sources (stored in the data/ directory)

1. Bus Speed Data
   - `182_Midday_speeds.geojson`
   - `metro_lines.geojson`

[source](https://rt--cal-itp-data-analyses.netlify.app/district_07-los-angeles/18__speedmaps__district_07-los-angeles__itp_id_182)

2. Ridership Input: Segment-level boardings and de-boardings
   - `bus_ridership.csv`

## Overview

This project analyzes bus route performance in terms of speed and passenger time lost. It combines speed data from different times of day representing the bus service periods (Early AM, AM peak, midday, PM peak, Evening, and Owl) with ridership information to calculate metrics such as:

- Passenger minutes lost
- Passenger minutes lost per mile traveled
- Total ridership minutes lost per route

The analysis identifies routes and segments with the highest impact on passenger travel times, providing insights for potential service improvements.

### Stop-level Ridership Simulation

The approach for generating a useful ridership curve for each route is as follows:

1. Data is loaded which features the boardings and de-boardings for each stop for each line. This is merged with the working speeds dataset.
2. Sequence ids are mapped to those stops, and missing sequence values are filled my iteratively matching stop names to link together sequence chains
3. Each route for each direction is stepped through in sequence order and boardings and de-boardings are aggregated to maintain a count, as each route segment, of approximately how many average riders are on the bus at that segment daily.

### Segment Consolidation

This analysis focuses on the bus network at the geographic segment level since it aims to provide insight on where in the network improvements would make the most impact. It is necessary to combine route segments that share space in the network so that the segments can be aggregated and clearly analyzed. The process for merging segments is as follows:

1. Data is partitioned by direction to prevent merging segments going in opposite directions.
2. LineString data for each segment is buffered into a thin Polygon and its length is slightly reduced to prevent extraneous overlap with adjacent, non-overlapping segments
3. Overlapping segments are programmatically and efficiently identified. Their overlap is compared to a specified overlap threshold, in this case 80%. If they meet or exceed the threshold, they are merged geometrically and the respective data features are appropriately aggregated. 

## Output

The script generates a GeoJSON file (`bus_segments_calculated_ridership.geojson`) containing detailed segment-level data and aggregated route-level statistics. It is uploaded zipped.