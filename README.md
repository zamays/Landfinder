# landFinder

A helpful application for scraping real estate websites so you can search through the data locally.

## Features

- **Web Scraper**: Scrapes land listings from LandWatch.com (with anti-bot detection)
- **Manual Import**: Import data from JSON/CSV files
- **Local Database**: Stores all listing data in a SQLite database
- **Query Interface**: Easy-to-use command-line interface for querying listings
- **Flexible Filtering**: Filter by location, price, acreage, and more

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zamays/landFinder.git
cd landFinder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚠️ Important Note About Web Scraping

LandWatch.com implements advanced bot detection that blocks most automated scraping attempts. This project includes:
- **undetected-chromedriver** for bypassing some detection
- **Manual data collection methods** (FREE and effective)
- **Data import tools** for JSON/CSV files

**Recommended Approach**: Use the manual collection methods described in `MANUAL_COLLECTION.md` - they're free, legal, and actually work!

## Usage

### Method 1: Manual Data Collection (Recommended - FREE & Works!)

See [MANUAL_COLLECTION.md](MANUAL_COLLECTION.md) for detailed instructions on:
- Using browser DevTools to extract data (works perfectly!)
- Browser extensions for data collection
- CSV export methods

Then import your data:
```bash
python import_data.py --json your_listings.json
python import_data.py --csv your_listings.csv
```

### Method 2: Automated Scraping (May Be Blocked)

Attempt automated scraping with anti-bot detection:

```bash
# Scrape 1 page of listings (any state)
python main.py --scrape

# Scrape 3 pages from Texas
python main.py --scrape --state TX --pages 3

# Scrape 2 pages from California with detailed information
python main.py --scrape --state CA --pages 2 --details
```

**Note**: The `--details` flag will fetch detailed information for each listing (description, agent info, coordinates, etc.), but this will take significantly longer.

### Querying the Database

Once you've scraped some listings, you can query the local database:

```bash
# Show all listings
python main.py --query --all

# Search by location
python main.py --query --location "Austin"
python main.py --query --location "Texas"

# Filter by price range
python main.py --query --price-min 50000 --price-max 200000

# Filter by acreage
python main.py --query --acres-min 10 --acres-max 50

# Show database statistics
python main.py --query --stats
```

## Database Schema

The database stores listings with the following fields:

- **listing_id**: Unique identifier for the listing
- **title**: Property title
- **price**: Listing price
- **acres**: Property size in acres
- **price_per_acre**: Price per acre
- **location**: Full location string
- **address**, **city**, **state**, **zip_code**, **county**: Location details
- **description**: Property description
- **property_type**: Type of property (land, farm, ranch, etc.)
- **url**: Link to the listing
- **image_url**: Main property image
- **agent_name**, **agent_phone**: Contact information
- **date_listed**: When the property was listed
- **date_scraped**: When the data was scraped
- **latitude**, **longitude**: Coordinates
- **features**: Property features and amenities
- **additional_info**: Other relevant information

## Configuration

You can modify scraper settings in `config.py`:

- `DATABASE_NAME`: Name of the SQLite database file
- `REQUEST_TIMEOUT`: HTTP request timeout in seconds
- `REQUEST_DELAY`: Delay between requests (be respectful to the website)

## Notes

- The scraper respects the website by including delays between requests
- Scraping behavior may need to be adjusted if the website structure changes
- Always check the website's terms of service and robots.txt before scraping
- The database file (`landwatch.db`) will be created automatically on first run

## License

See LICENSE file for details.
