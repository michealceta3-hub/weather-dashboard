# Weather Dashboard 🌤️

A modern, responsive weather dashboard that fetches real-time weather data from multiple public APIs and displays comprehensive weather information including current conditions, forecasts, air quality, and interactive visualizations.

## Features ✨

### Current Implementation
- ✅ Real-time weather data from OpenWeatherMap API
- ✅ Current weather conditions (temp, humidity, wind speed)
- ✅ 5-day forecast with hourly breakdowns
- ✅ Multiple location search and favorites
- ✅ Temperature unit toggle (Celsius/Fahrenheit)
- ✅ Interactive charts (temperature, precipitation, wind)
- ✅ Weather alerts and warnings
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark/Light theme toggle
- ✅ Local storage for favorites and preferences
- ✅ Geolocation support
- ✅ Weather details (UV index, visibility, dew point)
- ✅ Air quality index (AQI)
- ✅ Sunrise/sunset times
- ✅ Wind direction visualization

### Planned Features
- 🔄 Radar and satellite imagery
- 🔄 Historical weather data
- 🔄 Weather comparison between cities
- 🔄 Severe weather notifications
- 🔄 Pollen forecast
- 🔄 UV index details
- 🔄 Marine forecast
- 🔄 Air quality details

## Tech Stack 💻

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **JavaScript (ES6+)** - Dynamic interactions
- **Chart.js** - Data visualization
- **Leaflet.js** - Interactive maps (future)
- **Axios** - HTTP client

### Backend
- **Python 3.9+** - Server-side logic
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin requests
- **Requests** - HTTP library
- **python-dotenv** - Environment configuration

### APIs
- **OpenWeatherMap API** - Weather data (primary)
- **Open-Meteo API** - Alternative free provider
- **Geolocation API** - Browser geolocation
- **Reverse Geocoding** - Location names from coordinates

### Deployment
- **Docker** - Containerization
- **Heroku/Vercel** - Cloud hosting (optional)
- **GitHub Pages** - Static frontend hosting

## Project Structure

```
weather-dashboard/
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── css/
│   │   ├── styles.css       # Main styles
│   │   ├── responsive.css   # Mobile responsive styles
│   │   └── themes.css       # Dark/light theme
│   ├── js/
│   │   ├── app.js           # Main application logic
│   │   ├── api.js           # API communication
│   │   ├── ui.js            # UI rendering
│   │   ├── charts.js        # Chart visualizations
│   │   ├── storage.js       # Local storage management
│   │   ├── geolocation.js   # Geolocation handling
│   │   └── utils.js         # Utility functions
│   └── assets/
│       ├── icons/           # Weather icons
│       └── images/          # Background images
├── backend/
│   ├── app.py               # Flask application
│   ├── config.py            # Configuration
│   ├── weather_api.py       # Weather API integration
│   ├── cache.py             # Caching layer
│   ├── models.py            # Data models
│   ├── routes.py            # API endpoints
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_api.py          # API tests
│   ├── test_weather.py      # Weather logic tests
│   └── test_frontend.py     # Frontend tests
├── docs/
│   ├── API.md               # API documentation
│   ├── SETUP.md             # Setup instructions
│   ├── DEPLOYMENT.md        # Deployment guide
│   └── ARCHITECTURE.md      # Architecture overview
├── docker/
│   ├── Dockerfile           # Docker configuration
│   └── docker-compose.yml   # Multi-container setup
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── package.json             # Frontend dependencies (if using npm)
└── README.md                # Project documentation
```

## Installation

