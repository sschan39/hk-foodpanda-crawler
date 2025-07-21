"""
FoodPanda Hong Kong Restaurant Crawler - Coordinate Input Version
Allows users to directly input coordinates to add search areas

This script crawls FoodPanda Hong Kong restaurant data using coordinate-based searches.
Users can either select from predefined popular locations or input custom coordinates.
The script includes deduplication and exports results to Excel with multiple sheets.
"""

import json
import requests
import time
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, asdict
import re


@dataclass
class Restaurant:
    """Restaurant data structure - contains all restaurant information fields"""
    code: str                           # Unique restaurant identifier
    name: str                          # Restaurant name
    rating: Optional[float] = None     # Average rating (0-5 scale)
    rating_count: Optional[int] = None # Number of reviews
    delivery_time: Optional[str] = None # Estimated delivery time
    minimum_order: Optional[float] = None # Minimum order amount
    delivery_fee: Optional[str] = None  # Delivery fee information
    address: Optional[str] = None       # Full address
    phone: Optional[str] = None         # Contact phone number
    is_open: Optional[bool] = None      # Current operating status
    cuisines: str = ""                  # Cuisine types (comma-separated)
    budget_range: Optional[int] = None  # Price range category
    chain_name: Optional[str] = None    # Chain brand name if applicable
    longitude: Optional[float] = None   # GPS longitude coordinate
    latitude: Optional[float] = None    # GPS latitude coordinate
    area: Optional[str] = None          # Search area name
    distance: Optional[float] = None    # Distance from search point
    is_delivery_enabled: Optional[bool] = None # Delivery availability
    is_pickup_enabled: Optional[bool] = None   # Pickup availability
    delivery_provider: Optional[str] = None    # Delivery service provider
    hero_image: Optional[str] = None           # Main restaurant image URL
    website: Optional[str] = None              # Restaurant website
    legal_name: Optional[str] = None           # Legal business name
    available_in: Optional[str] = None         # Service availability info
    tags: str = ""                            # Restaurant tags (comma-separated)


def validate_coordinates(longitude: float, latitude: float) -> bool:
    """
    Validate if coordinates are within Hong Kong boundaries
    
    Args:
        longitude: GPS longitude coordinate
        latitude: GPS latitude coordinate
        
    Returns:
        bool: True if coordinates are within HK bounds, False otherwise
    """
    # Hong Kong approximate boundaries
    # Longitude: 113.8 - 114.5
    # Latitude: 22.0 - 22.6
    if 113.8 <= longitude <= 114.5 and 22.0 <= latitude <= 22.6:
        return True
    return False


def parse_coordinate_input(coord_input: str) -> Optional[Tuple[float, float, str]]:
    """
    Parse coordinate input string, supports multiple formats:
    - "114.1578,22.2842,Central"
    - "114.1578, 22.2842, Central Business District"  
    - "114.1578 22.2842 Central"
    
    Args:
        coord_input: String containing coordinates and optional area name
        
    Returns:
        Optional[Tuple[float, float, str]]: (longitude, latitude, area_name) or None if invalid
    """
    try:
        # Remove extra whitespace
        coord_input = coord_input.strip()
        
        # Try to split (supports comma or space separation)
        if ',' in coord_input:
            parts = [part.strip() for part in coord_input.split(',')]
        else:
            parts = coord_input.split()
        
        if len(parts) < 2:
            return None
        
        # Parse longitude and latitude
        try:
            longitude = float(parts[0])
            latitude = float(parts[1])
        except ValueError:
            return None
        
        # Validate coordinate range
        if not validate_coordinates(longitude, latitude):
            return None
        
        # Parse area name (if provided)
        area_name = "Custom Location"
        if len(parts) > 2:
            area_name = ' '.join(parts[2:]).strip()
        
        return (longitude, latitude, area_name)
        
    except Exception:
        return None


