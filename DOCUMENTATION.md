# FoodPanda Hong Kong Restaurant Crawler Documentation

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation Guide](#installation-guide)
5. [Usage Instructions](#usage-instructions)
6. [Code Architecture](#code-architecture)
7. [Data Structure](#data-structure)
8. [API Integration](#api-integration)
9. [Configuration Options](#configuration-options)
10. [Output Format](#output-format)
11. [Troubleshooting](#troubleshooting)
12. [Technical Implementation](#technical-implementation)
13. [Advanced Features](#advanced-features)
14. [Development Notes](#development-notes)
15. [FAQ](#faq)

---

## Overview

### Purpose
The FoodPanda Hong Kong Restaurant Crawler is a comprehensive data collection tool designed to gather detailed restaurant information from FoodPanda's Hong Kong platform using coordinate-based searches.

### Key Capabilities
- **Multi-Location Search**: Supports both predefined popular locations and custom coordinate input
- **Comprehensive Data Collection**: Extracts 20+ restaurant attributes including ratings, contact info, and operational details
- **Intelligent Deduplication**: Removes duplicate entries using multiple identification criteria
- **Excel Export**: Generates multi-sheet Excel reports with statistics and area breakdowns
- **Rate Limiting**: Implements intelligent delays to avoid API blocking
- **Error Handling**: Robust error recovery and progress tracking

### Version Information
- **Script Name**: `coordinate_input_crawler.py`
- **Language**: Python 3.8+
- **Last Updated**: July 2025
- **License**: Educational/Research Use

---

## Features

### 🎯 Core Features
| Feature | Description | Status |
|---------|-------------|--------|
| Coordinate Input | Manual GPS coordinate entry | ✅ Active |
| Predefined Locations | 29 popular HK locations | ✅ Active |
| Mixed Mode | Combine predefined + custom | ✅ Active |
| Deduplication | Multi-criteria duplicate removal | ✅ Active |
| Excel Export | Multi-sheet statistical reports | ✅ Active |
| Progress Tracking | Real-time collection progress | ✅ Active |

### 📊 Data Collection
- **Restaurant Details**: Name, code, address, phone
- **Rating Information**: Average rating (0-5), review count
- **Location Data**: GPS coordinates, distance from search point
- **Operational Status**: Open/closed, delivery/pickup availability
- **Business Information**: Cuisine types, price range, chain affiliation
- **Service Details**: Delivery provider, minimum order amount

### 🔍 Search Modes
1. **Predefined Mode**: Select from 29 popular Hong Kong locations
2. **Custom Mode**: Input your own GPS coordinates with area names
3. **Mixed Mode**: Combine both predefined and custom locations

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python Version**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for large datasets)
- **Storage**: 100MB free space for output files
- **Internet**: Stable broadband connection

### Dependencies
```
requests >= 2.25.1
pandas >= 1.3.0
openpyxl >= 3.0.7
```

### Optional Requirements
- **Excel Viewer**: Microsoft Excel or LibreOffice Calc for viewing results
- **Text Editor**: For viewing/editing coordinate files

---

## Installation Guide

### Method 1: Direct Python Installation
```bash
# 1. Clone or download the script
# 2. Install dependencies
pip install requests pandas openpyxl

# 3. Run the script
python coordinate_input_crawler.py
```

### Method 2: Virtual Environment (Recommended)
```bash
# 1. Create virtual environment
python -m venv foodpanda_crawler

# 2. Activate environment
# Windows:
foodpanda_crawler\Scripts\activate
# macOS/Linux:
source foodpanda_crawler/bin/activate

# 3. Install dependencies
pip install requests pandas openpyxl

# 4. Run the script
python coordinate_input_crawler.py
```

### Method 3: Executable Version
1. Download the pre-built executable from the distribution folder
2. Double-click `FoodPandaCrawler.exe` (Windows)
3. No Python installation required

---

## Usage Instructions

### Quick Start Guide

#### Step 1: Launch the Application
```bash
python coordinate_input_crawler.py
```

#### Step 2: Select Search Mode
You'll see three options:
- **Option 1**: Use predefined coordinate points
- **Option 2**: Input custom coordinates manually
- **Option 3**: Mixed mode (both predefined + custom)

#### Step 3: Choose Locations

##### For Predefined Mode:
```
Examples:
• Single location: Central
• Multiple locations: Central,Mong Kok,Sha Tin
• All locations: all
```

##### For Custom Mode:
```
Coordinate formats:
• 114.1578,22.2842,My Location
• 114.1578 22.2842 Custom Area
• 114.1578,22.2842 (auto-named as "Custom Location")
```

#### Step 4: Monitor Progress
The crawler will display real-time progress:
- Current location being processed
- Number of restaurants collected per location
- Total progress and estimated completion time

#### Step 5: Review Results
- Excel file will be automatically generated
- Contains multiple sheets with detailed data and statistics

### Detailed Usage Examples

#### Example 1: Tourist Areas Search
```
Mode: 1 (Predefined)
Locations: Tsim Sha Tsui,Central,Causeway Bay
Expected Output: ~450-600 restaurants
Processing Time: ~3-5 minutes
```

#### Example 2: University Campus Search
```
Mode: 2 (Custom)
Coordinates: 
114.2642,22.3736,CUHK Area
114.1194,22.3669,HKUST Area
Expected Output: ~200-400 restaurants
Processing Time: ~2-3 minutes
```

#### Example 3: Comprehensive Hong Kong Search
```
Mode: 1 (Predefined)
Locations: all
Expected Output: ~2000-3000 restaurants
Processing Time: ~15-20 minutes
```

---

## Code Architecture

### Project Structure
```
coordinate_input_crawler.py
├── Data Models
│   └── Restaurant (dataclass)
├── Input Processing
│   ├── validate_coordinates()
│   ├── parse_coordinate_input()
│   └── get_user_coordinates()
├── Data Collection
│   ├── get_restaurants_by_location()
│   └── parse_restaurant_data()
├── Data Processing
│   └── remove_duplicates()
├── Output Generation
│   └── export_restaurants_to_excel()
└── Main Program
    └── main()
```

### Function Hierarchy
```
main()
├── get_user_coordinates()
│   ├── get_predefined_coordinates()
│   └── parse_coordinate_input()
│       └── validate_coordinates()
├── get_restaurants_by_location() (for each coordinate)
│   └── parse_restaurant_data()
├── remove_duplicates()
└── export_restaurants_to_excel()
```

### Design Patterns Used
- **Dataclass Pattern**: Structured data representation
- **Factory Pattern**: Restaurant object creation
- **Strategy Pattern**: Multiple coordinate input methods
- **Template Method**: Consistent data processing workflow

---

## Data Structure

### Restaurant Data Model
```python
@dataclass
class Restaurant:
    # Core Identifiers
    code: str                           # Unique restaurant ID
    name: str                          # Restaurant name
    
    # Rating & Reviews
    rating: Optional[float]            # Average rating (0-5)
    rating_count: Optional[int]        # Number of reviews
    
    # Location Data
    longitude: Optional[float]         # GPS longitude
    latitude: Optional[float]          # GPS latitude
    address: Optional[str]             # Full address
    area: Optional[str]                # Search area name
    distance: Optional[float]          # Distance from search point
    
    # Business Information
    cuisines: str                      # Cuisine types (comma-separated)
    budget_range: Optional[int]        # Price category (1-4)
    chain_name: Optional[str]          # Chain brand name
    legal_name: Optional[str]          # Legal business name
    
    # Contact Information
    phone: Optional[str]               # Contact phone number
    website: Optional[str]             # Restaurant website
    
    # Operational Details
    is_open: Optional[bool]            # Current status
    minimum_order: Optional[float]     # Minimum order amount
    is_delivery_enabled: Optional[bool] # Delivery availability
    is_pickup_enabled: Optional[bool]   # Pickup availability
    delivery_provider: Optional[str]    # Delivery service
    available_in: Optional[str]         # Service areas
    
    # Media & Marketing
    hero_image: Optional[str]          # Main image URL
    tags: str                          # Marketing tags
    
    # Legacy Fields
    delivery_time: Optional[str]       # Estimated delivery time
    delivery_fee: Optional[str]        # Delivery fee info
```

### Data Validation Rules
| Field | Validation | Required |
|-------|------------|----------|
| code | Non-empty string | ✅ Yes |
| name | Non-empty string | ✅ Yes |
| rating | 0.0 - 5.0 range | ❌ No |
| longitude | 113.8 - 114.5 (HK bounds) | ❌ No |
| latitude | 22.0 - 22.6 (HK bounds) | ❌ No |
| phone | Valid phone format | ❌ No |
| budget_range | 1-4 integer | ❌ No |

---

## API Integration

### FoodPanda API Details
- **Base URL**: `https://disco.deliveryhero.io/listing/api/v1/pandora/vendors`
- **Method**: GET
- **Authentication**: None required
- **Rate Limit**: ~1 request per second (recommended)

### Request Parameters
```python
params = {
    'longitude': float,              # GPS longitude
    'latitude': float,               # GPS latitude  
    'language_id': 10,               # Hong Kong language
    'include': 'characteristics',    # Include cuisine data
    'dynamic_pricing': 0,
    'configuration': 'Variant1',
    'country': 'hk',                 # Hong Kong country code
    'sort': 'rating_desc',           # Sort by rating
    'vertical': 'restaurants',
    'limit': 48,                     # Results per page
    'offset': 0,                     # Pagination offset
    'customer_type': 'regular'
}
```

### HTTP Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Chrome Browser)',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
    'x-disco-client-id': 'web',
    'Referer': 'https://www.foodpanda.hk/',
    'Origin': 'https://www.foodpanda.hk'
}
```

### Response Structure
```json
{
  "data": {
    "items": [
      {
        "code": "restaurant_id",
        "name": "Restaurant Name",
        "rating": 4.5,
        "review_number": 123,
        "longitude": 114.1578,
        "latitude": 22.2842,
        "address": "Full Address",
        "characteristics": {
          "cuisines": [{"name": "Chinese"}]
        },
        "metadata": {
          "is_delivery_available": true
        }
      }
    ]
  }
}
```

---

## Configuration Options

### Search Parameters
```python
# Location limits
LIMIT_PER_LOCATION = 150           # Max restaurants per coordinate
BATCH_SIZE = 48                    # Results per API request
REQUEST_TIMEOUT = 15               # Timeout in seconds

# Rate limiting
STANDARD_DELAY = 1.0               # Delay between requests (seconds)
BATCH_DELAY = 3.0                  # Delay after 5 locations (seconds)

# Hong Kong coordinate boundaries
MIN_LONGITUDE = 113.8
MAX_LONGITUDE = 114.5
MIN_LATITUDE = 22.0
MAX_LATITUDE = 22.6
```

### Predefined Locations Database
The script includes 29 carefully selected coordinate points covering:

#### Hong Kong Island (13 locations)
- Central, Sheung Wan, Sai Wan, Admiralty
- Wan Chai, Causeway Bay, Happy Valley
- Quarry Bay, Taikoo, Shau Kei Wan, North Point
- Aberdeen, Wong Chuk Hang

#### Kowloon (12 locations)
- Tsim Sha Tsui, Jordan, Yau Ma Tei, Mong Kok
- Prince Edward, Sham Shui Po, Cheung Sha Wan
- Kowloon City, Hung Hom, To Kwa Wan, Ho Man Tin, Kwun Tong

#### New Territories (9 locations)
- Sha Tin, Ma On Shan, Tai Po, Fanling, Sheung Shui
- Tsuen Wan, Tuen Mun, Yuen Long, Tung Chung

---

## Output Format

### Excel File Structure

#### Sheet 1: Restaurant Data
Contains all collected restaurant information with columns:
- **Basic Info**: name, area, code, rating, rating_count
- **Location**: address, longitude, latitude, distance
- **Business**: cuisines, budget_range, chain_name, legal_name
- **Operations**: is_open, is_delivery_enabled, is_pickup_enabled
- **Contact**: phone, website, delivery_provider
- **Additional**: tags, hero_image, available_in

#### Sheet 2: Statistics Summary
Provides overall statistics:
```
Statistic                    | Value
----------------------------|--------
Total Restaurants           | 2,847
Restaurants with Ratings    | 2,234
Average Rating              | 4.2
Search Coordinate Points    | 15
Records with GPS Coordinates| 2,801
Records with Phone Numbers  | 1,987
Chain Restaurants           | 456
Data Collection Time        | 2025-07-20 14:30:45
```

#### Sheet 3: Area Statistics
Shows per-area breakdown:
```
Area Name     | Restaurant Count | Rated Count | Avg Rating | Avg Budget
--------------|------------------|-------------|------------|------------
Central       | 234              | 198         | 4.3        | 2.8
Mong Kok      | 187              | 156         | 4.1        | 2.2
Causeway Bay  | 201              | 167         | 4.4        | 3.1
```

### File Naming Convention
```
foodpanda_hk_coordinates_YYYYMMDD_HHMMSS.xlsx

Example:
foodpanda_hk_coordinates_20250720_143045.xlsx
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: API Request Failures
**Symptoms**: `❌ API request failed (Status: 429)` or `❌ API request failed (Status: 403)`

**Causes**:
- Rate limiting exceeded
- IP temporarily blocked
- Network connectivity issues

**Solutions**:
1. Wait 5-10 minutes before retrying
2. Reduce the number of coordinate points
3. Check internet connection
4. Use VPN if necessary

#### Issue 2: Coordinate Validation Errors
**Symptoms**: `❌ Invalid coordinate format` or coordinates outside Hong Kong

**Solutions**:
1. Verify coordinate format: `longitude,latitude,name`
2. Check Hong Kong bounds: Longitude 113.8-114.5, Latitude 22.0-22.6
3. Use decimal degrees (not degrees/minutes/seconds)

#### Issue 3: Excel Export Failures
**Symptoms**: `❌ Export failed: Permission denied`

**Causes**:
- Excel file already open
- Insufficient disk space
- File permission issues

**Solutions**:
1. Close all Excel files before running
2. Check available disk space (>100MB)
3. Run as administrator if needed
4. Change output directory

#### Issue 4: Memory Issues
**Symptoms**: Slow performance or crashes with large datasets

**Solutions**:
1. Reduce `LIMIT_PER_LOCATION` from 150 to 100
2. Process fewer locations at once
3. Close other applications
4. Use 64-bit Python

#### Issue 5: Duplicate Detection Issues
**Symptoms**: Unexpected number of duplicates found/removed

**Solutions**:
1. Review restaurant codes and names
2. Check for data quality issues
3. Verify coordinate precision
4. Examine address normalization

### Debug Mode
To enable detailed debugging, modify the script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Technical Implementation

### Algorithm Details

#### Deduplication Algorithm
```python
def remove_duplicates(restaurants):
    """
    Multi-criteria deduplication using:
    1. Primary: Restaurant code (most reliable)
    2. Secondary: Name + Address combination
    """
    seen_identifiers = set()
    unique_restaurants = []
    
    for restaurant in restaurants:
        # Primary identifier
        primary_id = restaurant.code.lower().strip()
        
        # Secondary identifier  
        if restaurant.name and restaurant.address:
            secondary_id = f"{restaurant.name.lower()}|{restaurant.address.lower()}"
        
        # Check for duplicates
        if primary_id not in seen_identifiers:
            unique_restaurants.append(restaurant)
            seen_identifiers.add(primary_id)
            if secondary_id:
                seen_identifiers.add(secondary_id)
    
    return unique_restaurants
```

#### Coordinate Validation
```python
def validate_coordinates(longitude, latitude):
    """
    Hong Kong boundaries:
    - Longitude: 113.8° to 114.5°E  
    - Latitude: 22.0° to 22.6°N
    """
    return (113.8 <= longitude <= 114.5 and 
            22.0 <= latitude <= 22.6)
```

#### Rate Limiting Strategy
```python
# Dynamic delays based on processing count
if processed_count % 5 == 0:
    time.sleep(3)  # Longer delay every 5 locations
else:
    time.sleep(1.5)  # Standard delay
```

### Performance Optimization

#### Memory Management
- Use generators for large datasets
- Clear intermediate variables
- Implement batch processing

#### Network Optimization
- HTTP session reuse
- Connection pooling
- Retry logic with exponential backoff

#### Data Processing
- Vectorized operations with pandas
- Efficient deduplication algorithms
- Streaming Excel writing

---

## Advanced Features

### Custom Coordinate Input Formats
The script supports multiple coordinate input formats:

```python
# Comma-separated with name
"114.1578,22.2842,Central District"

# Space-separated with name  
"114.1578 22.2842 Wan Chai"

# Coordinates only (auto-named)
"114.1578,22.2842"

# Multiple entries (one per line)
114.1578,22.2842,Location 1
114.2029,22.3193,Location 2
114.1194,22.3669,Location 3
```

### Batch Processing Mode
For processing large coordinate lists:

```python
# Create coordinate file: coordinates.txt
114.1578,22.2842,Central
114.2029,22.3193,Mong Kok
114.1693,22.2783,Causeway Bay

# Modify script to read from file
with open('coordinates.txt', 'r') as f:
    coordinates = [parse_coordinate_input(line.strip()) 
                  for line in f if line.strip()]
```

### Statistical Analysis
The Excel output includes advanced statistics:

- **Coverage Analysis**: Restaurant density per area
- **Rating Distribution**: Histogram of rating ranges
- **Cuisine Analysis**: Most popular cuisine types
- **Price Range Analysis**: Budget distribution
- **Chain Analysis**: Chain vs independent restaurants

### Export Customization
Modify column order and content:

```python
column_order = [
    'name', 'rating', 'cuisines', 'address', 'phone',
    'longitude', 'latitude', 'is_open', 'minimum_order'
]
```

---

## Development Notes

### Code Quality Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Full type annotation coverage
- **Docstrings**: Comprehensive function documentation
- **Error Handling**: Robust exception management

### Testing Strategy
- **Unit Tests**: Individual function testing
- **Integration Tests**: API communication testing  
- **Data Validation**: Output format verification
- **Performance Tests**: Large dataset handling

### Future Enhancements

#### Short-term (v1.1)
- [ ] GUI interface with Tkinter
- [ ] JSON output format support
- [ ] Command-line argument support
- [ ] Progress bar visualization

#### Medium-term (v1.2)
- [ ] Multi-threading for parallel requests
- [ ] Database storage option (SQLite)
- [ ] Restaurant menu information
- [ ] Price comparison features

#### Long-term (v2.0)
- [ ] Web interface with Flask
- [ ] Real-time monitoring dashboard
- [ ] Historical data tracking
- [ ] Machine learning insights

### Contributing Guidelines
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

### Version History
- **v1.0** (July 2025): Initial coordinate-based crawler
- **v0.9** (June 2025): Custom location input support
- **v0.8** (May 2025): Interactive area selection
- **v0.7** (April 2025): Basic Hong Kong crawler

---

## FAQ

### General Questions

**Q: How accurate is the restaurant data?**
A: The data is sourced directly from FoodPanda's API, ensuring high accuracy. However, restaurant information can change frequently, so data should be considered a snapshot at collection time.

**Q: Can I use this for commercial purposes?**
A: This script is intended for educational and research purposes. Commercial use should comply with FoodPanda's Terms of Service and data usage policies.

**Q: How long does a full Hong Kong scan take?**
A: Processing all 29 predefined locations typically takes 15-20 minutes and yields 2,000-3,000 unique restaurants.

### Technical Questions

**Q: Why do I get different numbers of restaurants each time?**
A: Restaurant availability, operating hours, and FoodPanda's algorithms can affect results. Some restaurants may be temporarily unavailable or new ones may be added.

**Q: Can I modify the coordinate boundaries?**
A: Yes, modify the `validate_coordinates()` function to change the geographic scope. Current bounds are optimized for Hong Kong.

**Q: How does the deduplication work?**
A: The system uses a two-tier approach: primary identification by restaurant code, and secondary identification by name+address combination.

### Data Questions

**Q: What does the budget_range field represent?**
A: Budget range is typically 1-4, where:
- 1 = Budget-friendly
- 2 = Moderate  
- 3 = Mid-range
- 4 = Premium

**Q: Why are some fields empty?**
A: Not all restaurants provide complete information. The script captures all available data while handling missing fields gracefully.

**Q: Can I get menu information?**
A: The current version focuses on restaurant metadata. Menu data would require additional API endpoints and significantly more complex processing.

### Troubleshooting Questions

**Q: The script stops with network errors. What should I do?**
A: Network issues are common. The script includes retry logic, but you may need to restart if problems persist. Consider using a VPN or trying during off-peak hours.

**Q: I'm getting "coordinate out of bounds" errors for valid Hong Kong locations.**
A: Double-check your coordinate format and ensure you're using decimal degrees. The bounds are conservative and may exclude some outlying areas.

**Q: The Excel file won't open.**
A: Ensure you have Excel or LibreOffice Calc installed. Large files (>10MB) may take time to open. Try opening with a text editor first to verify the file isn't corrupted.

---

## Support and Contact

### Getting Help
1. **Documentation**: Review this comprehensive guide
2. **Code Comments**: Check inline code documentation
3. **Error Messages**: Read error output carefully
4. **GitHub Issues**: Report bugs or request features

### Best Practices
- **Test Small**: Start with 2-3 coordinates before large runs
- **Monitor Progress**: Watch console output for issues
- **Regular Backups**: Save successful Excel files
- **Update Regularly**: Check for script updates

### Performance Tips
- **Optimal Timing**: Run during Hong Kong off-peak hours (2-6 AM HKT)
- **Stable Connection**: Use wired internet when possible
- **Resource Management**: Close other applications during large runs
- **Batch Processing**: Process locations in groups of 5-10

---

*This documentation covers FoodPanda Hong Kong Restaurant Crawler v1.0. For the latest updates and additional resources, check the project repository.*

**Last Updated**: July 20, 2025
**Document Version**: 1.0
**Script Compatibility**: coordinate_input_crawler.py v1.0+
