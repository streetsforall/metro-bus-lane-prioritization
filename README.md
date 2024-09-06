# Bus Route Performance Analysis

## Data Sources

1. Bus Speed Data:
   - `182_Midday_variance.geojson`
   - `182_Midday_speeds.geojson`
   - `182_PM_Peak_speeds.geojson`
   - `182_AM_Peak_speeds.geojson`

[source](https://embeddable-maps.calitp.org/?state=eyJuYW1lIjogIm51bGwiLCAibGF5ZXJzIjogW3sibmFtZSI6ICJEMDcgU3RhdGUgSGlnaHdheSBOZXR3b3JrIiwgInVybCI6ICJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vY2FsaXRwLW1hcC10aWxlcy9zcGVlZHNfMjAyNC0wNC0xNy8wN19TSE4uZ2VvanNvbi5neiIsICJwcm9wZXJ0aWVzIjogeyJzdHJva2VkIjogZmFsc2UsICJoaWdobGlnaHRfc2F0dXJhdGlvbl9tdWx0aXBsaWVyIjogMC41fSwgInR5cGUiOiAic3RhdGVfaGlnaHdheV9uZXR3b3JrIn0sIHsibmFtZSI6ICJMb3MgQW5nZWxlcyBDb3VudHkgTWV0cm9wb2xpdGFuIFRyYW5zcG9ydGF0aW9uIEF1dGhvcml0eSBBcHIgMTcsIDIwMjQgKFdlZCkgQU0gUGVhayIsICJ1cmwiOiAiaHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL2NhbGl0cC1tYXAtdGlsZXMvc3BlZWRzXzIwMjQtMDQtMTcvMTgyX0FNX1BlYWtfc3BlZWRzLmdlb2pzb24uZ3oiLCAicHJvcGVydGllcyI6IHsic3Ryb2tlZCI6IGZhbHNlLCAiaGlnaGxpZ2h0X3NhdHVyYXRpb25fbXVsdGlwbGllciI6IDAuNSwgInRvb2x0aXBfc3BlZWRfa2V5IjogInAyMF9tcGgifSwgInR5cGUiOiAic3BlZWRtYXAifV0sICJsYXRfbG9uIjogWzM0LjA1MDUzODc1NzkzMTYxLCAtMTE4LjI5OTAzNzg0MTg1NjA4XSwgInpvb20iOiAxMywgImxlZ2VuZF91cmwiOiAiaHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL2NhbGl0cC1tYXAtdGlsZXMvc3BlZWRzX2xlZ2VuZC5zdmcifQ==)

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