### Prerequisites
- Python 3.9+
- Node.js 14+ (optional, for frontend build tools)
- OpenWeatherMap API key (free tier available)
- Modern web browser

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/michealceta3-hub/weather-dashboard.git
   cd weather-dashboard
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Create .env file
   cp .env.example .env
   # Edit .env and add your API key
   
   # Run server
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   # Open index.html in browser or use a local server
   python -m http.server 8000
   ```

4. **Access the Dashboard**
   - Frontend: http://localhost:8000
   - Backend API: http://localhost:5000

## API Documentation

### Weather Endpoints

#### Get Current Weather
```
GET /api/weather/current?city=London
```

#### Get Forecast
```
GET /api/weather/forecast?city=London&days=5
```

#### Search Cities
```
GET /api/locations/search?query=New
```

#### Get Air Quality
```
GET /api/weather/air-quality?lat=51.5074&lon=-0.1278
```

See [API.md](docs/API.md) for detailed documentation.

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
OPENWEATHERMAP_API_KEY=your_api_key_here
API_CACHE_TIME=600  # Cache duration in seconds

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

## Usage

### Search for a City
1. Enter city name in search bar
2. Select from suggestions
3. Dashboard updates with new location data

### Add to Favorites
1. Click heart icon on weather card
2. Saves to local storage
3. Quick access from favorites menu

### View Detailed Forecast
1. Click on any day in forecast
2. Expand hourly breakdown
3. View interactive temperature chart

### Change Settings
1. Click settings icon (gear)
2. Toggle temperature units
3. Toggle dark/light theme
4. Enable/disable notifications
5. Clear cache

### Enable Location Services
1. Click location icon
2. Allow browser geolocation
3. Dashboard auto-loads weather for current location

## Key Features Explained

### Real-time Weather Updates
- Automatic updates every 10 minutes
- Manual refresh button
- Timestamp of last update

### Temperature Unit Toggle
- Switch between Celsius and Fahrenheit
- Preference saved in local storage
- All temperatures updated instantly

### Weather Charts
- Temperature trend (24 hours)
- Precipitation probability
- Wind speed variations
- Interactive hover tooltips
- Responsive to screen size

### Favorites System
- Store up to 10 favorite locations
- Quick access menu
- Delete favorites individually
- Persist across sessions

### Dark Mode
- Automatic theme detection
- Manual toggle available
- Comfortable reading in low light
- Improved battery life on OLED screens

### Responsive Design
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)
- Touch-friendly interface

## API Sources

### OpenWeatherMap (Primary)
- **Current weather**: Temperature, humidity, wind, clouds
- **Forecast**: 5-day forecast with 3-hour intervals
- **Air quality**: PM2.5, PM10, O3, NO2, SO2, CO
- **Free tier**: 60 calls/minute, 5-day forecast
- **Sign up**: https://openweathermap.org/api

### Open-Meteo (Backup)
- **No API key required**
- **Hourly forecast**: 7 days
- **Daily forecast**: 35 days
- **Historical data**: 50 years back
- **Website**: https://open-meteo.com

## Security Considerations

✅ **Backend**: API keys stored in environment variables, never exposed to frontend
✅ **Frontend**: Uses CORS proxy to prevent direct API exposure
✅ **HTTPS**: Recommended for production
✅ **Rate limiting**: Implement on backend
✅ **Input validation**: All user inputs sanitized
✅ **CSRF protection**: Token-based requests

## Performance Optimization

- **Caching**: 10-minute cache on weather data
- **Lazy loading**: Images load on demand
- **Minification**: CSS and JS minified in production
- **Compression**: Gzip compression enabled
- **CDN**: Static assets served from CDN
- **Code splitting**: Modular JavaScript

## Testing

### Run Tests
```bash
# Backend tests
python -m pytest tests/

# Frontend tests (if using Jest)
npm test

# Coverage report
pytest --cov=backend tests/
```

### Manual Testing Checklist
- [ ] Search for multiple cities
- [ ] Add/remove favorites
- [ ] Toggle temperature units
- [ ] Toggle dark/light mode
- [ ] Test on mobile device
- [ ] Test on tablet
- [ ] Check all weather icons display
- [ ] Verify chart rendering
- [ ] Test error handling (invalid city)
- [ ] Test geolocation functionality

## Deployment

### Docker Deployment
```bash
# Build image
docker-compose build

# Run containers
docker-compose up -d

# Access at http://localhost
```

### Cloud Deployment (Heroku)
```bash
heroku login
heroku create your-weather-app
git push heroku main
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## Troubleshooting

### API Key Issues
- Verify API key in .env file
- Check API key is active on OpenWeatherMap
- Ensure API plan includes current features

### CORS Errors
- Verify backend is running
- Check CORS_ORIGINS in .env
- Ensure frontend URL matches CORS config

### No Data Displayed
- Check browser console for errors
- Verify API key is valid
- Check internet connection
- Clear browser cache

### Location Not Found
- Try exact city name
- Check spelling
- Use city + country format
- Check API rate limits

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Credits

- **OpenWeatherMap** - Weather data API
- **Chart.js** - Chart library
- **Leaflet** - Map library
- **Axios** - HTTP client
- **Flask** - Web framework

## Support

- 📧 Email: support@weather-dashboard.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📖 Docs: [Documentation](docs/)

## Roadmap

### v1.0 (Current)
- ✅ Current weather display
- ✅ 5-day forecast
- ✅ Multiple locations
- ✅ Dark mode
- ✅ Mobile responsive

### v1.1 (Upcoming)
- 🔄 Weather alerts
- 🔄 Air quality details
- 🔄 Hourly forecast view
- 🔄 Week view

### v1.2 (Future)
- 🔄 Radar integration
- 🔄 Historical weather
- 🔄 Weather comparison
- 🔄 Notifications

### v2.0 (Long-term)
- 🔄 Mobile app (React Native)
- 🔄 PWA support
- 🔄 Smartwatch app
- 🔄 Voice assistant integration

---

**Last Updated**: September 2, 2026
**Version**: 1.0.0
**Status**: Active Development

🌤️ **Check the weather, every day!**
