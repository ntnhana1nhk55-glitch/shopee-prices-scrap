# Shopee Price Scraper Project Ver 2

A project to scrape product data and prices from Shopee using Python and Playwright.

## Features
- **Extract product information**: name, price, ratings, metadata, etc.
- **Handle dynamic content**: processes JavaScript-rendered pages using Playwright.
- **Bot detection bypass**: utilizes the stealth plugin to reduce the risk of being identified as a bot.
- **Data export**: saves results to CSV files for easy processing with Pandas or Excel.

## Technologies Used
- **Python**: Core programming language.
- **Playwright**: Browser automation library.
- **playwright-stealth**: Stealth plugin for Playwright.
- **Pandas**: Data manipulation and export.

## Installation

### System Requirements
- Python 3.8+
- pip (Python package manager)

### Installation Steps
1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

## Usage
To run the scraper script:
```bash
python shopee_scraper.py
```
Upon running, the program will prompt you to enter:
- **Keyword**: The name of the product you want to search for.
- **Number of pages**: The number of result pages you want to scrape (each page contains approximately 60 products).

Data will be automatically saved to a CSV file in the root directory with the naming format: `shopee_[keyword]_[timestamp].csv`.

## Testing
Run tests using pytest:
```bash
pytest
```

## Note
The project uses the `shopee_profile` directory to store browser data, which helps maintain login states or browser configurations if needed.
