#!/usr/bin/env python3
"""Import listings from various sources into the database."""

import argparse
import json
import csv
from database import Database
from typing import List, Dict


def import_from_json(file_path: str) -> List[Dict]:
    """Import listings from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Handle both single listing and list of listings
    if isinstance(data, list):
        return data
    else:
        return [data]


def import_from_csv(file_path: str) -> List[Dict]:
    """Import listings from CSV file."""
    listings = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            listings.append(dict(row))
    return listings


def main():
    """Main entry point for the import script."""
    parser = argparse.ArgumentParser(
        description='Import land listings from JSON or CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from JSON file
  python import_data.py --json listings.json
  
  # Import from CSV file
  python import_data.py --csv listings.csv

JSON Format:
  Single listing:
  {
    "listing_id": "12345",
    "title": "40 Acres Ranch Land",
    "price": "$320,000",
    "acres": "40",
    ...
  }
  
  Multiple listings:
  [
    {"listing_id": "12345", ...},
    {"listing_id": "67890", ...}
  ]

CSV Format:
  listing_id,title,price,acres,location,...
  12345,"40 Acres Ranch Land","$320,000",40,"Austin, TX",...
        """
    )
    
    parser.add_argument('--json', type=str, help='Path to JSON file with listings')
    parser.add_argument('--csv', type=str, help='Path to CSV file with listings')
    
    args = parser.parse_args()
    
    if not args.json and not args.csv:
        parser.error('Must specify either --json or --csv')
    
    # Import listings
    print("="*60)
    print("Land Listing Importer")
    print("="*60)
    print()
    
    try:
        if args.json:
            print(f"Importing from JSON file: {args.json}")
            listings = import_from_json(args.json)
        else:
            print(f"Importing from CSV file: {args.csv}")
            listings = import_from_csv(args.csv)
        
        print(f"Found {len(listings)} listings to import")
        print()
        
        # Initialize database
        db = Database()
        db.create_tables()
        
        # Import listings
        count = db.insert_listings(listings)
        
        print(f"✓ Successfully imported {count} listings into database")
        print()
        print("You can now query the database using:")
        print("  python main.py --query --all")
        print("  python main.py --query --stats")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
