#!/usr/bin/env python3
"""Main script to run the LandWatch scraper and query the database."""

import argparse
from database import Database
from scraper import LandWatchScraper


def scrape_and_store(state: str = None, max_pages: int = 1, fetch_details: bool = False):
    """
    Scrape listings and store them in the database.
    
    Args:
        state: State abbreviation to search (e.g., 'TX', 'CA')
        max_pages: Maximum number of pages to scrape
        fetch_details: Whether to fetch detailed information for each listing
    """
    # Initialize database
    db = Database()
    db.create_tables()
    
    # Initialize scraper
    scraper = LandWatchScraper()
    
    try:
        # Scrape listings
        print(f"\n{'='*60}")
        print("Starting LandWatch scraper...")
        print(f"{'='*60}\n")
        
        listings = scraper.search_listings(state=state, max_pages=max_pages)
        print(f"\nScraped {len(listings)} listings total.")
        
        # Optionally fetch detailed information
        if fetch_details and listings:
            print("\nFetching detailed information for listings...")
            for i, listing in enumerate(listings):
                if listing.get('url'):
                    print(f"Fetching details for listing {i+1}/{len(listings)}...")
                    details = scraper.scrape_listing_details(listing['url'])
                    listing.update(details)
        
        # Store in database
        if listings:
            print(f"\nStoring {len(listings)} listings in database...")
            count = db.insert_listings(listings)
            print(f"Successfully stored {count} listings in the database.")
        else:
            print("No listings found to store.")
        
    finally:
        scraper.close()
    
    print(f"\n{'='*60}")
    print("Scraping completed!")
    print(f"{'='*60}\n")


def query_database(args):
    """Query the database based on command line arguments."""
    db = Database()
    
    if args.all:
        listings = db.query_all_listings()
        print(f"\nFound {len(listings)} total listings:\n")
        for listing in listings[:10]:  # Show first 10
            print(f"- {listing.get('title', 'N/A')}")
            print(f"  Price: {listing.get('price', 'N/A')}, Acres: {listing.get('acres', 'N/A')}")
            print(f"  Location: {listing.get('location', 'N/A')}")
            print(f"  URL: {listing.get('url', 'N/A')}\n")
        if len(listings) > 10:
            print(f"... and {len(listings) - 10} more listings")
    
    elif args.location:
        listings = db.query_by_location(args.location)
        print(f"\nFound {len(listings)} listings in {args.location}:\n")
        for listing in listings:
            print(f"- {listing.get('title', 'N/A')}")
            print(f"  Price: {listing.get('price', 'N/A')}, Acres: {listing.get('acres', 'N/A')}")
            print(f"  URL: {listing.get('url', 'N/A')}\n")
    
    elif args.price_min or args.price_max:
        min_price = args.price_min or 0
        max_price = args.price_max or float('inf')
        listings = db.query_by_price_range(min_price, max_price)
        print(f"\nFound {len(listings)} listings in price range ${min_price:,.0f} - ${max_price:,.0f}:\n")
        for listing in listings:
            print(f"- {listing.get('title', 'N/A')}")
            print(f"  Price: {listing.get('price', 'N/A')}, Acres: {listing.get('acres', 'N/A')}")
            print(f"  Location: {listing.get('location', 'N/A')}\n")
    
    elif args.acres_min:
        max_acres = args.acres_max if args.acres_max else None
        listings = db.query_by_acres(args.acres_min, max_acres)
        if max_acres:
            print(f"\nFound {len(listings)} listings with {args.acres_min}-{max_acres} acres:\n")
        else:
            print(f"\nFound {len(listings)} listings with {args.acres_min}+ acres:\n")
        for listing in listings:
            print(f"- {listing.get('title', 'N/A')}")
            print(f"  Price: {listing.get('price', 'N/A')}, Acres: {listing.get('acres', 'N/A')}")
            print(f"  Location: {listing.get('location', 'N/A')}\n")
    
    elif args.stats:
        stats = db.get_statistics()
        print(f"\n{'='*60}")
        print("Database Statistics")
        print(f"{'='*60}\n")
        print(f"Total listings: {stats['total_listings']}\n")
        print("Listings by state:")
        for state_info in stats['by_state'][:10]:
            print(f"  {state_info['state']}: {state_info['count']} listings")
        print()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='LandWatch.com scraper and database query tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape listings (1 page, any state)
  python main.py --scrape
  
  # Scrape listings from Texas (3 pages)
  python main.py --scrape --state TX --pages 3
  
  # Scrape with detailed information
  python main.py --scrape --state CA --pages 2 --details
  
  # Query all listings
  python main.py --query --all
  
  # Query by location
  python main.py --query --location "Austin"
  
  # Query by price range
  python main.py --query --price-min 50000 --price-max 200000
  
  # Query by acreage
  python main.py --query --acres-min 10 --acres-max 50
  
  # Show statistics
  python main.py --query --stats
        """
    )
    
    # Main action group
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--scrape', action='store_true',
                             help='Scrape listings from LandWatch.com')
    action_group.add_argument('--query', action='store_true',
                             help='Query the database')
    
    # Scraping options
    scrape_group = parser.add_argument_group('scraping options')
    scrape_group.add_argument('--state', type=str,
                             help='State abbreviation (e.g., TX, CA)')
    scrape_group.add_argument('--pages', type=int, default=1,
                             help='Number of pages to scrape (default: 1)')
    scrape_group.add_argument('--details', action='store_true',
                             help='Fetch detailed information for each listing')
    
    # Query options
    query_group = parser.add_argument_group('query options')
    query_group.add_argument('--all', action='store_true',
                            help='Show all listings')
    query_group.add_argument('--location', type=str,
                            help='Filter by location (city, state, or county)')
    query_group.add_argument('--price-min', type=float,
                            help='Minimum price')
    query_group.add_argument('--price-max', type=float,
                            help='Maximum price')
    query_group.add_argument('--acres-min', type=float,
                            help='Minimum acres')
    query_group.add_argument('--acres-max', type=float,
                            help='Maximum acres')
    query_group.add_argument('--stats', action='store_true',
                            help='Show database statistics')
    
    args = parser.parse_args()
    
    if args.scrape:
        scrape_and_store(
            state=args.state,
            max_pages=args.pages,
            fetch_details=args.details
        )
    elif args.query:
        if not any([args.all, args.location, args.price_min, args.price_max,
                   args.acres_min, args.stats]):
            parser.error('--query requires at least one query option (--all, --location, --price-min, etc.)')
        query_database(args)


if __name__ == '__main__':
    main()
