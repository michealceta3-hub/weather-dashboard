from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from weather_api import WeatherAPI
from cache import Cache
from models import WeatherData
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

# Initialize services
weather_api = WeatherAPI()
cache = Cache(duration=int(os.getenv('API_CACHE_TIME', 600)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== API Endpoints ====================

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Weather Dashboard API is running',
        'version': '1.0.0'
    }), 200

# Current Weather
@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather for a location"""
    try:
        city = request.args.get('city')
        if not city:
            return jsonify({'error': 'City parameter required'}), 400
        
        # Check cache
        cache_key = f'current_{city.lower()}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Fetch from API
        weather_data = weather_api.get_current_weather(city)
        if not weather_data:
            return jsonify({'error': 'City not found'}), 404
        
        # Cache the result
        cache.set(cache_key, weather_data)
        
        return jsonify(weather_data), 200
    
    except Exception as e:
        logger.error(f"Error fetching current weather: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Forecast
@app.route('/api/weather/forecast', methods=['GET'])
def get_forecast():
    """Get weather forecast for a location"""
    try:
        city = request.args.get('city')
        days = request.args.get('days', default=5, type=int)
        
        if not city:
            return jsonify({'error': 'City parameter required'}), 400
        
        # Check cache
        cache_key = f'forecast_{city.lower()}_{days}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Fetch from API
        forecast_data = weather_api.get_forecast(city, days)
        if not forecast_data:
            return jsonify({'error': 'City not found'}), 404
        
        # Cache the result
        cache.set(cache_key, forecast_data)
        
        return jsonify(forecast_data), 200
    
    except Exception as e:
        logger.error(f"Error fetching forecast: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Air Quality
@app.route('/api/weather/air-quality', methods=['GET'])
def get_air_quality():
    """Get air quality index for coordinates"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Check cache
        cache_key = f'aqi_{lat}_{lon}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Fetch from API
        aqi_data = weather_api.get_air_quality(lat, lon)
        if not aqi_data:
            return jsonify({'error': 'Unable to fetch air quality data'}), 500
        
        # Cache the result
        cache.set(cache_key, aqi_data)
        
        return jsonify(aqi_data), 200
    
    except Exception as e:
        logger.error(f"Error fetching air quality: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Location Search
@app.route('/api/locations/search', methods=['GET'])
def search_locations():
    """Search for locations by name"""
    try:
        query = request.args.get('query')
        if not query or len(query) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        # Check cache
        cache_key = f'search_{query.lower()}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Search locations
        locations = weather_api.search_locations(query)
        
        # Cache the result
        cache.set(cache_key, locations)
        
        return jsonify(locations), 200
    
    except Exception as e:
        logger.error(f"Error searching locations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Reverse Geocoding
@app.route('/api/locations/reverse', methods=['GET'])
def reverse_geocode():
    """Get location name from coordinates"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Check cache
        cache_key = f'reverse_{lat}_{lon}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data), 200
        
        # Reverse geocode
        location = weather_api.reverse_geocode(lat, lon)
        
        # Cache the result
        cache.set(cache_key, location)
        
        return jsonify(location), 200
    
    except Exception as e:
        logger.error(f"Error reverse geocoding: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Weather Alerts
@app.route('/api/weather/alerts', methods=['GET'])
def get_alerts():
    """Get weather alerts for a location"""
    try:
        city = request.args.get('city')
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not city and (lat is None or lon is None):
            return jsonify({'error': 'City or coordinates required'}), 400
        
        # Fetch alerts
        alerts = weather_api.get_alerts(city, lat, lon)
        
        return jsonify(alerts), 200
    
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Cache Statistics
@app.route('/api/cache/stats', methods=['GET'])
def cache_stats():
    """Get cache statistics"""
    try:
        stats = cache.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Clear Cache
@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cached data"""
    try:
        cache.clear()
        return jsonify({'message': 'Cache cleared successfully'}), 200
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ==================== Main ====================

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🌤️  Starting Weather Dashboard API on {host}:{port}")
    print(f"📡 OpenWeatherMap API Key: {'✓' if os.getenv('OPENWEATHERMAP_API_KEY') else '✗'}")
    
    app.run(host=host, port=port, debug=debug)