def parse_restaurant_data(item: Dict, area_name: str) -> Optional[Restaurant]:
    """
    Parse individual restaurant data from API response
    
    Args:
        item: Restaurant data dictionary from API
        area_name: Name of the search area
        
    Returns:
        Optional[Restaurant]: Restaurant object or None if parsing fails
    """
    try:
        # Basic identifiers - skip if missing
        code = item.get('code', '')
        name = item.get('name', '')
        if not code or not name:
            return None

        # Rating information
        rating = item.get('rating')
        rating_count = item.get('review_number')

        # Location data
        longitude = item.get('longitude')
        latitude = item.get('latitude')
        distance = item.get('distance')

        # Order information
        minimum_order = item.get('minimum_order_amount')
        
        # Get availability info from metadata
        metadata = item.get('metadata', {})
        available_in = metadata.get('available_in')
        is_delivery_available = metadata.get('is_delivery_available', True)
        is_pickup_available = metadata.get('is_pickup_available', True)
        
        # Address information
        address = item.get('address', '')
        if item.get('address_line2'):
            address += f", {item.get('address_line2')}"
        
        # Contact and basic info
        phone = item.get('customer_phone', '')
        budget_range = item.get('budget')
        
        # Chain information
        chain_name = None
        chain_data = item.get('chain')
        if chain_data and isinstance(chain_data, dict):
            chain_name = chain_data.get('name')

        # Parse cuisine types
        cuisines_list = []
        characteristics = item.get('characteristics', {})
        if 'cuisines' in characteristics:
            for cuisine in characteristics['cuisines']:
                if isinstance(cuisine, dict):
                    cuisine_name = cuisine.get('name', '').strip()
                    if cuisine_name:
                        cuisines_list.append(cuisine_name)
        
        # Fallback to direct cuisines field
        if not cuisines_list and 'cuisines' in item:
            for cuisine in item['cuisines']:
                if isinstance(cuisine, dict):
                    cuisine_name = cuisine.get('name', '').strip()
                    if cuisine_name:
                        cuisines_list.append(cuisine_name)
        
        cuisines_str = ', '.join(cuisines_list)

        # Parse tags information
        tags_list = []
        if 'tags' in item and isinstance(item['tags'], list):
            for tag in item['tags']:
                if isinstance(tag, dict):
                    tag_text = tag.get('text', '').strip()
                    if tag_text:
                        tags_list.append(tag_text)
        tags_str = ', '.join(tags_list)

        # Additional information
        delivery_provider = item.get('delivery_provider')
        hero_image = item.get('hero_image')
        website = item.get('website')
        
        # Legal name information
        legal_name = None
        vendor_legal = item.get('vendor_legal_information', {})
        if vendor_legal:
            legal_name = vendor_legal.get('legal_name')

        # Operating status
        is_open = item.get('is_active', True) and not metadata.get('is_temporary_closed', False)

        # Create Restaurant object with all parsed data
        restaurant = Restaurant(
            code=code,
            name=name,
            rating=rating,
            rating_count=rating_count,
            delivery_time=None,
            minimum_order=minimum_order,
            delivery_fee=None,
            address=address,
            phone=phone,
            is_open=is_open,
            cuisines=cuisines_str,
            budget_range=budget_range,
            chain_name=chain_name,
            longitude=longitude,
            latitude=latitude,
            area=area_name,
            distance=distance,
            is_delivery_enabled=is_delivery_available,
            is_pickup_enabled=is_pickup_available,
            delivery_provider=delivery_provider,
            hero_image=hero_image,
            website=website,
            legal_name=legal_name,
            available_in=available_in,
            tags=tags_str
        )
        
        return restaurant
    
    except Exception as e:
        print(f"⚠️  Error parsing restaurant data ({item.get('name', 'Unknown')}): {e}")
        return None


