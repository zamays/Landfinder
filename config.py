"""Configuration settings for the LandWatch scraper."""

# Database settings
DATABASE_NAME = "landwatch.db"

# Scraper settings
BASE_URL = "https://www.landwatch.com"
SEARCH_URL = f"{BASE_URL}/search"

# Default search parameters
DEFAULT_SEARCH_PARAMS = {
    "type": "land",
}

# Scraping settings
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Delay between requests (in seconds) to be respectful
REQUEST_DELAY = 2
