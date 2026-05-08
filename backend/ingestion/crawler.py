import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class DocumentationCrawler:

    def __init__(self, base_url):

        self.base_url = base_url

        self.visited = set()

        self.valid_links = []


    def crawl(self, url, depth=2):

        if depth == 0:
            return

        if url in self.visited:
            return

        self.visited.add(url)

        print(f"Crawling: {url}")

        try:

            response = requests.get(
                url,
                timeout=10
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            self.valid_links.append(url)

            for a_tag in soup.find_all("a", href=True):

                href = a_tag["href"]

                full_url = urljoin(url, href)

                # keep only internal docs links
                if (
                    self.base_url in full_url
                    and "#" not in full_url
                    and "?" not in full_url
                ):

                    self.crawl(
                        full_url,
                        depth - 1
                    )

        except Exception as e:

            print(f"Error crawling {url}: {e}")


    def get_all_links(self):

        self.crawl(self.base_url)

        return list(set(self.valid_links))