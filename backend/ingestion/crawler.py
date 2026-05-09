import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque


LANGUAGE_PATTERN = re.compile(
    r'/(zh|es|fr|ja|ko|de|pt|ru|it|tr|pl|nl|ar|fa|hi|bn|id|uk|ro|cs|hu|vi|th)(-\w+)?/'
)

SKIP_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg',
                   '.ico', '.css', '.js', '.pdf', '.zip', '.woff', '.woff2')


class DocumentationCrawler:

    def __init__(self, base_url, max_pages=15):

        self.base_url = base_url.rstrip("/")

        self.max_pages = max_pages

        self.visited = set()

        self.valid_links = []


    def _is_valid(self, url):
        """Return True if the URL should be crawled."""

        # Must be within the base domain
        if not url.startswith(self.base_url):
            return False

        # Skip non-English language paths
        if LANGUAGE_PATTERN.search(url):
            return False

        # Skip static assets
        if any(url.endswith(ext) for ext in SKIP_EXTENSIONS):
            return False

        return True


    def get_all_links(self):
        """BFS crawl — visits at most max_pages pages, no recursion."""

        queue = deque([self.base_url])

        while queue and len(self.valid_links) < self.max_pages:

            url = queue.popleft()

            if url in self.visited:
                continue

            self.visited.add(url)

            print(f"Crawling: {url}")

            try:

                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                self.valid_links.append(url)

                for a_tag in soup.find_all("a", href=True):

                    href = a_tag["href"]

                    # Skip anchors, query strings, mailto, javascript
                    if not href or href.startswith(("#", "?", "mailto:", "javascript:")):
                        continue

                    full_url = urljoin(url, href).split("?")[0].split("#")[0]

                    if self._is_valid(full_url) and full_url not in self.visited:
                        queue.append(full_url)

            except Exception as e:

                print(f"Error crawling {url}: {e}")

        return self.valid_links