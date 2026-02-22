import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import IFrame
from pathlib import Path
from src.config import DTYPE_MAPPING, CUSTOM_CARD_STYLING, PLACEHOLDER_IMAGE_PATH
from src.math_util import calculate_total_miles

# Configure page settings
st.set_page_config(
    page_title="Our Adventures",
    layout="wide"
)

# Custom CSS for card-style details panel
st.markdown(CUSTOM_CARD_STYLING, unsafe_allow_html=True)

st.title("🌍 Our Adventures")

# Load data (not cached since we need to reload after edits)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        "trips.csv",
        dtype=DTYPE_MAPPING,
        skipinitialspace=True
    )

    df["date"] = pd.to_datetime(
        df["date"].str.strip(),
        format="%Y-%m-%d"
    ).dt.date
    
    # Strip whitespace from photo column
    df["photo"] = df["photo"].str.strip()

    return df

# Function to save updated description
def save_description(photo: str, new_description: str):
    df = pd.read_csv("trips.csv", skipinitialspace=True)
    df["photo"] = df["photo"].str.strip()
    df.loc[df["photo"] == photo, "description"] = new_description
    df.to_csv("trips.csv", index=False)

df = load_data()

# Stats at the top
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Trips Taken", len(df['title'].unique()))
col2.metric("Places Visited", df["location"].nunique())
col3.metric("Years of Adventures",
            len(pd.to_datetime(df["date"]).dt.year.unique()))

# Total miles traveled
total_miles = calculate_total_miles(df)
col4.metric("Total Miles Traveled", f"{int(total_miles):,} miles")
col5.metric("Total Photos", len(df))
st.markdown("---")

# 7. Navigation/Filtering Controls Above the Map
st.markdown("### Filter & Search")
filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    sort_by = st.selectbox("Sort by", options=["date", "location", "title"], index=0, key="sort_by")
with filter_col2:
    search = st.text_input("Search by title or location", key="search")
with filter_col3:
    map_style = st.selectbox(
        "Map Style",
        options=["Dark (Sleek)", "Light (Clean)"],
        index=0,
        key="map_style"
    )

filtered_df = df.copy()
if search:
    mask = (
        df["title"].str.contains(search, case=False, na=False, regex=True) |
        df["location"].str.contains(search, case=False, na=False, regex=True) | 
        df["description"].str.contains(search, case=False, na=False, regex=True)
    )
    filtered_df = df[mask]

sorted_df = (
    filtered_df
    .sort_values(sort_by)
    .reset_index(drop=True)
)

# Create map object with responsive height
tile_options = {
    "Dark (Sleek)": "CartoDB dark_matter",
    "Light (Clean)": "CartoDB positron"
}
m = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles=tile_options[map_style]
)

# Add Markers for each visited location
for _, row in sorted_df.iterrows():
    html = f"""
    <h3>{row['title']}</h3>
    <p><b>Date:</b> {row['date']}</p>
    <p>{row['description']}</p>
    """
    iframe = IFrame(html=html, width=300, height=150)
    popup = folium.Popup(iframe, max_width=300)
    try:
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            tooltip=row["title"],
            icon=folium.Icon(color="red", icon="heart")
        ).add_to(m)
    except Exception as e:
        st.error(f"Error adding marker for {row['title']}: {e}")

# Side-by-Side Layout: Map on left, Details on right
map_col, details_col = st.columns([2, 1])

with map_col:
    # Responsive Map Height
    map_data = st_folium(m, width=800, height=500)

