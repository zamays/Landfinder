"""Database module for storing and querying land listings."""

import sqlite3
from typing import List, Dict, Optional
import config


class Database:
    """Handles database operations for land listings."""

    def __init__(self, db_name: str = None):
        """Initialize database connection."""
        self.db_name = db_name or config.DATABASE_NAME
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create the listings table if it doesn't exist."""
        self.connect()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id TEXT UNIQUE,
            title TEXT,
            price TEXT,
            acres TEXT,
            price_per_acre TEXT,
            location TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            county TEXT,
            description TEXT,
            property_type TEXT,
            url TEXT,
            image_url TEXT,
            agent_name TEXT,
            agent_phone TEXT,
            date_listed TEXT,
            date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            latitude TEXT,
            longitude TEXT,
            features TEXT,
            additional_info TEXT
        )
        """
        
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print(f"Database '{self.db_name}' initialized successfully.")
        self.close()

    def insert_listing(self, listing: Dict) -> bool:
        """Insert a single listing into the database."""
        self.connect()
        
        try:
            insert_query = """
            INSERT OR REPLACE INTO listings (
                listing_id, title, price, acres, price_per_acre,
                location, address, city, state, zip_code, county,
                description, property_type, url, image_url,
                agent_name, agent_phone, date_listed,
                latitude, longitude, features, additional_info
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            values = (
                listing.get('listing_id'),
                listing.get('title'),
                listing.get('price'),
                listing.get('acres'),
                listing.get('price_per_acre'),
                listing.get('location'),
                listing.get('address'),
                listing.get('city'),
                listing.get('state'),
                listing.get('zip_code'),
                listing.get('county'),
                listing.get('description'),
                listing.get('property_type'),
                listing.get('url'),
                listing.get('image_url'),
                listing.get('agent_name'),
                listing.get('agent_phone'),
                listing.get('date_listed'),
                listing.get('latitude'),
                listing.get('longitude'),
                listing.get('features'),
                listing.get('additional_info')
            )
            
            self.cursor.execute(insert_query, values)
            self.conn.commit()
            self.close()
            return True
        except Exception as e:
            print(f"Error inserting listing: {e}")
            self.close()
            return False

    def insert_listings(self, listings: List[Dict]) -> int:
        """Insert multiple listings into the database."""
        count = 0
        for listing in listings:
            if self.insert_listing(listing):
                count += 1
        return count

    def query_all_listings(self) -> List[Dict]:
        """Query all listings from the database."""
        self.connect()
        self.cursor.execute("SELECT * FROM listings")
        rows = self.cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def query_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        """Query listings within a price range."""
        self.connect()
        query = "SELECT * FROM listings WHERE CAST(REPLACE(REPLACE(price, '$', ''), ',', '') AS REAL) BETWEEN ? AND ?"
        self.cursor.execute(query, (min_price, max_price))
        rows = self.cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def query_by_location(self, location: str) -> List[Dict]:
        """Query listings by location (city, state, or county)."""
        self.connect()
        query = """
        SELECT * FROM listings 
        WHERE city LIKE ? OR state LIKE ? OR county LIKE ? OR location LIKE ?
        """
        search_term = f"%{location}%"
        self.cursor.execute(query, (search_term, search_term, search_term, search_term))
        rows = self.cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def query_by_acres(self, min_acres: float, max_acres: float = None) -> List[Dict]:
        """Query listings by acreage."""
        self.connect()
        if max_acres:
            query = "SELECT * FROM listings WHERE CAST(REPLACE(acres, ',', '') AS REAL) BETWEEN ? AND ?"
            self.cursor.execute(query, (min_acres, max_acres))
        else:
            query = "SELECT * FROM listings WHERE CAST(REPLACE(acres, ',', '') AS REAL) >= ?"
            self.cursor.execute(query, (min_acres,))
        rows = self.cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """Get statistics about the database."""
        self.connect()
        stats = {}
        
        # Total listings
        self.cursor.execute("SELECT COUNT(*) FROM listings")
        stats['total_listings'] = self.cursor.fetchone()[0]
        
        # Listings by state
        self.cursor.execute("SELECT state, COUNT(*) as count FROM listings GROUP BY state ORDER BY count DESC")
        stats['by_state'] = [dict(row) for row in self.cursor.fetchall()]
        
        self.close()
        return stats
