#(C)Tsubasa Kato 2025/6/22 - Inspire Search Corp. - Created with help of Perplexity Pro.
import math
import requests
import time  # Import the time module
from bs4 import BeautifulSoup
from collections import deque
import sys
class SpiralMagneticCrawler:
    def __init__(self, start_url, max_pages=100, delay=1):
        """
        Initializes the crawler.
        
        Args:
            start_url (str): The URL to begin crawling from.
            max_pages (int): The maximum number of pages to crawl.
            delay (int): The number of seconds to pause between requests.
        """
        self.start_url = start_url
        self.max_pages = max_pages
        self.delay = delay  # Store the delay
        self.visited = set()
        self.to_visit = deque([(start_url, 0)])  
        self.crawled_pages = 0

    def magnetic_priority(self, url):
        """
        Calculates a priority score for a URL based on 'magnetic' keywords.
        """
        magnetic_keywords = ['magnet', 'spin', 'field', 'energy', 'force']
        score = sum(url.count(k) for k in magnetic_keywords)
        return score

    def spiral_angle_increment(self, current_angle):
        """
        Increments the angle in radians to simulate a spiral progression.
        """
        return current_angle + math.pi / 4

    def crawl(self):
        """
        Starts the crawling process.
        """
        while self.to_visit and self.crawled_pages < self.max_pages:
            url, angle = self.to_visit.popleft()
            
            if url in self.visited:
                continue
            
            try:
                
                response = requests.get(url, timeout=5)
                

                if response.status_code != 200:
                    # Add a pause after making the request
                    
                    continue
                
                self.visited.add(url)
                self.crawled_pages += 1
                print(f'Crawling ({self.crawled_pages}): {url}')

                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                
                filtered_links = [link for link in links if link.startswith('http') and link not in self.visited]
                filtered_links.sort(key=self.magnetic_priority, reverse=True)

                for link in filtered_links:
                    new_angle = self.spiral_angle_increment(angle)
                    self.to_visit.append((link, new_angle))

                print(f"Pausing for {self.delay} second(s)...")
                time.sleep(self.delay)

            except Exception as e:
                print(f'Error crawling {url}: {e}')

url = sys.argv[1]
num_pages_to_crawl = int(sys.argv[2])
crawler = SpiralMagneticCrawler(url, max_pages=num_pages_to_crawl, delay=1)
crawler.crawl()
