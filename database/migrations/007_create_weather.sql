-- Milestone #35: Weather Table Migration

DROP TABLE IF EXISTS weather CASCADE;

CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    location_city VARCHAR(100) NOT NULL,
    temperature_celsius DECIMAL(5, 1),
    humidity_percent DECIMAL(5, 2),
    wind_speed_kmh DECIMAL(6, 2),
    wind_direction VARCHAR(5),
    condition VARCHAR(20),
    visibility_km DECIMAL(6, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_weather_condition CHECK (condition IN ('clear', 'cloudy', 'rain', 'snow', 'fog', 'storm')),
    CONSTRAINT chk_temp_range CHECK (temperature_celsius BETWEEN -50 AND 60),
    CONSTRAINT chk_humidity_range CHECK (humidity_percent BETWEEN 0 AND 100)
);

CREATE INDEX idx_weather_timestamp ON weather(timestamp);
CREATE INDEX idx_weather_location ON weather(location_city);
CREATE INDEX idx_weather_date_location ON weather(timestamp, location_city);

COMMENT ON TABLE weather IS 'Weather data for delivery locations';