def get_restaurants_by_location(longitude: float, latitude: float, area_name: str, limit: int = 200) -> List[Restaurant]:
    """
    Fetch restaurant data from a specific location using FoodPanda API
    
    Args:
        longitude: GPS longitude coordinate
        latitude: GPS latitude coordinate  
        area_name: Name of the search area for identification
        limit: Maximum number of restaurants to fetch
        
    Returns:
        List[Restaurant]: List of restaurant objects from this location
    """
    # FoodPanda API endpoint for restaurant listing
    url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
    
    # Setup HTTP session with browser-like headers to avoid detection
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
        'x-disco-client-id': 'web',
        'Referer': 'https://www.foodpanda.hk/',
        'Origin': 'https://www.foodpanda.hk',
    })
    
    restaurants = []
    offset = 0          # Pagination offset
    batch_size = 48     # Number of restaurants per request
    
    print(f"🔍 Collecting restaurant data for {area_name} ({longitude:.4f}, {latitude:.4f})...")
    
    # Paginate through all available restaurants
    while len(restaurants) < limit:
        # API request parameters
        params = {
            'longitude': longitude,
            'latitude': latitude,
            'language_id': 10,                    # Hong Kong language setting
            'include': 'characteristics',        # Include cuisine/tag data
            'dynamic_pricing': 0,
            'configuration': 'Variant1',
            'country': 'hk',                     # Hong Kong country code
            'sort': 'rating_desc' if offset < 100 else 'distance_asc',  # Sort by rating first, then distance
            'use_free_delivery_label': False,
            'vertical': 'restaurants',
            'limit': min(batch_size, limit - len(restaurants)),
            'offset': offset,
            'customer_type': 'regular'
        }
        
        try:
            # Make API request with timeout
            response = session.get(url, params=params, timeout=15)
            
            # Check for successful response
            if response.status_code != 200:
                print(f"❌ API request failed (Status: {response.status_code})")
                break
            
            data = response.json()
            
            # Validate response structure
            if not data or 'data' not in data or 'items' not in data['data']:
                break
                
            items = data['data']['items']
            if not items:  # No more restaurants available
                break
            
            # Parse restaurant data from this batch
            batch_restaurants = []
            for item in items:
                restaurant = parse_restaurant_data(item, area_name)
                if restaurant:
                    batch_restaurants.append(restaurant)
            
            # Add to main collection
            restaurants.extend(batch_restaurants)
            offset += batch_size
            
            print(f"📥 {area_name}: Collected {len(restaurants)} restaurants (this batch: {len(batch_restaurants)})")
            
            # Stop if no new restaurants found
            if len(batch_restaurants) == 0:
                break
            
            # Rate limiting to avoid being blocked
            time.sleep(1.0)
            
        except Exception as e:
            print(f"❌ Error occurred for {area_name}: {e}")
            break
    
    print(f"✅ {area_name}: Collection completed, total {len(restaurants)} restaurants")
    return restaurants


def get_predefined_coordinates():
    """
    Get predefined popular coordinate points in Hong Kong
    
    Returns:
        dict: Dictionary mapping area names to (longitude, latitude) tuples
    """
    return {
        # Hong Kong Island major areas
        "Central 中環": (114.1578, 22.2842),
        "Sheung Wan 上環": (114.1417, 22.2569),
        "Sai Wan 西環": (114.1444, 22.2861),
        "Admiralty 金鐘": (114.1849, 22.2818),
        "Wan Chai 灣仔": (114.1722, 22.2783),
        "Causeway Bay 銅鑼灣": (114.1693, 22.2783),
        "Happy Valley 跑馬地": (114.1889, 22.2667),
        "Quarry Bay 鰂魚涌": (114.2264, 22.2444),
        "Taikoo 太古": (114.2397, 22.2597),
        "Shau Kei Wan 筲箕灣": (114.2583, 22.2781),
        "North Point 北角": (114.2181, 22.2472),
        "Aberdeen 香港仔": (114.1689, 22.2406),
        "Wong Chuk Hang 黃竹坑": (114.1750, 22.2472),
        
        # Kowloon major areas
        "Tsim Sha Tsui 尖沙咀": (114.2107, 22.3223),
        "Jordan 佐敦": (114.1819, 22.3028),
        "Yau Ma Tei 油麻地": (114.2281, 22.3193),
        "Mong Kok 旺角": (114.2029, 22.3193),
        "Prince Edward 太子": (114.2111, 22.3389),
        "Sham Shui Po 深水埗": (114.1944, 22.3278),
        "Cheung Sha Wan 長沙灣": (114.1917, 22.3361),
        "Kowloon City 九龍城": (114.2583, 22.3306),
        "Hung Hom 紅磡": (114.2236, 22.2778),
        "To Kwa Wan 土瓜灣": (114.2742, 22.3158),
        "Ho Man Tin 何文田": (114.2347, 22.3139),
        "Kwun Tong 觀塘": (114.2919, 22.3361),
        
        # New Territories major areas
        "Sha Tin 沙田": (114.2642, 22.3736),
        "Ma On Shan 馬鞍山": (114.3556, 22.4175),
        "Tai Po 大埔": (114.2119, 22.4467),
        "Fanling 粉嶺": (114.1569, 22.4964),
        "Sheung Shui 上水": (114.1244, 22.4969),
        "Tsuen Wan 荃灣": (114.1194, 22.3669),
        "Tuen Mun 屯門": (114.0306, 22.3969),
        "Yuen Long 元朗": (114.0742, 22.4456),
        "Tung Chung 東涌": (114.0500, 22.3117),
    }


