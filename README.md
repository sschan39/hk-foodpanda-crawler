# 🍜 FoodPanda Hong Kong Restaurant Crawler

A comprehensive Python tool for collecting restaurant data from FoodPanda Hong Kong using coordinate-based searches.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/foodpanda-hk-crawler.git
cd foodpanda-hk-crawler

# Install dependencies
pip install -r requirements.txt

# Run the crawler
python coordinate_input_crawler.py
```

## ✨ Features

- 🎯 **Multi-Location Search**: 29+ predefined Hong Kong locations + custom coordinates
- 📊 **Comprehensive Data**: 20+ restaurant attributes (ratings, contact, location, etc.)
- 🔄 **Smart Deduplication**: Advanced duplicate removal algorithms
- 📈 **Excel Reports**: Multi-sheet statistical analysis
- ⚡ **Rate Limiting**: Intelligent API request management
- 🛡️ **Error Handling**: Robust recovery and progress tracking

## 📖 Documentation

- **[Complete Documentation](DOCUMENTATION.md)** - Comprehensive guide (15 sections, 50+ subsections)
- **[Quick Start Guide](#quick-start)** - Get running in 5 minutes
- **[API Reference](#api-reference)** - Technical implementation details
- **[FAQ](#faq)** - Common questions and troubleshooting

## 🎯 Usage Examples

### Tourist Areas Search
```bash
Mode: 1 (Predefined)
Locations: Tsim Sha Tsui,Central,Causeway Bay
Output: ~450-600 restaurants in 3-5 minutes
```

### Custom University Areas
```bash
Mode: 2 (Custom Coordinates)
Input: 114.2642,22.3736,CUHK Area
Output: ~200-400 restaurants in 2-3 minutes
```

### Full Hong Kong Coverage
```bash
Mode: 1 (Predefined)
Locations: all
Output: ~2000-3000 restaurants in 15-20 minutes
```

## 📊 Sample Output

| Name | Rating | Cuisines | Address | Phone |
|------|--------|----------|---------|-------|
| Tim Ho Wan | 4.5 | Dim Sum, Cantonese | Central, Hong Kong | +852 2332 2896 |
| Tsui Wah | 4.2 | Hong Kong Style Cafe | Multiple Locations | +852 2868 3322 |

**Excel Output Includes:**
- 📋 **Restaurant Data**: Complete dataset with 20+ fields
- 📈 **Statistics Summary**: Aggregated insights and metrics  
- 🗺️ **Area Analysis**: Location-based breakdowns

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Stable internet connection
- 100MB free disk space

### Method 1: Python Installation
```bash
pip install requests pandas openpyxl
python coordinate_input_crawler.py
```

### Method 2: Executable (Windows)
1. Download from [Releases](https://github.com/yourusername/foodpanda-hk-crawler/releases)
2. Run `FoodPandaCrawler.exe`
3. No Python required!

### Method 3: Docker
```bash
docker build -t foodpanda-crawler .
docker run -it foodpanda-crawler
```

## 🏗️ Project Structure

```
foodpanda-hk-crawler/
├── coordinate_input_crawler.py    # Main crawler script
├── DOCUMENTATION.md               # Complete documentation
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── setup.py                      # Package setup
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker orchestration
├── build_app.py                 # Executable builder
├── launch_crawler.bat/.sh       # Launch scripts
└── FoodPandaCrawler_Distribution/  # Pre-built executables
    ├── FoodPandaCrawler.exe
    ├── QUICK_START.md
    └── README.md
```

## 🔧 Configuration

### Predefined Locations (29 areas)
- **Hong Kong Island**: Central, Wan Chai, Causeway Bay, etc.
- **Kowloon**: Tsim Sha Tsui, Mong Kok, Yau Ma Tei, etc.  
- **New Territories**: Sha Tin, Tsuen Wan, Tuen Mun, etc.

### Custom Coordinate Formats
```python
# Multiple supported formats
"114.1578,22.2842,Central District"
"114.1578 22.2842 Wan Chai"
"114.1578,22.2842"  # Auto-named
```

### Rate Limiting
```python
STANDARD_DELAY = 1.0      # Between requests
BATCH_DELAY = 3.0         # After 5 locations
LIMIT_PER_LOCATION = 150  # Max restaurants per area
```

## 🚨 Troubleshooting

### Common Issues

**API Rate Limiting**
```bash
❌ API request failed (Status: 429)
✅ Solution: Wait 5-10 minutes, reduce coordinate count
```

**Coordinate Validation**
```bash
❌ Invalid coordinate format
✅ Solution: Use format "longitude,latitude,name"
```

**Excel Export Errors**
```bash
❌ Export failed: Permission denied
✅ Solution: Close Excel files before running
```

See [DOCUMENTATION.md](DOCUMENTATION.md#troubleshooting) for complete troubleshooting guide.

## 🧪 Testing

```bash
# Run basic functionality test
python -c "from coordinate_input_crawler import validate_coordinates; print(validate_coordinates(114.1578, 22.2842))"

# Test with small dataset
python coordinate_input_crawler.py
# Select Mode 1, enter "Central" for quick test
```

## 📈 Performance

- **Memory Usage**: ~50-100MB during operation
- **Network**: ~1 request/second rate limit
- **Storage**: ~1-5MB per 1000 restaurants
- **Speed**: ~100-200 restaurants per minute

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/foodpanda-hk-crawler.git
cd foodpanda-hk-crawler
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## � License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This tool is for **educational and research purposes only**. Users must comply with:
- FoodPanda's Terms of Service
- Applicable data protection laws
- Respectful API usage practices

## 🙋 FAQ

**Q: How accurate is the data?**  
A: Data is sourced directly from FoodPanda's API, ensuring high accuracy at collection time.

**Q: Can I modify the search area?**  
A: Yes! Use custom coordinates or modify the `validate_coordinates()` function.

**Q: Why do results vary between runs?**  
A: Restaurant availability and FoodPanda's algorithms can affect results.

## � Stats

- **Lines of Code**: ~700+
- **Functions**: 8 main functions
- **Data Fields**: 24 restaurant attributes
- **Locations**: 29 predefined + unlimited custom
- **Output Formats**: Excel (3 sheets)

---

⭐ **Star this repo if you find it useful!** ⭐

*Last updated: July 2025*
- **Missing Data**: Some restaurants may have incomplete profiles
- **API Errors**: Wait and retry, or reduce batch size

## 📝 License

This project is for educational purposes. Please respect FoodPanda's terms of service and use responsibly.

## 🤝 Contributing

Feel free to submit issues, suggestions, or improvements!

---

**Author**: sschan
**Version**: 1.0  
**Last Updated**: July 2025
