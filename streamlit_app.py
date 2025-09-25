import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import time


from weather_app import WeatherApp


st.set_page_config(
    page_title="Weather Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .city-title {
        font-size: 2rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .weather-description {
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
    }
    .data-source {
        background: #e3f2fd;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        color: #1976d2;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

if 'weather_app' not in st.session_state:
    st.session_state.weather_app = WeatherApp()
    st.session_state.search_history = []
    st.session_state.current_city = None
    st.session_state.last_search_time = None

def main():
    st.markdown('<h1 class="main-header">Weather App</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Choose a section:",
            ["Current Weather", "5-Day Forecast", "Favorites"]
        )
        
        st.markdown("---")
        
        
        st.header("Quick Search")
        quick_city = st.text_input("Enter city name:", placeholder="e.g., London, Tokyo, New York")
        
        if st.button("Search Weather", key="quick_search_btn", type="primary"):
            if quick_city:
                search_weather(quick_city)
        
        
        if st.session_state.search_history:
            st.header("Recent Searches")
            for city in reversed(st.session_state.search_history[-5:]):  # Last 5 searches, newest first
                if st.button(f"{city}", key=f"history_{city}"):
                    search_weather(city)
        
        
        st.markdown("---")
        with st.expander("About this app"):
            st.write("""
            This weather app provides:
            - Current weather 
            - 5-day forecast
            - Interactive charts
            - Favorite cities 
            - Global data
            
            Data used from OpenWeatherMap API
            """)
    
    
    if page == "Current Weather":
        show_current_weather()
    elif page == "5-Day Forecast":
        show_forecast()
    elif page == "Favorites":
        show_favorites()

def search_weather(city):
    st.session_state.current_city = city
    
    with st.spinner(f"Fetching weather data for {city}..."):
        try:
            st.session_state.weather_app.search_city(city)
            st.session_state.last_search_time = datetime.now()
            
           
            if city not in st.session_state.search_history:
                st.session_state.search_history.append(city)
                if len(st.session_state.search_history) > 10:
                    st.session_state.search_history.pop(0)
            
            st.success(f"Weather data loaded for {city}")
            
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")
            st.info("Try checking the city name spelling")

def show_current_weather():
    st.header("Current Weather")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        city = st.text_input(
            "Enter city name:", 
            value=st.session_state.current_city or "",
            placeholder="Enter any city name (e.g., Paris, Mumbai, Sydney)"
        )
    
    with col2:
        st.write("")
        search_button = st.button("Get Weather", type="primary", use_container_width=True)
    
    if search_button and city:
        search_weather(city)
    
    if hasattr(st.session_state.weather_app, 'current_weather') and st.session_state.weather_app.current_weather:
        display_current_weather_data()
    
    elif st.session_state.current_city:
        st.info(f"Enter city name and click 'Get Weather' ")
    
    else:
        st.info("Welcome! Enter city name to get started")

def display_current_weather_data():
    try:
        data = st.session_state.weather_app.current_weather
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<h2 class="city-title">{data["name"]}, {data["sys"]["country"]}</h2>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.last_search_time:
                st.write(f"Updated: {st.session_state.last_search_time.strftime('%H:%M:%S')}")
        
        st.markdown('<div class="data-source">OpenWeatherMap</div>', unsafe_allow_html=True)
        
        
        weather_desc = data['weather'][0]['description'].title()
        st.markdown(f'<p class="weather-description">{weather_desc}</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            st.metric(
                label="Temperature",
                value=f"{temp:.1f}°C",
                delta=f"Feels like {feels_like:.1f}°C"
            )
        
        with col2:
            humidity = data['main']['humidity']
            st.metric(
                label="Humidity",
                value=f"{humidity}%"
            )
        
        with col3:
            pressure = data['main']['pressure']
            st.metric(
                label="Pressure",
                value=f"{pressure} hPa"
            )
        
        with col4:
            wind_speed = data.get('wind', {}).get('speed', 0)
            st.metric(
                label="Wind Speed",
                value=f"{wind_speed} m/s"
            )
        
        with st.expander("Sun & Sky Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                st.write(f"**Sunrise:** {sunrise}")
                st.write(f"**Sunset:** {sunset}")
                
                if 'visibility' in data:
                    visibility_km = data['visibility'] / 1000
                    st.write(f"**Visibility:** {visibility_km:.1f} km")
            
            with col2:
                if 'clouds' in data:
                    cloudiness = data['clouds']['all']
                    st.write(f"**Cloudiness:** {cloudiness}%")
                
                if 'wind' in data and 'deg' in data['wind']:
                    wind_dir = data['wind']['deg']
                    st.write(f"**Wind Direction:** {wind_dir}°")
                
                st.write(f"**Coordinates:** {data['coord']['lat']:.2f}, {data['coord']['lon']:.2f}")
    
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Add to Favorites", key="add_favorite"):
                success = st.session_state.weather_app.add_to_favorites()
                if success:
                    st.success(f"{data['name']} added to favorites!")
                else:
                    st.info(f"{data['name']} is already in favorites")
        
        with col2:
            if st.button("Refresh", key="refresh"):
                search_weather(st.session_state.current_city)
        
    except Exception as e:
        st.error(f"Error displaying weather data: {str(e)}")

def show_forecast():
    st.header("5-Day Weather Forecast")
    
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        forecast_city = st.text_input(
            "Enter city for forecast:", 
            value=st.session_state.current_city or "",
            key="forecast_city",
            placeholder="Enter city name for 5-day forecast"
        )
    
    with col2:
        st.write("") 
        forecast_btn = st.button("Get 5-Day Forecast", type="primary")
    
    if forecast_btn and forecast_city:
        get_and_display_forecast(forecast_city)
    
    elif hasattr(st.session_state.weather_app, 'current_weather') and st.session_state.weather_app.current_weather:
        if st.button("Show Forecast for Current City"):
            get_and_display_forecast(st.session_state.current_city)

def get_and_display_forecast(city):
    with st.spinner(f"Loading 5-day forecast for {city}..."):
        try:
            st.session_state.weather_app.search_city(city)
            forecast_data = st.session_state.weather_app.weather_api.get_forecast(city, 5)
            
            st.success(f"5-day forecast loaded for {city}")
            
            display_forecast_chart(forecast_data, city)
            display_forecast_details(forecast_data)
            
        except Exception as e:
            st.error(f"Error loading forecast: {str(e)}")

def display_forecast_chart(forecast_data, city):
    try:
        times = []
        temps = []
        
        for item in forecast_data['list']:
            times.append(datetime.fromtimestamp(item['dt']))
            temps.append(item['main']['temp'])
        
        df = pd.DataFrame({
            'DateTime': times,
            'Temperature': temps
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['Temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Temperature: %{y:.1f}°C<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"5-Day Temperature Forecast - {city}",
            xaxis_title="Date & Time",
            yaxis_title="Temperature (°C)",
            hovermode='x unified',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Max Temperature", f"{max(temps):.1f}°C")
        
        with col2:
            st.metric("Min Temperature", f"{min(temps):.1f}°C")
        
        with col3:
            avg_temp = sum(temps) / len(temps)
            st.metric("Average Temperature", f"{avg_temp:.1f}°C")
        
    except Exception as e:
        st.error(f"Error creating forecast chart: {str(e)}")

def display_forecast_details(forecast_data):
    try:
        st.subheader("Daily Forecast Details")
        
        daily_forecasts = {}
        
        for item in forecast_data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            
            daily_forecasts[date].append(item)
        
        for date, day_data in list(daily_forecasts.items())[:5]:  
            with st.expander(f"{date.strftime('%A, %B %d, %Y')}"):
 
                day_temps = [item['main']['temp'] for item in day_data]
                min_temp = min(day_temps)
                max_temp = max(day_temps)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Temperature Range:** {min_temp:.1f}°C - {max_temp:.1f}°C")
                    
                    conditions = [item['weather'][0]['description'] for item in day_data]
                    most_common = max(set(conditions), key=conditions.count)
                    st.write(f"**Main Condition:** {most_common.title()}")
                
                with col2:
                    avg_humidity = sum(item['main']['humidity'] for item in day_data) / len(day_data)
                    avg_wind = sum(item.get('wind', {}).get('speed', 0) for item in day_data) / len(day_data)
                    
                    st.write(f"**Average Humidity:** {avg_humidity:.0f}%")
                    st.write(f"**Average Wind:** {avg_wind:.1f} m/s")
                
                if date <= datetime.now().date() + timedelta(days=1):
                    st.write("**Hourly Breakdown:**")
                    
                    hourly_df = pd.DataFrame([
                        {
                            'Time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                            'Temp (°C)': f"{item['main']['temp']:.1f}",
                            'Condition': item['weather'][0]['description'].title(),
                            'Humidity (%)': item['main']['humidity']
                        }
                        for item in day_data
                    ])
                    
                    st.dataframe(hourly_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying forecast details: {str(e)}")

def show_favorites():
    st.header("Favorite Cities")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_favorite = st.text_input(
            "Add city to favorites:", 
            placeholder="Enter city name to add to favorites"
        )
    
    with col2:
        st.write("") 
        if st.button("Add to Favorites", type="primary"):
            if new_favorite:
                try:
                    st.session_state.weather_app.search_city(new_favorite)
                    success = st.session_state.weather_app.add_to_favorites(new_favorite)
                    
                    if success:
                        st.success(f"{new_favorite} added to favorites!")
                    else:
                        st.info(f"{new_favorite} is already in favorites")
                
                except Exception as e:
                    st.error(f"Cannot add {new_favorite}: {str(e)}")
    
    favorites = st.session_state.weather_app.get_favorites()
    
    if favorites:
        st.subheader(f"Your Favorite Cities ({len(favorites)} cities)")
        
        cols_per_row = 3
        
        for i in range(0, len(favorites), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, city in enumerate(favorites[i:i+cols_per_row]):
                with cols[j]:
                    if st.button(f"{city}\nClick for weather", key=f"fav_{city}", use_container_width=True):

                        st.session_state.current_city = city
                        search_weather(city)
                        st.success(f"Loading weather for {city}. Go to 'Current Weather' tab to view.")
        

        with st.expander("Remove Favorites"):
            st.write("Select cities to remove from favorites:")
            
            cities_to_remove = st.multiselect(
                "Choose cities to remove:",
                options=favorites,
                key="cities_to_remove"
            )
            
            if cities_to_remove and st.button("Remove Selected", type="secondary"):
                removed_count = 0
                for city in cities_to_remove:
                    if st.session_state.weather_app.data_manager.remove_favorite(city):
                        removed_count += 1
                
                if removed_count > 0:
                    st.success(f"Removed {removed_count} cities from favorites")
                    st.rerun()  
    
    else:
        st.info("No favorite cities yet.")
        st.write("Add cities above to save them as favorites for quick access!")

if __name__ == "__main__":
    main()