def get_user_coordinates():
    """
    Get user-selected coordinates for restaurant search
    Supports predefined locations, custom coordinates, or mixed mode
    
    Returns:
        List[Tuple[float, float, str]]: List of (longitude, latitude, area_name) tuples
    """
    
    predefined = get_predefined_coordinates()
    
    print("\n" + "="*80)
    print("📍 Select Search Coordinates")
    print("="*80)
    print("Option 1: Use predefined coordinate points")
    print("Option 2: Input custom coordinates manually")  
    print("Option 3: Mixed mode (predefined + custom)")
    print("="*80)
    
    while True:
        try:
            mode = input("Please select mode (1/2/3): ").strip()
            if mode in ['1', '2', '3']:
                break
            print("❌ Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\n👋 User cancelled operation")
            return []
    
    selected_coordinates = []
    
    # Mode 1: Predefined coordinates
    if mode in ['1', '3']:
        print(f"\n🏙️ Available predefined coordinate points ({len(predefined)} locations):")
        print("-" * 80)
        
        # Display by regions for better organization
        hk_island = [(name, coord) for name, coord in predefined.items() if any(x in name for x in ["Central", "Sheung Wan", "Sai Wan", "Admiralty", "Wan Chai", "Causeway Bay", "Happy Valley", "Quarry Bay", "Taikoo", "Shau Kei Wan", "North Point", "Aberdeen", "Wong Chuk Hang"])]
        kowloon = [(name, coord) for name, coord in predefined.items() if any(x in name for x in ["Tsim Sha Tsui", "Jordan", "Yau Ma Tei", "Mong Kok", "Prince Edward", "Sham Shui Po", "Cheung Sha Wan", "Kowloon City", "Hung Hom", "To Kwa Wan", "Ho Man Tin", "Kwun Tong"])]
        nt = [(name, coord) for name, coord in predefined.items() if name not in [item[0] for item in hk_island + kowloon]]
        
        regions = [("🏝️ Hong Kong Island", hk_island), ("🏢 Kowloon", kowloon), ("🌳 New Territories", nt)]
        
        for region_name, locations in regions:
            print(f"\n{region_name}:")
            for name, (lng, lat) in locations:
                print(f"  • {name:<25} ({lng:.4f}, {lat:.4f})")
        
        print(f"\n💡 Input methods:")
        print("• Single: Central")
        print("• Multiple: Central,Mong Kok,Sha Tin")
        print("• All locations: all")
        
        while True:
            user_input = input(f"\nPlease enter locations to search: ").strip()
            
            if user_input.lower() == 'all':
                for name, coords in predefined.items():
                    selected_coordinates.append((coords[0], coords[1], name))
                print(f"✅ Selected all {len(predefined)} predefined coordinate points")
                break
            
            else:
                locations_input = [loc.strip() for loc in user_input.split(',') if loc.strip()]
                valid_locations = []
                
                for loc in locations_input:
                    # Fuzzy matching - match partial names
                    matched = False
                    for name, coords in predefined.items():
                        if loc in name or name.startswith(loc):
                            selected_coordinates.append((coords[0], coords[1], name))
                            valid_locations.append(name)
                            matched = True
                            break
                    
                    if not matched:
                        print(f"⚠️  Could not find '{loc}' in predefined coordinates")
                
                if valid_locations:
                    print(f"✅ Selected {len(valid_locations)} locations: {', '.join([loc.split()[0] for loc in valid_locations])}")
                    break
                else:
                    print("❌ No valid locations found, please try again")
    
    # Mode 2 or 3: Custom coordinates
    if mode in ['2', '3']:
        print(f"\n📐 Add Custom Coordinates")
        print("💡 Coordinate format examples:")
        print("  • Longitude,Latitude,Name: 114.1578,22.2842,My Location")
        print("  • Longitude Latitude Name: 114.1578 22.2842 My Location")  
        print("  • Coordinates only: 114.1578,22.2842")
        print("  • Multiple coordinates (one per line):")
        print("    114.1578,22.2842,Location 1")
        print("    114.2029,22.3193,Location 2")
        print("\n📍 Hong Kong coordinate range: Longitude 113.8-114.5, Latitude 22.0-22.6")
        
        while True:
            try:
                print(f"\nPlease enter coordinates (one per line, empty line to finish):")
                custom_coords = []
                
                while True:
                    coord_input = input().strip()
                    if not coord_input:
                        break
                    
                    parsed = parse_coordinate_input(coord_input)
                    if parsed:
                        longitude, latitude, area_name = parsed
                        custom_coords.append((longitude, latitude, area_name))
                        print(f"✅ Added: {area_name} ({longitude:.4f}, {latitude:.4f})")
                    else:
                        print(f"❌ Invalid coordinate format: {coord_input}")
                
                if custom_coords:
                    selected_coordinates.extend(custom_coords)
                    print(f"✅ Successfully added {len(custom_coords)} custom coordinate points")
                
                # Ask if user wants to continue adding more
                if custom_coords:
                    continue_input = input("Continue adding more coordinates? (y/n): ").strip().lower()
                    if continue_input not in ['y', 'yes']:
                        break
                else:
                    break
                    
            except KeyboardInterrupt:
                print("\n👋 Finished adding custom coordinates")
                break
    
    if not selected_coordinates:
        print("❌ No coordinate points selected")
        return []
    
    print(f"\n📍 Final selected search coordinates ({len(selected_coordinates)} points):")
    for i, (lng, lat, name) in enumerate(selected_coordinates, 1):
        print(f"  {i:2d}. {name:<30} ({lng:.4f}, {lat:.4f})")
    
    return selected_coordinates


