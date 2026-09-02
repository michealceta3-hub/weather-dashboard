import requests
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class WeatherAPI:
    """Wrapper for OpenWeatherMap and Open-Meteo APIs"""
    
    def __init__(self):
        self.openweather_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.openweather_base_url = 'https://api.openweathermap.org'
        self.openmeteo_base_url = 'https://api.open-meteo.com/v1'
        self.geocoding_url = 'https://geocoding-api.open-meteo.com/v1'
        self.timeout = 10  # Request timeout in seconds
    
    def get_current_weather(self, city: str) -> Optional[Dict]:
        """Get current weather for a city"""
        try:
            # Get coordinates first
            coords = self._get_coordinates(city)
            if not coords:
                return None
            
            lat, lon = coords
            
            # Fetch current weather from OpenWeatherMap
            url = f"{self.openweather_base_url}/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Format response
            return self._format_current_weather(data)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching current weather: {str(e)}")
            return None
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict]:
        """Get weather forecast for a city"""
        try:
            # Get coordinates first
            coords = self._get_coordinates(city)
            if not coords:
                return None
            
            lat, lon = coords
            
            # Fetch forecast from OpenWeatherMap
            url = f"{self.openweather_base_url}/data/2.5/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Format response
            return self._format_forecast(data)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            return None
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """Get air quality index for coordinates"""
        try:
            url = f"{self.openweather_base_url}/data/3.0/uvi"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            return self._format_air_quality(data)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching air quality: {str(e)}")
            return None
    
    def search_locations(self, query: str) -> List[Dict]:
        """Search for locations by name"""
        try:
            url = f"{self.geocoding_url}/search"
            params = {
                'name': query,
                'count': 10,
                'language': 'en',
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'results' in data:
                for result in data['results']:
                    results.append({
                        'name': result.get('name'),
                        'country': result.get('country'),
                        'latitude': result.get('latitude'),
                        'longitude': result.get('longitude'),
                        'admin1': result.get('admin1'),
                        'timezone': result.get('timezone')
                    })
            
            return results
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching locations: {str(e)}")
            return []
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Get location name from coordinates"""
        try:
            url = f"{self.geocoding_url}/reverse"
            params = {
                'latitude': lat,
                'longitude': lon,
                'language': 'en'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                return {
                    'name': result.get('name'),
                    'country': result.get('country'),
                    'admin1': result.get('admin1'),
                    'latitude': lat,
                    'longitude': lon
                }
            
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reverse geocoding: {str(e)}")
            return None
    
    def get_alerts(self, city: Optional[str] = None, lat: Optional[float] = None, 
                   lon: Optional[float] = None) -> List[Dict]:
        """Get weather alerts for a location"""
        try:
            if not lat or not lon:
                if not city:
                    return []
                coords = self._get_coordinates(city)
                if not coords:
                    return []
                lat, lon = coords
            
            url = f"{self.openweather_base_url}/data/3.0/alerts"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            alerts = []
            if 'alerts' in data:
                for alert in data['alerts']:
                    alerts.append({
                        'event': alert.get('event'),
                        'start': alert.get('start'),
                        'end': alert.get('end'),
                        'description': alert.get('description'),
                        'tags': alert.get('tags', [])
                    })
            
            return alerts
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching alerts: {str(e)}")
            return []
    
    # ==================== Private Methods ====================
    
    def _get_coordinates(self, city: str) -> Optional[tuple]:
        """Get coordinates for a city name"""
        try:
            url = f"{self.geocoding_url}/search"
            params = {
                'name': city,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                return (result['latitude'], result['longitude'])
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            return None
    
    def _format_current_weather(self, data: Dict) -> Dict:
        """Format OpenWeatherMap current weather response"""
        return {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': data.get('main', {}).get('temp'),
            'feels_like': data.get('main', {}).get('feels_like'),
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'description': data.get('weather', [{}])[0].get('description'),
            'icon': data.get('weather', [{}])[0].get('icon'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'wind_direction': data.get('wind', {}).get('deg'),
            'cloudiness': data.get('clouds', {}).get('all'),
            'visibility': data.get('visibility'),
            'sunrise': data.get('sys', {}).get('sunrise'),
            'sunset': data.get('sys', {}).get('sunset'),
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_forecast(self, data: Dict) -> Dict:
        """Format OpenWeatherMap forecast response"""
        forecasts = []
        for forecast in data.get('list', []):
            forecasts.append({
                'timestamp': forecast.get('dt'),
                'temperature': forecast.get('main', {}).get('temp'),
                'feels_like': forecast.get('main', {}).get('feels_like'),
                'humidity': forecast.get('main', {}).get('humidity'),
                'pressure': forecast.get('main', {}).get('pressure'),
                'description': forecast.get('weather', [{}])[0].get('description'),
                'icon': forecast.get('weather', [{}])[0].get('icon'),
                'wind_speed': forecast.get('wind', {}).get('speed'),
                'wind_direction': forecast.get('wind', {}).get('deg'),
                'cloudiness': forecast.get('clouds', {}).get('all'),
                'rain_probability': forecast.get('pop'),
                'rain_volume': forecast.get('rain', {}).get('3h', 0)
            })
        
        return {
            'city': data.get('city', {}).get('name'),
            'country': data.get('city', {}).get('country'),
            'forecasts': forecasts
        }
    
    def _format_air_quality(self, data: Dict) -> Dict:
        """Format air quality response"""
        return {
            'uv_index': data.get('value'),
            'timestamp': datetime.now().isoformat()
        }
