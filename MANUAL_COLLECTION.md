# Manual Data Collection Guide

Since LandWatch.com blocks automated scraping, here are FREE methods to collect data:

## Method 1: Browser DevTools Console (Recommended)

1. Open landwatch.com in your browser (Chrome/Firefox)
2. Navigate to: https://www.landwatch.com/tx/land-for-sale
3. Open DevTools (F12 or Right-click → Inspect)
4. Go to the Console tab
5. Paste and run this JavaScript code:

```javascript
// Extract all listings from the current page
const listings = [];
document.querySelectorAll('[data-testid*="listing"], .property-card, .listing-card, .search-result-item').forEach((card, index) => {
    const listing = {
        listing_id: card.getAttribute('data-id') || card.getAttribute('id') || `listing_${Date.now()}_${index}`,
        title: card.querySelector('h2, h3, .title, [class*="title"]')?.textContent?.trim() || '',
        price: card.querySelector('[class*="price"]')?.textContent?.trim() || '',
        acres: card.querySelector('[class*="acre"]')?.textContent?.trim() || '',
        location: card.querySelector('[class*="location"], [class*="address"]')?.textContent?.trim() || '',
        url: card.querySelector('a')?.href || '',
        image_url: card.querySelector('img')?.src || ''
    };
    if (listing.title) listings.push(listing);
});

// Download as JSON
const dataStr = JSON.stringify(listings, null, 2);
const dataBlob = new Blob([dataStr], {type: 'application/json'});
const url = URL.createObjectURL(dataBlob);
const link = document.createElement('a');
link.href = url;
link.download = `landwatch_listings_${Date.now()}.json`;
link.click();

console.log(`Extracted ${listings.length} listings`);
```

6. The file will auto-download
7. Import it: `python import_data.py --json landwatch_listings_*.json`

## Method 2: Copy-Paste from Browser

1. Browse landwatch.com manually
2. For each property, collect:
   - Title
   - Price
   - Acres
   - Location
   - URL
3. Save in CSV format
4. Import: `python import_data.py --csv my_listings.csv`

## Method 3: Browser Extension

Use a browser extension like:
- **Web Scraper** (Chrome/Firefox extension)
- **Data Miner** (Chrome extension)
- **ParseHub** (Desktop app, free tier)

Configure it to extract: title, price, acres, location, URL from landwatch.com listings.

## Method 4: API Access (if available)

Contact LandWatch.com to request API access. If they provide an API key, we can integrate it into the scraper.

## Example CSV Format

```csv
listing_id,title,price,acres,location,url
1,"40 Acres Ranch Land","$320,000",40,"Austin, TX",https://...
2,"100 Acres Farm","$450,000",100,"Llano, TX",https://...
```

## Example JSON Format

```json
[
  {
    "listing_id": "1",
    "title": "40 Acres Ranch Land",
    "price": "$320,000",
    "acres": "40",
    "location": "Austin, TX",
    "url": "https://...",
    "image_url": "https://..."
  }
]
```

## Notes

- The JavaScript method works because you're manually visiting the site
- Bot detection doesn't apply to manual browser sessions
- You can paginate through listings manually and collect data
- Free browser extensions can automate the collection while you browse
- All methods are 100% free