# Show details in right column (next to map)
with details_col:
    # Card-style details panel with highlight
    st.markdown("### Trip Details")

    if map_data and map_data.get("last_object_clicked"):
        lat = map_data["last_object_clicked"]["lat"]
        lng = map_data["last_object_clicked"]["lng"]

        # Find ALL matching rows at this location (using tolerance for floating point)
        tolerance = 0.0001  # ~11 meters
        selected = df[
            (abs(df["latitude"] - lat) < tolerance) &
            (abs(df["longitude"] - lng) < tolerance)
        ]

        if not selected.empty:
            # If multiple entries at same location, show tabs
            if len(selected) > 1:
                st.info(f"📸 {len(selected)} photos at this location")
                tabs = st.tabs([f"Photo {i+1}" for i in range(len(selected))])
                for i, (_, row) in enumerate(selected.iterrows()):
                    with tabs[i]:
                        st.markdown('<div class="details-card">', unsafe_allow_html=True)
                        st.subheader(f"💕 {row['title']}")
                        st.write(f"**📍 Location:** {row['location']}")
                        st.write(f"**📅 Date:** {row['date']}")
                        
                        # Editable description field
                        new_desc = st.text_area(
                            "📝 Description",
                            value=row['description'],
                            key=f"desc_map_{row['photo']}_{i}"
                        )
                        if new_desc != row['description']:
                            if st.button("💾 Save", key=f"save_map_{row['photo']}_{i}"):
                                save_description(row['photo'], new_desc)
                                st.success("Description saved!")
                                st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)

                        image_path = Path("photos/updated_pics") / row["photo"]
                        if image_path.exists():
                            st.image(image_path, width='content')
                        else:
                            st.warning(f"Image not found: {row['photo']}")
            else:
                row = selected.iloc[0]
                st.markdown('<div class="details-card">', unsafe_allow_html=True)
                st.subheader(f"💕 {row['title']}")
                st.write(f"**📍 Location:** {row['location']}")
                st.write(f"**📅 Date:** {row['date']}")
                
                # Editable description field
                new_desc = st.text_area(
                    "📝 Description",
                    value=row['description'],
                    key=f"desc_map_{row['photo']}"
                )
                if new_desc != row['description']:
                    if st.button("💾 Save", key=f"save_map_{row['photo']}"):
                        save_description(row['photo'], new_desc)
                        st.success("Description saved!")
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

                image_path = Path("photos/updated_pics") / row["photo"]
                if image_path.exists():
                    st.image(image_path, width='content')
                else:
                    st.warning(f"Image not found: {row['photo']}")
        else:
            st.info("No matching trip found for this location.")
    else:
        # Default placeholder image when no marker selected
        st.info("Click a marker on the map to see trip details and photo.")
        placeholder_path = Path("photos/updated_pics") / PLACEHOLDER_IMAGE_PATH
        if placeholder_path.exists():
            st.image(placeholder_path, caption="Our Special Day ❤️", width='content')

# 2. Collapsible Data Table at the bottom
with st.expander("📋 Show Data Table"):
    # Add row selection to the dataframe
    st.markdown("**Click a row to view its photo:**")
    
    # Create a selectable dataframe
    selected_row = st.dataframe(
        sorted_df[["title", "location", "date", "description", "photo"]],
        width='stretch',
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Show image if a row is selected
    if selected_row and selected_row.selection and selected_row.selection.rows:
        row_idx = selected_row.selection.rows[0]
        selected_trip = sorted_df.iloc[row_idx]
        
        st.markdown("---")
        st.markdown(f"### 📸 {selected_trip['title']}")
        
        # Create columns for image and details
        img_col, info_col = st.columns([1, 1])
        
        with img_col:
            photo_filename = selected_trip["photo"].strip() if isinstance(selected_trip["photo"], str) else None
            if photo_filename:
                image_path = Path(f"photos/updated_pics/{photo_filename}")
                if image_path.exists():
                    st.image(str(image_path), width='content')
                else:
                    st.warning(f"Image not found: {photo_filename}")
            else:
                st.info("No photo available for this trip")
        
        with info_col:
            st.markdown(f"**📍 Location:** {selected_trip['location']}")
            st.markdown(f"**📅 Date:** {selected_trip['date']}")
            
            # Editable description field for data table selection
            new_desc = st.text_area(
                "📝 Description",
                value=selected_trip['description'],
                key=f"desc_table_{selected_trip['photo']}"
            )
            if new_desc != selected_trip['description']:
                if st.button("💾 Save", key=f"save_table_{selected_trip['photo']}"):
                    save_description(selected_trip['photo'], new_desc)
                    st.success("Description saved!")
                    st.rerun()