def remove_duplicates(restaurants: List[Restaurant]) -> List[Restaurant]:
    """
    Remove duplicate restaurants using multiple identification criteria
    
    Args:
        restaurants: List of Restaurant objects potentially containing duplicates
        
    Returns:
        List[Restaurant]: Deduplicated list of restaurants
    """
    if not restaurants:
        return []
    
    print(f"🔄 Starting deduplication process, original count: {len(restaurants)}")
    
    unique_restaurants = []
    seen_identifiers = set()
    
    for restaurant in restaurants:
        # Primary identifier: code (most reliable)
        primary_id = restaurant.code.lower().strip() if restaurant.code else ""
        
        # Secondary identifier: name + address combination
        secondary_id = None
        if restaurant.name and restaurant.address:
            name_clean = restaurant.name.lower().strip()
            address_clean = restaurant.address.lower().strip()
            secondary_id = f"{name_clean}|{address_clean}"
        
        # Check for duplicates
        is_duplicate = False
        
        if primary_id and primary_id in seen_identifiers:
            is_duplicate = True
        elif not primary_id and secondary_id and secondary_id in seen_identifiers:
            is_duplicate = True
        
        if not is_duplicate:
            unique_restaurants.append(restaurant)
            
            if primary_id:
                seen_identifiers.add(primary_id)
            if secondary_id:
                seen_identifiers.add(secondary_id)
    
    removed_count = len(restaurants) - len(unique_restaurants)
    print(f"✅ Deduplication completed, removed {removed_count} duplicates, remaining: {len(unique_restaurants)} restaurants")
    
    return unique_restaurants


