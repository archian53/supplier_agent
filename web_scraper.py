import trafilatura
from logger_config import logger
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_website_text_content(self, url: str) -> str:
        try:
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded)
            if not text:
                raise ValueError("No content extracted from the URL")
            logger.info(f"Successfully scraped content from {url}")
            return text
        except Exception as e:
            logger.error(f"Error scraping content from {url}: {str(e)}")
            raise

    def search_product_info(self, supplier_name: str, product_name: str) -> dict:
        try:
            # Construct search query
            search_query = f"{supplier_name} {product_name} specifications"
            search_url = f"https://www.google.com/search?q={search_query}"
            
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant links
            search_results = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('/url?q='):
                    url = href.split('/url?q=')[1].split('&')[0]
                    if self._is_valid_domain(url):
                        search_results.append(url)
            
            # Get content from first valid result
            if search_results:
                content = self.get_website_text_content(search_results[0])
                return {
                    'source_url': search_results[0],
                    'content': content
                }
            else:
                raise ValueError("No valid search results found")
                
        except Exception as e:
            logger.error(f"Error searching product info: {str(e)}")
            raise

    def _is_valid_domain(self, url: str) -> bool:
        """Filter out unwanted domains like social media, video platforms, etc."""
        excluded_domains = {'facebook.com', 'twitter.com', 'youtube.com', 'instagram.com'}
        domain = urlparse(url).netloc
        return domain not in excluded_domains
