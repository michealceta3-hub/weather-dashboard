from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class WeatherData:
    """Weather data model"""
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    wind_direction: int
    cloudiness: int
    visibility: int
    sunrise: int
    sunset: int
    timestamp: datetime

@dataclass
class ForecastData:
    """Forecast data model"""
    city: str
    country: str
    forecasts: List[dict]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class LocationData:
    """Location data model"""
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: Optional[str] = None
    admin1: Optional[str] = None

@dataclass
class AirQualityData:
    """Air quality data model"""
    aqi: float
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    o3: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AlertData:
    """Weather alert data model"""
    event: str
    start: int
    end: int
    description: str
    tags: List[str]
