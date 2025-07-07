import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Airly Indoor Air Quality Monitor",
                   layout="wide")

# Authentication settings
DEFAULT_PASSWORD = os.getenv("APP_PASSWORD", "merton")  # Use environment variable or fallback

def check_password():
    """Returns True if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256(DEFAULT_PASSWORD.encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.markdown("## Broadway Market Air Quality Monitoring")
    st.markdown("Please enter the password to access the dashboard:")
    
    st.text_input(
        "Password", 
        type="password", 
        on_change=password_entered, 
        key="password",
        placeholder="Enter password..."
    )
    
    if "password_correct" in st.session_state:
        if not st.session_state["password_correct"]:
            st.error("Password incorrect. Please try again.")
    
    return False

# WHO Guidelines (24-hour average values in µg/m³)
WHO_GUIDELINES = {
    'PM2.5': 15,
    'PM10': 45,
    'PM1': None  # No WHO guideline for PM1
}

# Sensor ID to location name mapping (Broadway Market sensors)
SENSOR_MAPPING = {
    14903: "BM1 - Nr Leather and Lace shop, Longmead Rd entrance",
    14519: "BM2 - Middle corridor - Fishmonger end of corridor",
    14548: "BM3 - Tooting High Street/Gems Broadway entrance nr Craft Tooting",
    14868: "BM4 - Tooting High Street/Aldi/new flats Entrance nr Chinese Food"
}

# Sensor locations on the map (as % of image width/height)
# Edit these coordinates to position sensors correctly on your map
SENSOR_LOCATIONS = {
    14903: {
        "x": 88,
        "y": 21
    },  # BM1 - Nr Leather and Lace shop, Longmead Rd entrance
    14519: {
        "x": 36,
        "y": 58
    },  # BM2 - Middle corridor - Fishmonger end of corridor  
    14548: {
        "x": 19,
        "y": 33
    },  # BM3 - Tooting High Street/Gems Broadway entrance nr Craft Tooting
    14868: {
        "x": 20,
        "y": 60
    }  # BM4 - Tooting High Street/Aldi/new flats Entrance nr Chinese Food
}

# Color scale for air quality levels
COLOR_SCALE = {
    'PM2.5': [{
        'max': 11.5,
        'color': '#2E8B57',
        'name': 'SeaGreen'
    }, {
        'max': 23.5,
        'color': '#3CB371',
        'name': 'MediumSeaGreen'
    }, {
        'max': 35.5,
        'color': '#9ACD32',
        'name': 'YellowGreen'
    }, {
        'max': 41.5,
        'color': '#FFFF00',
        'name': 'Yellow'
    }, {
        'max': 47.5,
        'color': '#FFA500',
        'name': 'Orange'
    }, {
        'max': 53.5,
        'color': '#FF8C00',
        'name': 'DarkOrange'
    }, {
        'max': 58.5,
        'color': '#FF4500',
        'name': 'OrangeRed'
    }, {
        'max': 64.5,
        'color': '#DC143C',
        'name': 'Crimson'
    }, {
        'max': 70.5,
        'color': '#B22222',
        'name': 'FireBrick'
    }, {
        'max': 120,
        'color': '#800080',
        'name': 'Purple'
    }, {
        'max': float('inf'),
        'color': '#310154',
        'name': 'Deep Violet'
    }],
    'PM10': [{
        'max': 16.5,
        'color': '#2E8B57',
        'name': 'SeaGreen'
    }, {
        'max': 33.5,
        'color': '#3CB371',
        'name': 'MediumSeaGreen'
    }, {
        'max': 50.5,
        'color': '#9ACD32',
        'name': 'YellowGreen'
    }, {
        'max': 58.5,
        'color': '#FFFF00',
        'name': 'Yellow'
    }, {
        'max': 66.5,
        'color': '#FFA500',
        'name': 'Orange'
    }, {
        'max': 75.5,
        'color': '#FF8C00',
        'name': 'DarkOrange'
    }, {
        'max': 83.5,
        'color': '#FF4500',
        'name': 'OrangeRed'
    }, {
        'max': 91.5,
        'color': '#DC143C',
        'name': 'Crimson'
    }, {
        'max': 100.5,
        'color': '#B22222',
        'name': 'FireBrick'
    }, {
        'max': 180,
        'color': '#800080',
        'name': 'Purple'
    }, {
        'max': float('inf'),
        'color': '#310154',
        'name': 'Deep Violet'
    }],
    'PM1': [  # Use PM2.5 scale for PM1 as no specific guidelines exist
        {
            'max': 11.5,
            'color': '#2E8B57',
            'name': 'SeaGreen'
        }, {
            'max': 23.5,
            'color': '#3CB371',
            'name': 'MediumSeaGreen'
        }, {
            'max': 35.5,
            'color': '#9ACD32',
            'name': 'YellowGreen'
        }, {
            'max': 41.5,
            'color': '#FFFF00',
            'name': 'Yellow'
        }, {
            'max': 47.5,
            'color': '#FFA500',
            'name': 'Orange'
        }, {
            'max': 53.5,
            'color': '#FF8C00',
            'name': 'DarkOrange'
        }, {
            'max': 58.5,
            'color': '#FF4500',
            'name': 'OrangeRed'
        }, {
            'max': 64.5,
            'color': '#DC143C',
            'name': 'Crimson'
        }, {
            'max': 70.5,
            'color': '#B22222',
            'name': 'FireBrick'
        }, {
            'max': 120,
            'color': '#800080',
            'name': 'Purple'
        }, {
            'max': float('inf'),
            'color': '#310154',
            'name': 'Deep Violet'
        }
    ]
}


def get_color_for_value(pollutant, value):
    """Get color for a pollutant value based on the color scale"""
    scale = COLOR_SCALE.get(pollutant, COLOR_SCALE['PM2.5'])

    for level in scale:
        if value <= level['max']:
            return level['color'], level['name']

    # Default to last color if value exceeds all thresholds
    return scale[-1]['color'], scale[-1]['name']


@st.cache_data
def load_and_process_data():
    """Load and process the Airly CSV data"""
    try:
        # Try to load the CSV file
        csv_path = "attached_assets/Airly_Report_London_Borough_of_Wandsworth_2025_07_07_10_35_27_1751881436832.csv"

        if not os.path.exists(csv_path):
            st.error(f"Data file not found at: {csv_path}")
            return None

        # Load the CSV data
        df = pd.read_csv(csv_path)

        # Parse datetime
        df['From'] = pd.to_datetime(df['From'])
        df['Till'] = pd.to_datetime(df['Till'])

        # Extract time components for weekly pattern analysis
        df['hour'] = df['From'].dt.hour
        df['day_of_week'] = df['From'].dt.day_name()
        df['day_num'] = df['From'].dt.dayofweek

        # Map sensor IDs to readable names
        df['Location_Name'] = df['Sensor id'].map(SENSOR_MAPPING)

        # Clean column names for pollutants
        pollutant_columns = {
            'PM10 [ug/m3]': 'PM10',
            'PM2.5 [ug/m3]': 'PM2.5',
            'PM1 [ug/m3]': 'PM1'
        }
        df = df.rename(columns=pollutant_columns)

        return df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def create_time_series_chart(df, pollutant):
    """Create time series chart for all hourly data"""
    fig = go.Figure()

    # Get unique sensors that have non-null location names
    sensors = df[df['Location_Name'].notna()]['Location_Name'].unique()

    if len(sensors) == 0:
        st.error("No sensors found with valid location names")
        return fig

    # Color palette for different sensors
    colors = px.colors.qualitative.Set1[:len(sensors)]

    for i, sensor in enumerate(sensors):
        sensor_data = df[df['Location_Name'] == sensor]

        # Skip if no data for this pollutant
        if sensor_data[pollutant].isna().all():
            continue

        fig.add_trace(
            go.Scatter(x=sensor_data['From'],
                       y=sensor_data[pollutant],
                       mode='lines',
                       name=sensor,
                       line=dict(color=colors[i], width=2),
                       hovertemplate=f'<b>{sensor}</b><br>' +
                       'Time: %{x}<br>' +
                       f'{pollutant}: %{{y}} µg/m³<extra></extra>'))

    # Add WHO guideline if available
    if WHO_GUIDELINES[pollutant] is not None:
        fig.add_hline(y=WHO_GUIDELINES[pollutant],
                      line_dash="dash",
                      line_color="red",
                      annotation_text=
                      f"WHO 24h Guideline ({WHO_GUIDELINES[pollutant]} µg/m³)",
                      annotation_position="top left",
                      annotation_font_color="red")

    fig.update_layout(title=f'{pollutant} Hourly Measurements - Time Series',
                      xaxis_title='Date and Time',
                      yaxis_title=f'{pollutant} Concentration (µg/m³)',
                      hovermode='x unified',
                      height=500,
                      showlegend=True,
                      legend=dict(orientation="h",
                                  yanchor="top",
                                  y=-0.15,
                                  xanchor="center",
                                  x=0.5,
                                  font=dict(size=14)))

    return fig


def create_weekly_pattern_chart(df, pollutant):
    """Create weekly pattern chart averaging same hours across days"""

    # Filter for valid location names only
    df_valid = df[df['Location_Name'].notna()]

    if len(df_valid) == 0:
        st.error("No valid sensor data found")
        return go.Figure()

    # Calculate hourly averages for each day of week and sensor
    weekly_pattern = df_valid.groupby(
        ['day_num', 'day_of_week', 'hour',
         'Location_Name'])[pollutant].mean().reset_index()

    fig = go.Figure()

    # Get unique sensors
    sensors = df_valid['Location_Name'].unique()
    colors = px.colors.qualitative.Set1[:len(sensors)]

    # Days of week in order
    days_order = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
    ]

    for i, sensor in enumerate(sensors):
        sensor_data = weekly_pattern[weekly_pattern['Location_Name'] == sensor]

        # Create x-axis values: day_num * 24 + hour for proper spacing
        x_values = sensor_data['day_num'] * 24 + sensor_data['hour']

        fig.add_trace(
            go.Scatter(x=x_values,
                       y=sensor_data[pollutant],
                       mode='lines+markers',
                       name=sensor,
                       line=dict(color=colors[i], width=2),
                       marker=dict(size=4),
                       hovertemplate=f'<b>{sensor}</b><br>' +
                       'Day: %{customdata[0]}<br>' +
                       'Hour: %{customdata[1]}:00<br>' +
                       f'{pollutant}: %{{y:.2f}} µg/m³<extra></extra>',
                       customdata=sensor_data[['day_of_week', 'hour']].values))

    # Add WHO guideline if available
    if WHO_GUIDELINES[pollutant] is not None:
        fig.add_hline(y=WHO_GUIDELINES[pollutant],
                      line_dash="dash",
                      line_color="red",
                      annotation_text=
                      f"WHO 24h Guideline ({WHO_GUIDELINES[pollutant]} µg/m³)",
                      annotation_position="top left",
                      annotation_font_color="red")

    # Add vertical lines to separate days and day labels
    for day_num, day_name in enumerate(days_order):
        x_pos = day_num * 24
        if day_num > 0:  # Don't add line before first day
            fig.add_vline(x=x_pos,
                          line_dash="dot",
                          line_color="gray",
                          opacity=0.5)

    # Update layout with custom x-axis labels
    fig.update_layout(
        title=f'{pollutant} Weekly Pattern - Average by Hour and Day',
        xaxis_title='Day of Week and Hour',
        yaxis_title=f'{pollutant} Concentration (µg/m³)',
        hovermode='closest',
        height=500,
        showlegend=True,
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=14)),
        xaxis=dict(
            tickmode='array',
            tickvals=[day_num * 24 + 12
                      for day_num in range(7)],  # Middle of each day
            ticktext=days_order,
            range=[-2, 7 * 24 + 2]))

    return fig


def create_single_day_chart(df, pollutant, selected_day):
    """Create chart for a single day showing hourly patterns"""

    # Filter for valid location names only
    df_valid = df[df['Location_Name'].notna()]

    if len(df_valid) == 0:
        st.error("No valid sensor data found")
        return go.Figure()

    # Filter for the selected day
    day_data = df_valid[df_valid['day_of_week'] == selected_day]

    if len(day_data) == 0:
        st.warning(f"No data found for {selected_day}")
        return go.Figure()

    # Calculate hourly averages for the selected day
    hourly_pattern = day_data.groupby(['hour', 'Location_Name'
                                       ])[pollutant].mean().reset_index()

    fig = go.Figure()

    # Get unique sensors
    sensors = df_valid['Location_Name'].unique()
    colors = px.colors.qualitative.Set1[:len(sensors)]

    for i, sensor in enumerate(sensors):
        sensor_data = hourly_pattern[hourly_pattern['Location_Name'] == sensor]

        if len(sensor_data) == 0:
            continue

        fig.add_trace(
            go.Scatter(x=sensor_data['hour'],
                       y=sensor_data[pollutant],
                       mode='lines+markers',
                       name=sensor,
                       line=dict(color=colors[i], width=3),
                       marker=dict(size=6),
                       hovertemplate=f'<b>{sensor}</b><br>' +
                       'Hour: %{x}:00<br>' +
                       f'{pollutant}: %{{y:.2f}} µg/m³<extra></extra>'))

    # Add WHO guideline if available
    if WHO_GUIDELINES[pollutant] is not None:
        fig.add_hline(y=WHO_GUIDELINES[pollutant],
                      line_dash="dash",
                      line_color="red",
                      annotation_text=
                      f"WHO 24h Guideline ({WHO_GUIDELINES[pollutant]} µg/m³)",
                      annotation_position="top left",
                      annotation_font_color="red")

    fig.update_layout(title=f'{pollutant} Hourly Pattern - {selected_day}',
                      xaxis_title='Hour of Day',
                      yaxis_title=f'{pollutant} Concentration (µg/m³)',
                      hovermode='closest',
                      height=500,
                      showlegend=True,
                      legend=dict(orientation="h",
                                  yanchor="top",
                                  y=-0.15,
                                  xanchor="center",
                                  x=0.5,
                                  font=dict(size=14)),
                      xaxis=dict(tickmode='linear',
                                 tick0=0,
                                 dtick=2,
                                 range=[-0.5, 23.5]))

    return fig


def create_map_visualization(df, pollutant, selected_time_idx):
    """Create map visualization with sensors positioned on background image"""
    import base64

    # Filter for valid location names only
    df_valid = df[df['Location_Name'].notna()]

    if len(df_valid) == 0:
        st.error("No valid sensor data found")
        return go.Figure()

    # Calculate weekly pattern data (same as weekly pattern chart)
    weekly_pattern = df_valid.groupby(
        ['day_num', 'day_of_week', 'hour',
         'Location_Name'])[pollutant].mean().reset_index()

    # Create time series for map navigation
    time_points = []
    for day_num in range(7):
        for hour in range(24):
            time_points.append({
                'day_num': day_num,
                'hour': hour,
                'time_idx': day_num * 24 + hour
            })

    if selected_time_idx >= len(time_points):
        selected_time_idx = 0

    current_time = time_points[selected_time_idx]
    day_names = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
    ]

    # Get data for current time point
    current_data = weekly_pattern[
        (weekly_pattern['day_num'] == current_time['day_num'])
        & (weekly_pattern['hour'] == current_time['hour'])]

    # Create figure with map background
    fig = go.Figure()

    # Load and encode the background image
    try:
        with open("attached_assets/broadway 2_1751883488289.png", "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()

        # Add background image with fixed coordinate system
        fig.add_layout_image(
            dict(source=f"data:image/png;base64,{encoded_image}",
                 xref="x",
                 yref="y",
                 x=0,
                 y=75,
                 sizex=100,
                 sizey=75,
                 sizing="stretch",
                 opacity=0.8,
                 layer="below"))
    except Exception as e:
        st.warning(f"Could not load background image: {e}")

    # Add sensors to map with color scale
    if len(current_data) > 0:
        # Get value range for size scaling
        min_val = current_data[pollutant].min()
        max_val = current_data[pollutant].max()

        for sensor_id, location in SENSOR_LOCATIONS.items():
            sensor_data = current_data[current_data['Location_Name'] ==
                                       SENSOR_MAPPING[sensor_id]]

            if len(sensor_data) > 0:
                value = sensor_data[pollutant].iloc[0]

                # Get color based on air quality color scale
                color, color_name = get_color_for_value(pollutant, value)

                # Continuous size scaling based on actual data ranges
                data_ranges = {
                    "PM1": {
                        "min": 0.4,
                        "max": 238.78
                    },
                    "PM2.5": {
                        "min": 0.69,
                        "max": 277.45
                    },
                    "PM10": {
                        "min": 7.67,
                        "max": 283.98
                    }
                }

                # Get range for current pollutant
                min_val = data_ranges[pollutant]["min"]
                max_val = data_ranges[pollutant]["max"]

                # Normalize value to 0-1 range
                normalized = (value - min_val) / (max_val - min_val)
                normalized = max(0, min(1, normalized))  # Clamp to 0-1

                # Very subtle size scaling:8px to 32px (small range for subtle effect)
                size = 25 + (normalized * 40)  # Size range

                fig.add_trace(
                    go.Scatter(
                        x=[location["x"]],
                        y=[location["y"]],
                        mode='markers',
                        marker=dict(size=size,
                                    color=color,
                                    line=dict(width=2, color='white')),
                        name=SENSOR_MAPPING[sensor_id],
                        hovertemplate=f'<b>{SENSOR_MAPPING[sensor_id]}</b><br>'
                        + f'{pollutant}: {value:.2f} µg/m³<br>' +
                        f'Quality Level: {color_name}<br>' +
                        f'Time: {day_names[current_time["day_num"]]} {current_time["hour"]:02d}:00<extra></extra>'
                    ))

    # Update layout for fixed aspect ratio map display
    fig.update_layout(
        title=
        f'{pollutant} Map View - {day_names[current_time["day_num"]]} {current_time["hour"]:02d}:00',
        xaxis=dict(range=[0, 100],
                   showgrid=False,
                   zeroline=False,
                   showticklabels=False,
                   scaleanchor="y",
                   scaleratio=1,
                   constrain="domain"),
        yaxis=dict(range=[0, 75],
                   showgrid=False,
                   zeroline=False,
                   showticklabels=False,
                   constrain="domain"),
        plot_bgcolor='rgba(0,0,0,0)',
        width=1000,
        height=750,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=True,
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.02,
                    xanchor="center",
                    x=0.5),
        autosize=False)

    return fig


def display_data_summary(df):
    """Display data summary statistics"""
    st.subheader("Data Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Dataset Overview:**")
        st.write(f"• Total records: {len(df):,}")
        st.write(
            f"• Date range: {df['From'].min().strftime('%Y-%m-%d')} to {df['From'].max().strftime('%Y-%m-%d')}"
        )
        st.write(f"• Number of sensors: {df['Sensor id'].nunique()}")

        # Data quality indicators
        total_possible = len(df)
        for pollutant in ['PM1', 'PM2.5', 'PM10']:
            missing = df[pollutant].isna().sum()
            coverage = (total_possible - missing) / total_possible * 100
            st.write(f"• {pollutant} data coverage: {coverage:.1f}%")

    with col2:
        st.write("**Sensor Locations:**")
        sensor_counts = df.groupby(['Sensor id', 'Location_Name'
                                    ]).size().reset_index(name='Records')
        for _, row in sensor_counts.iterrows():
            st.write(
                f"• {row['Location_Name']} (ID: {row['Sensor id']}): {row['Records']:,} records"
            )


def display_pollutant_statistics(df, pollutant):
    """Display statistics for selected pollutant"""
    st.subheader(f"{pollutant} Statistics")

    # Calculate statistics by sensor
    stats = df.groupby('Location_Name')[pollutant].agg(
        ['count', 'mean', 'median', 'min', 'max', 'std']).round(2)

    # Display as a formatted table
    st.write("**Statistics by Sensor Location:**")

    # Format the statistics table
    stats_display = stats.copy()
    stats_display.columns = [
        'Count', 'Mean', 'Median', 'Min', 'Max', 'Std Dev'
    ]

    # Add WHO guideline comparison
    if WHO_GUIDELINES[pollutant] is not None:
        guideline = WHO_GUIDELINES[pollutant]
        above_who_pct = []
        for location in df['Location_Name'].unique():
            location_data = df[df['Location_Name'] == location][pollutant]
            above_count = (location_data > guideline).sum()
            total_count = location_data.count()
            pct = (above_count / total_count * 100) if total_count > 0 else 0
            above_who_pct.append(pct)

        stats_display['Above WHO (%)'] = [
            round(pct, 1) for pct in above_who_pct
        ]
        st.write(f"*WHO 24-hour guideline for {pollutant}: {guideline} µg/m³*")
    else:
        st.write(f"*No WHO guideline available for {pollutant}*")

    st.dataframe(stats_display, use_container_width=True)


def main():
    """Main application function"""
    
    # Check password first
    if not check_password():
        st.stop()

    # App header
    st.title("Airly Indoor Air Quality Monitor")
    st.markdown(
        "**Exploring PM1, PM2.5, and PM10 data from 4 Broadway Market sensors in Wandsworth**"
    )

    # Load data
    df = load_and_process_data()

    if df is None:
        st.stop()

    # Sidebar for controls
    with st.sidebar:
        # Logout button
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        st.header("Chart Controls")

        # Pollutant selection
        pollutant = st.selectbox(
            "Select Pollutant to Display:",
            options=['PM2.5', 'PM10', 'PM1'],
            help="Choose which pollutant concentration to visualize")

        st.markdown("---")

        # WHO Guidelines info
        st.subheader("WHO Guidelines")
        st.write("**24-hour average limits:**")
        st.write("• PM2.5: 15 µg/m³")
        st.write("• PM10: 45 µg/m³")
        st.write("• PM1: No guideline")

        st.markdown("---")

        # Sensor info
        st.subheader("Broadway Market Sensors")
        sensor_codes = {14903: "BM1", 14519: "BM2", 14548: "BM3", 14868: "BM4"}
        for sensor_id, location in SENSOR_MAPPING.items():
            st.write(f"• **{sensor_codes[sensor_id]}**: {location}")

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Time Series", "Weekly Patterns", "Map View", "Data Summary"])

    with tab1:
        st.subheader(f"Hourly {pollutant} Measurements Over Time")
        st.plotly_chart(create_time_series_chart(df, pollutant),
                        use_container_width=True)

        # Show statistics for selected pollutant
        display_pollutant_statistics(df, pollutant)

    with tab2:
        st.subheader(f"Weekly {pollutant} Patterns")
        st.markdown(
            "*Averages of the same hour across all days in the dataset*")
        st.plotly_chart(create_weekly_pattern_chart(df, pollutant),
                        use_container_width=True)

        # Day selection for detailed view
        st.subheader("Single Day View")
        selected_day = st.selectbox(
            "Select a day to view detailed hourly patterns:",
            options=['All Days'] + [
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday'
            ],
            help=
            "Choose a specific day to see hourly patterns for that day only")

        if selected_day != 'All Days':
            st.plotly_chart(create_single_day_chart(df, pollutant,
                                                    selected_day),
                            use_container_width=True)

        # Additional info about weekly patterns
        st.info(
            "**How to read this chart:** Each line represents a sensor location. "
            "The x-axis shows days of the week with hours. This helps identify daily patterns "
            "and differences between weekdays and weekends.")

    with tab3:
        st.subheader(f"Weekly Pattern Map - {pollutant}")
        st.markdown(
            "*Navigate through time to see how air quality changes across sensor locations*"
        )

        # Initialize session state for time navigation
        if 'time_index' not in st.session_state:
            st.session_state.time_index = 0

        # Current time display on one line
        day_names = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday'
        ]
        current_day = st.session_state.time_index // 24
        current_hour = st.session_state.time_index % 24
        if current_day < 7:
            st.markdown(f"## {day_names[current_day]} {current_hour:02d}:00")
        else:
            st.markdown("## End of Week")

        # Time navigation controls with gap between backward and forward
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])

        with col1:
            if st.button("◀◀ -24h", key="btn_minus_24h"):
                st.session_state.time_index = max(
                    0, st.session_state.time_index - 24)
                st.rerun()

        with col2:
            if st.button("◀ -1h", key="btn_minus_1h"):
                st.session_state.time_index = max(
                    0, st.session_state.time_index - 1)
                st.rerun()

        with col3:
            # Gap column
            st.write("")

        with col4:
            if st.button("▶ +1h", key="btn_plus_1h"):
                st.session_state.time_index = min(
                    167, st.session_state.time_index + 1)  # 7*24-1
                st.rerun()

        with col5:
            if st.button("▶▶ +24h", key="btn_plus_24h"):
                st.session_state.time_index = min(
                    167, st.session_state.time_index + 24)
                st.rerun()

        # Time slider for quick navigation - shorter without value display
        new_time_index = st.slider("Time",
                                   min_value=0,
                                   max_value=167,
                                   value=st.session_state.time_index,
                                   label_visibility="collapsed",
                                   key="time_slider")

        # Update session state if slider value changed
        if new_time_index != st.session_state.time_index:
            st.session_state.time_index = new_time_index

        # Map and color scale in side-by-side layout
        col_map, col_scale = st.columns([6, 1])

        with col_map:
            st.plotly_chart(create_map_visualization(
                df, pollutant, st.session_state.time_index),
                            use_container_width=True,
                            key=f"map_chart_{st.session_state.time_index}")

        with col_scale:
            st.write("**Legend**")
            scale_data = COLOR_SCALE[pollutant]

            # Create vertical color scale display
            for i, level in enumerate(scale_data):
                if level['max'] == float('inf'):
                    range_text = f"> {scale_data[i-1]['max']}"
                elif i == 0:
                    range_text = f"≤ {level['max']}"
                else:
                    range_text = f"≤ {level['max']}"

                st.markdown(
                    f'<div style="background-color: {level["color"]}; color: white; '
                    f'padding: 8px; text-align: center; border-radius: 4px; margin: 2px;">'
                    f'<small>{range_text}</small></div>',
                    unsafe_allow_html=True)

        # Map instructions
        st.info(
            "**Map Guide:** Sensor colors represent air quality levels according to the scale above. "
            "Sensor size increases quadratically with pollution level relative to current readings. "
            "Use the time controls to navigate through different times of the week."
        )

        # Sensor position editing instructions
        st.expander("Edit Sensor Positions").write(
            "To adjust sensor positions on the map, edit the SENSOR_LOCATIONS dictionary in the code. "
            "Coordinates are percentages of image width/height (0-100). "
            f"Current positions: {SENSOR_LOCATIONS}")

    with tab4:
        display_data_summary(df)

        # Show raw data sample
        st.subheader("Raw Data Sample")
        st.write("*First 10 records:*")
        display_columns = [
            'From', 'Location_Name', 'PM1', 'PM2.5', 'PM10',
            'Temperature [°C]', 'Humidity [%]'
        ]
        st.dataframe(df[display_columns].head(10), use_container_width=True)


if __name__ == "__main__":
    main()
