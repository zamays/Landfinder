"""Web scraper module for LandWatch.com."""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
import config
import re


class LandWatchScraper:
    """Scraper for LandWatch.com land listings."""

    def __init__(self):
        """Initialize the scraper."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def search_listings(self, state: str = None, max_pages: int = 1) -> List[Dict]:
        """
        Search for land listings.
        
        Args:
            state: State abbreviation (e.g., 'TX', 'CA')
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of listing dictionaries
        """
        listings = []
        
        # Build search URL
        if state:
            search_url = f"{config.BASE_URL}/{state.lower()}/land-for-sale"
        else:
            search_url = f"{config.BASE_URL}/land-for-sale"
        
        print(f"Starting scrape from: {search_url}")
        
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            
            # Add page parameter if not first page
            page_url = search_url if page == 1 else f"{search_url}/page-{page}"
            
            try:
                response = self.session.get(page_url, timeout=config.REQUEST_TIMEOUT)
                response.raise_for_status()
                
                # Parse the page
                page_listings = self._parse_search_page(response.text, page_url)
                listings.extend(page_listings)
                
                print(f"Found {len(page_listings)} listings on page {page}")
                
                # Be respectful - delay between requests
                if page < max_pages:
                    time.sleep(config.REQUEST_DELAY)
                    
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
        
        return listings

    def _parse_search_page(self, html: str, page_url: str) -> List[Dict]:
        """Parse a search results page and extract listings."""
        listings = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all listing cards
        # Note: The actual selectors will need to be adjusted based on the current
        # structure of landwatch.com. This is a general implementation.
        listing_cards = soup.find_all(['div', 'article'], class_=re.compile(r'.*property.*|.*listing.*|.*card.*', re.I))
        
        if not listing_cards:
            # Try alternative selectors
            listing_cards = soup.find_all('div', attrs={'data-property-id': True})
        
        if not listing_cards:
            # Try to find any divs that might contain property information
            listing_cards = soup.find_all('div', class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['propcard', 'prop-card', 'search-result']
            ))
        
        for card in listing_cards:
            try:
                listing = self._parse_listing_card(card)
                if listing and listing.get('title'):  # Only add if we got valid data
                    listings.append(listing)
            except Exception as e:
                print(f"Error parsing listing card: {e}")
                continue
        
        return listings

    def _parse_listing_card(self, card) -> Dict:
        """Parse a single listing card and extract information."""
        listing = {}
        
        # Try to extract listing ID
        listing_id = card.get('data-property-id') or card.get('id')
        if listing_id:
            listing['listing_id'] = str(listing_id)
        
        # Extract title
        title_elem = card.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'.*title.*|.*heading.*', re.I))
        if not title_elem:
            title_elem = card.find('a', href=re.compile(r'/.*-for-sale/.*'))
        if title_elem:
            listing['title'] = title_elem.get_text(strip=True)
        
        # Extract URL
        link_elem = card.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            if href.startswith('/'):
                listing['url'] = config.BASE_URL + href
            elif href.startswith('http'):
                listing['url'] = href
            else:
                listing['url'] = config.BASE_URL + '/' + href
        
        # Extract price
        price_elem = card.find(string=re.compile(r'\$[\d,]+'))
        if not price_elem:
            price_elem = card.find(class_=re.compile(r'.*price.*', re.I))
        if price_elem:
            price_text = price_elem if isinstance(price_elem, str) else price_elem.get_text(strip=True)
            listing['price'] = price_text
        
        # Extract acres
        acres_elem = card.find(string=re.compile(r'[\d,.]+ acre', re.I))
        if acres_elem:
            acres_text = acres_elem if isinstance(acres_elem, str) else acres_elem.get_text(strip=True)
            acres_match = re.search(r'([\d,]+\.?\d*)\s*acre', acres_text, re.I)
            if acres_match:
                listing['acres'] = acres_match.group(1)
        
        # Extract location
        location_elem = card.find(class_=re.compile(r'.*location.*|.*address.*|.*city.*', re.I))
        if location_elem:
            listing['location'] = location_elem.get_text(strip=True)
        
        # Try to extract city, state from location
        if 'location' in listing:
            location_parts = listing['location'].split(',')
            if len(location_parts) >= 2:
                listing['city'] = location_parts[0].strip()
                listing['state'] = location_parts[-1].strip()
        
        # Extract image URL
        img_elem = card.find('img')
        if img_elem:
            img_src = img_elem.get('src') or img_elem.get('data-src')
            if img_src:
                if img_src.startswith('//'):
                    listing['image_url'] = 'https:' + img_src
                elif img_src.startswith('/'):
                    listing['image_url'] = config.BASE_URL + img_src
                elif img_src.startswith('http'):
                    listing['image_url'] = img_src
        
        # Extract property type
        prop_type_elem = card.find(string=re.compile(r'(land|farm|ranch|lot)', re.I))
        if prop_type_elem:
            listing['property_type'] = prop_type_elem.strip()
        
        return listing

    def scrape_listing_details(self, listing_url: str) -> Dict:
        """
        Scrape detailed information from a specific listing page.
        
        Args:
            listing_url: URL of the listing detail page
            
        Returns:
            Dictionary with detailed listing information
        """
        try:
            response = self.session.get(listing_url, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            details = {}
            
            # Extract detailed description
            desc_elem = soup.find('div', class_=re.compile(r'.*description.*|.*detail.*', re.I))
            if desc_elem:
                details['description'] = desc_elem.get_text(strip=True)
            
            # Extract contact information
            agent_elem = soup.find(string=re.compile(r'agent|broker|seller', re.I))
            if agent_elem:
                parent = agent_elem.find_parent()
                if parent:
                    details['agent_name'] = parent.get_text(strip=True)
            
            # Extract phone number
            phone_elem = soup.find(string=re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'))
            if phone_elem:
                details['agent_phone'] = phone_elem.strip()
            
            # Extract coordinates if available
            coord_script = soup.find('script', string=re.compile(r'lat.*lng|latitude.*longitude', re.I))
            if coord_script:
                lat_match = re.search(r'lat(?:itude)?["\']?\s*[:=]\s*["\']?([-\d.]+)', coord_script.string, re.I)
                lng_match = re.search(r'lng|lon(?:gitude)?["\']?\s*[:=]\s*["\']?([-\d.]+)', coord_script.string, re.I)
                if lat_match:
                    details['latitude'] = lat_match.group(1)
                if lng_match:
                    details['longitude'] = lng_match.group(1)
            
            # Extract features list
            features_elem = soup.find_all('li', class_=re.compile(r'.*feature.*|.*amenity.*', re.I))
            if features_elem:
                features = [f.get_text(strip=True) for f in features_elem]
                details['features'] = ', '.join(features)
            
            time.sleep(config.REQUEST_DELAY)
            return details
            
        except Exception as e:
            print(f"Error scraping listing details from {listing_url}: {e}")
            return {}

    def close(self):
        """Close the session."""
        self.session.close()