def export_restaurants_to_excel(all_restaurants: List[Restaurant], custom_name: str = "") -> str:
    """
    Export restaurant data to Excel with multiple sheets
    
    Args:
        all_restaurants: List of Restaurant objects to export
        custom_name: Custom name to include in filename
        
    Returns:
        str: Generated Excel filename, or empty string if export failed
    """
    if not all_restaurants:
        print("❌ No data to export")
        return ""
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if custom_name:
        filename = f"foodpanda_hk_{custom_name}_{timestamp}.xlsx"
    else:
        filename = f"foodpanda_hk_coordinates_{timestamp}.xlsx"
    
    print(f"💾 Exporting {len(all_restaurants)} restaurant records to {filename}...")
    
    # Convert to DataFrame
    restaurant_dicts = [asdict(restaurant) for restaurant in all_restaurants]
    df = pd.DataFrame(restaurant_dicts)
    
    # Reorder columns for better readability
    column_order = [
        'name', 'area', 'code', 'rating', 'rating_count', 'cuisines',
        'address', 'phone', 'longitude', 'latitude', 'distance',
        'minimum_order', 'budget_range', 'chain_name', 'legal_name',
        'is_open', 'is_delivery_enabled', 'is_pickup_enabled',
        'delivery_provider', 'available_in', 'tags',
        'hero_image', 'website'
    ]
    
    # Add missing columns with None values
    for col in column_order:
        if col not in df.columns:
            df[col] = None
    
    df = df[column_order]
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Restaurant Data', index=False)
            
            # Statistics summary sheet
            total_restaurants = len(all_restaurants)
            rated_restaurants = df['rating'].notna().sum()
            avg_rating = round(df['rating'].mean(), 2) if rated_restaurants > 0 else 0
            unique_areas = len(df['area'].unique())
            
            stats_data = {
                'Statistic': [
                    'Total Restaurants',
                    'Restaurants with Ratings',
                    'Average Rating', 
                    'Search Coordinate Points',
                    'Records with GPS Coordinates',
                    'Records with Phone Numbers',
                    'Chain Restaurants',
                    'Data Collection Time'
                ],
                'Value': [
                    total_restaurants,
                    rated_restaurants,
                    avg_rating,
                    unique_areas,
                    (df['longitude'].notna() & df['latitude'].notna()).sum(),
                    df['phone'].notna().sum(),
                    df['chain_name'].notna().sum(),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Statistics Summary', index=False)
            
            # Area-wise statistics sheet
            if len(df) > 0:
                area_stats = df.groupby('area').agg({
                    'name': 'count',
                    'rating': ['count', 'mean'],
                    'budget_range': 'mean'
                }).round(2)
                area_stats.columns = ['Restaurant Count', 'Rated Count', 'Average Rating', 'Average Budget']
                area_stats.reset_index().to_excel(writer, sheet_name='Area Statistics', index=False)
        
        print(f"✅ Successfully exported to {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return ""


def main():
    """
    Main program function - Coordinate Input Version
    
    This function orchestrates the entire restaurant crawling process:
    1. Gets user coordinate selection
    2. Crawls restaurant data from each coordinate point
    3. Removes duplicates
    4. Exports results to Excel
    """
    print("🇭🇰 FoodPanda Hong Kong Restaurant Crawler")
    print("📐 Coordinate Input Version + Automatic Deduplication")
    print("="*80)
    
    # Get user-selected coordinates
    coordinates = get_user_coordinates()
    if not coordinates:
        print("👋 Program ended")
        return
    
    print(f"\n🚀 Starting search")
    print(f"📍 Search coordinate points: {len(coordinates)}")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    # Initialize data collection
    all_restaurants = []
    processed_count = 0
    
    # Process each coordinate point
    for longitude, latitude, area_name in coordinates:
        try:
            processed_count += 1
            print(f"\n🔄 Progress: {processed_count}/{len(coordinates)} - {area_name}")
            
            # Fetch restaurants from this location
            area_restaurants = get_restaurants_by_location(longitude, latitude, area_name, limit=150)
            
            if area_restaurants:
                all_restaurants.extend(area_restaurants)
                print(f"📊 Current total: {len(all_restaurants)} restaurants (this batch: {len(area_restaurants)})")
            
            # Dynamic rest intervals to avoid rate limiting
            if processed_count % 5 == 0:
                print("⏸️  Resting 3 seconds after processing 5 coordinate points...")
                time.sleep(3)
            else:
                time.sleep(1.5)
            
        except Exception as e:
            print(f"❌ Error occurred for {area_name}: {e}")
            continue
    
    # Display collection results
    print(f"\n📊 Raw collection results:")
    print(f"• Search coordinate points: {len(coordinates)}")
    print(f"• Raw restaurant count: {len(all_restaurants)}")
    
    if all_restaurants:
        # Remove duplicates
        unique_restaurants = remove_duplicates(all_restaurants)
        
        # Calculate detailed statistics
        rated_count = sum(1 for r in unique_restaurants if r.rating is not None)
        coord_count = sum(1 for r in unique_restaurants if r.longitude and r.latitude)
        
        print(f"\n🎯 Final statistics:")
        print(f"• Deduplicated restaurants: {len(unique_restaurants)}")
        
        if rated_count > 0:
            avg_rating = sum(r.rating for r in unique_restaurants if r.rating is not None) / rated_count
            print(f"• With ratings: {rated_count} ({rated_count/len(unique_restaurants)*100:.1f}%)")
            print(f"• Average rating: {avg_rating:.2f}")
        
        print(f"• With coordinates: {coord_count} ({coord_count/len(unique_restaurants)*100:.1f}%)")
        
        # Export to Excel
        excel_file = export_restaurants_to_excel(unique_restaurants, "coordinates")
        
        if excel_file:
            print(f"\n🎉 Search completed!")
            print(f"📄 Excel file: {excel_file}")
            print(f"📊 Contains sheets: Restaurant Data, Statistics Summary, Area Statistics")
        
    else:
        print("❌ No restaurant data was collected")
    
    print(f"\n⏰ Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ Program execution completed")


if __name__ == '__main__':
    main()
