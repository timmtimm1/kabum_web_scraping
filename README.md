# Kabum Product Scraper

This project is a web scraping tool designed to extract product information from the Kabum website. It retrieves details such as the product name, current price, old price (if available), stock status, and the product link. The scraped data is then saved into a CSV file and a JSON file for further analysis.

## Features

- **Multiple Pages Scraping**: The tool navigates through multiple pages of search results to gather comprehensive data on products.
- **Dynamic Web Scraping**: Utilizes `BeautifulSoup` and `requests` libraries to parse HTML content and extract relevant information.
- **Multithreaded Scraping:** The scraper uses threading to improve efficiency and reduce the time required to gather data.
- **Data Export**: The scraped data is automatically saved into both CSV and JSON files for easy access and analysis.

## How It Works

#### Product Links Extraction:
- The script generates a list of URLs based on the search query for the chosen product.
- It then fetches the product links from each page of search results.

#### Product Details Scraping:
- For each product link, the script visits the product page and scrapes the necessary details like name, price, stock status, etc.

#### Multithreaded Processing:
- The `scrape_product_details_threaded` function uses Python's `ThreadPoolExecutor` to scrape product details concurrently, making the process faster and more efficient.

#### Data Storage:
- The extracted data is stored in both CSV and JSON formats, named after the searched product, in the specified folder.

#### `scrape_product_details_threaded` Function:
This function manages the scraping process using multiple threads, allowing for faster data collection. It leverages `ThreadPoolExecutor` to run multiple threads simultaneously, each thread responsible for scraping one product page. The results are processed as they become available, and any errors are caught and printed without disrupting the entire scraping process.

## Installation

To use this project, you need to have Python installed on your system. Then, install the required Python libraries:

```bash
pip install requests pandas beautifulsoup4 tqdm


