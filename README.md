## Our Adventures Interactive

An interactive travel memory map built with Streamlit and Folium. Track and visualize your adventures with photos, locations, and memories on a beautiful interactive map.

### Features

- **Interactive Map** - Click markers to view trip details and photos
- **Multiple Map Styles** - Switch between Dark (Sleek) and Light (Clean) themes
- **Photo Gallery** - View multiple photos at the same location with tabbed navigation
- **Search & Filter** - Find trips by title or location with regex support
- **Trip Statistics** - See total trips, places visited, years of adventures, miles traveled, and photo count
- **Responsive Layout** - Side-by-side map and details panel
- **Collapsible Data Table** - View all trip data in an expandable table

### Getting Started

1. Install dependencies:
   ```bash
   pip install streamlit pandas folium streamlit-folium
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

3. Add your trips to `trips.csv` with columns:
   - `title` - Trip name
   - `location` - Specific location
   - `latitude` - Latitude coordinate
   - `longitude` - Longitude coordinate
   - `date` - Date in YYYY-MM-DD format
   - `description` - Trip description
   - `photo` - Photo filename (stored in `photos/updated_pics/`)

### Project Structure

```
├── app.py                 # Main Streamlit application
├── trips.csv              # Trip data
├── photos/
│   └── updated_pics/      # Trip photos
└── src/
    ├── config.py          # Configuration constants
    └── math_util.py       # Utility functions (e.g., distance calculation)
```

### Configuration

Edit `src/config.py` to customize:
- `DTYPE_MAPPING` - CSV column data types
- `CUSTOM_CARD_STYLING` - CSS for the details card
- `PLACEHOLDER_IMAGE_PATH` - Default image when no marker is selected