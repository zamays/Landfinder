#!/usr/bin/env python3
"""Test script to demonstrate the landFinder functionality with sample data."""

from database import Database


def create_sample_data():
    """Create sample listings for demonstration."""
    sample_listings = [
        {
            'listing_id': 'LW001',
            'title': '40 Acres Ranch Land in Hill Country',
            'price': '$320,000',
            'acres': '40',
            'price_per_acre': '$8,000',
            'location': 'Fredericksburg, TX',
            'city': 'Fredericksburg',
            'state': 'TX',
            'county': 'Gillespie County',
            'description': 'Beautiful 40-acre ranch property with rolling hills, oak trees, and stunning Hill Country views.',
            'property_type': 'Ranch',
            'url': 'https://www.landwatch.com/sample-listing-1',
            'image_url': 'https://example.com/image1.jpg',
            'agent_name': 'John Smith',
            'agent_phone': '(512) 555-0100',
            'latitude': '30.2672',
            'longitude': '-98.8738',
            'features': 'Fenced, Water well, Electricity, Mountain views',
        },
        {
            'listing_id': 'LW002',
            'title': '100 Acres Hunting Land',
            'price': '$450,000',
            'acres': '100',
            'price_per_acre': '$4,500',
            'location': 'Llano, TX',
            'city': 'Llano',
            'state': 'TX',
            'county': 'Llano County',
            'description': 'Prime hunting property with abundant wildlife including deer, turkey, and hogs.',
            'property_type': 'Hunting Land',
            'url': 'https://www.landwatch.com/sample-listing-2',
            'image_url': 'https://example.com/image2.jpg',
            'agent_name': 'Sarah Johnson',
            'agent_phone': '(830) 555-0200',
            'latitude': '30.7527',
            'longitude': '-98.6751',
            'features': 'High fence, Deer blind, Food plots, Water sources',
        },
        {
            'listing_id': 'LW003',
            'title': '5 Acres Residential Lot',
            'price': '$85,000',
            'acres': '5',
            'price_per_acre': '$17,000',
            'location': 'Austin, TX',
            'city': 'Austin',
            'state': 'TX',
            'county': 'Travis County',
            'description': 'Cleared 5-acre residential lot ready for your dream home, close to Austin.',
            'property_type': 'Residential Land',
            'url': 'https://www.landwatch.com/sample-listing-3',
            'image_url': 'https://example.com/image3.jpg',
            'agent_name': 'Mike Davis',
            'agent_phone': '(512) 555-0300',
            'latitude': '30.2672',
            'longitude': '-97.7431',
            'features': 'Cleared, Utilities available, Paved road access',
        },
        {
            'listing_id': 'LW004',
            'title': '200 Acres Farm Land with Creek',
            'price': '$1,200,000',
            'acres': '200',
            'price_per_acre': '$6,000',
            'location': 'Napa, CA',
            'city': 'Napa',
            'state': 'CA',
            'county': 'Napa County',
            'description': 'Stunning 200-acre vineyard-ready property with year-round creek and valley views.',
            'property_type': 'Farm',
            'url': 'https://www.landwatch.com/sample-listing-4',
            'image_url': 'https://example.com/image4.jpg',
            'agent_name': 'Emily Chen',
            'agent_phone': '(707) 555-0400',
            'latitude': '38.2975',
            'longitude': '-122.2869',
            'features': 'Creek, Vineyard potential, Barn, Well water',
        },
        {
            'listing_id': 'LW005',
            'title': '25 Acres Mountain Property',
            'price': '$175,000',
            'acres': '25',
            'price_per_acre': '$7,000',
            'location': 'Durango, CO',
            'city': 'Durango',
            'state': 'CO',
            'county': 'La Plata County',
            'description': 'Secluded mountain property with pine and aspen trees, perfect for a cabin retreat.',
            'property_type': 'Recreational Land',
            'url': 'https://www.landwatch.com/sample-listing-5',
            'image_url': 'https://example.com/image5.jpg',
            'agent_name': 'Robert Martinez',
            'agent_phone': '(970) 555-0500',
            'latitude': '37.2753',
            'longitude': '-107.8801',
            'features': 'Mountain views, Forest, Wildlife, Off-grid potential',
        },
    ]
    
    return sample_listings


def main():
    """Run the test with sample data."""
    print("="*70)
    print("LandFinder Test Script - Demonstrating Functionality")
    print("="*70)
    print()
    
    # Initialize database
    print("1. Initializing database...")
    db = Database()
    db.create_tables()
    print()
    
    # Create and insert sample data
    print("2. Creating sample listings...")
    sample_listings = create_sample_data()
    print(f"   Created {len(sample_listings)} sample listings")
    print()
    
    print("3. Storing listings in database...")
    count = db.insert_listings(sample_listings)
    print(f"   Successfully stored {count} listings")
    print()
    
    # Demonstrate queries
    print("4. Demonstrating query functionality:")
    print()
    
    # Query all
    print("   a) All listings:")
    all_listings = db.query_all_listings()
    print(f"      Total: {len(all_listings)} listings")
    for listing in all_listings[:3]:
        print(f"      - {listing['title']}")
        print(f"        Price: {listing['price']}, Acres: {listing['acres']}")
        print(f"        Location: {listing['location']}")
    print()
    
    # Query by location
    print("   b) Listings in Texas:")
    tx_listings = db.query_by_location("TX")
    print(f"      Found: {len(tx_listings)} listings")
    for listing in tx_listings[:2]:
        print(f"      - {listing['title']} - {listing['location']}")
    print()
    
    # Query by price range
    print("   c) Listings priced between $100k and $500k:")
    price_listings = db.query_by_price_range(100000, 500000)
    print(f"      Found: {len(price_listings)} listings")
    for listing in price_listings:
        print(f"      - {listing['title']}: {listing['price']}")
    print()
    
    # Query by acreage
    print("   d) Listings with 20+ acres:")
    acre_listings = db.query_by_acres(20)
    print(f"      Found: {len(acre_listings)} listings")
    for listing in acre_listings:
        print(f"      - {listing['title']}: {listing['acres']} acres")
    print()
    
    # Statistics
    print("   e) Database statistics:")
    stats = db.get_statistics()
    print(f"      Total listings: {stats['total_listings']}")
    print("      By state:")
    for state_info in stats['by_state']:
        print(f"        {state_info['state']}: {state_info['count']} listings")
    print()
    
    print("="*70)
    print("Test completed successfully!")
    print("="*70)
    print()
    print("You can now use the main.py script to:")
    print("  - Scrape real data: python main.py --scrape --state TX --pages 2")
    print("  - Query the database: python main.py --query --location Austin")
    print("  - See statistics: python main.py --query --stats")
    print()


if __name__ == '__main__':
    main()
