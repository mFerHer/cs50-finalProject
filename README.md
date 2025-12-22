# En Ruta
## Video Demo:  <URL HERE>
## Description:
**En Ruta** is a web-based application built using Python, JavaScript, Flask, and SQLite.
It is primarly aimed at proffesional drivers, such as truckers, who require up-to-date fuel pricing information while planning or driving long routes.

The core objective of the project is to display current fuel prices for petrol stations across Spain and allow users to visually explore this data on an interactive map. By centralizing official government data and presenting it in a geographic format, En Ruta enables users to quickly identify fuel stations and compare prices by fuel type, helping reduce operational costs during travel.

Fuel price data is sourced from the official Spanish government energy services API, ensuring reliability and frequent updates.

## How does it work?
### update_database.py

This Python script is responsible for fetching, processing, and storing fuel price data.

It sends a request to the Spanish Ministry of Energy’s public REST API, which provides information on all registered petrol stations in Spain. The response is returned as a JSON object containing a list of stations, each represented as a dictionary.

A key design decision was to separate station metadata from fuel prices into different tables. This improves normalization, avoids redundancy, and allows prices to be updated independently of static location data.
The script uses ON CONFLICT clauses to update existing records rather than duplicating them, ensuring idempotent updates.

Fuel prices are converted from the Spanish numeric format (comma as decimal separator) to floating-point values compatible with SQLite and Python.
Only stations intended for public sale are included.

Finally, the script records the last update timestamp in UTC, which is later displayed in the web interface.

### data.db

This SQLite database stores all persistent application data.

It contains three SQLite tables:
- info: stores static station metadata such as name, address, municipality, timetable, and geographic coordinates.

- prices: stores fuel prices for multiple fuel types (Gasoline 95, Gasoline 98, Diesel, Diesel Premium, and Diesel B).

- metadata: stores the timestamp of the last successful update.

SQLite was chosen due to its simplicity, portability, and suitability for a read-heavy application with structured relational data.

### .github/workflows/update.yml

This GitHub Actions workflow automates the execution of update_database.py.

It allows the database to be refreshed every 24 hours without manual intervention. This design ensures that fuel prices remain current while keeping the application lightweight and server-independent.

### app.py

This file contains the Flask backend of the application.

It defines a single route (/) that:
- Connects to the SQLite database
- Retrieves joined station and price data
- Fetches the last update timestamp
- Computes average latitude and longitude values per locality to support map centering and clustering

The data is passed to the frontend using Flask’s template rendering system.
The application is intentionally kept minimal to focus on data delivery rather than server-side logic, as most interactivity is handled client-side.

### templates/index.html

This file defines the main user interface of the application.

It receives data from Flask and renders:
- The interactive map
- Fuel station markers
- Update timestamps
- Client-side logic hooks for JavaScript-based interaction

The HTML structure is designed to work closely with Leaflet.js for geographic visualization.

### static/leaflet.js

This JavaScript file contains the core client-side logic of the application using the Leaflet library. It is responsible for rendering the interactive map, plotting petrol stations, handling user input, calculating routes, and identifying the cheapest fuel station either globally or along a selected route.

All logic is executed after the DOM has fully loaded to ensure that required HTML elements and data injected by Flask are available.

Separating mapping logic into its own file improves maintainability and keeps the HTML template clean.

**Step 0: Map Initialization**

The script begins by initializing a Leaflet map centered on Spain using Madrid as the default focal point. OpenStreetMap tiles are used as the base layer, providing an open-source and lightweight mapping solution.

This initial configuration establishes the geographic context of the application and ensures that the map is immediately usable without requiring user interaction.

**Step 1: Petrol Station Markers**

Fuel stations are plotted on the map using marker clustering. Marker clustering is a deliberate design choice aimed at preserving performance and usability, as thousands of petrol stations exist across Spain.

Each station is represented with a custom fuel-pump icon. Stations without valid geographic coordinates are skipped to avoid rendering errors. Clicking on a marker opens a popup displaying detailed station information, including address, timetable, and fuel prices by type.

Clustering parameters such as radius and chunked loading are tuned to balance responsiveness with visual clarity.

**Step 2: Origin and Destination Locations**

The application allows users to select an origin and destination from predefined localities. To support this, the script builds a lookup table mapping locality names to their average geographic coordinates.

Distinct visual markers are used for:
- Origin (green marker)
- Destination (red marker)

When a location is selected, any existing marker of the same type is removed to prevent duplication. The map automatically centers on the newly placed marker, improving user orientation.

This step provides the foundation for route calculation and contextual fuel price analysis.

**Step 3: Route Calculation and Display**

Once both origin and destination are defined, the application calculates a route using the Open Source Routing Machine (OSRM) service.

Key design choices in this step include:
- Disabling waypoint dragging to preserve route integrity
- Rendering only the route polyline, without default markers
- Automatically fitting the route within the map view

When a route is found, the total distance and estimated travel time are extracted and displayed in the interface. Route coordinates are stored internally for later spatial analysis, enabling proximity-based fuel station filtering.

**Step 4: Identifying the Cheapest Petrol Station**

This step determines the cheapest petrol station based on the selected fuel type.

Users may search:
- Across all stations, or
- Only among stations near the calculated route

Distance checks are performed by comparing station coordinates with route points, allowing stations within a defined threshold (0.5 km) to qualify. This spatial filtering avoids unnecessary detours and aligns with real-world driving behavior.

Once identified, the cheapest station is emphasized using a distinct star icon and brought into focus on the map.

**Step 5: Event Handling and User Interaction**

The final step wires all functionality together using event listeners attached to user interface elements.

These listeners:
- Place origin and destination markers
- Trigger route calculation
- Initiate cheapest-station search

By deferring all event handling until the final stage, the script maintains a clear execution flow and avoids unintended side effects during initialization.

### static/style.cs

This file defines the visual styling of the application.

It controls layout, typography, spacing, and overall presentation to ensure clarity and usability.

### .vscode/extensions.json, launch.json, settings.json

These files store development environment configuration for Visual Studio Code.

They are not required for running the application but help maintain consistency during development.

### .\_\_pycache\_\_/app.cpython-314.pyc

This directory contains automatically generated Python bytecode.

It is produced by the Python interpreter to improve execution performance and is not part of the project’s source logic.
