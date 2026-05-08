from ingestion.crawler import DocumentationCrawler
from ingestion.parser import DocumentationParser

BASE_URL = "https://react.dev/learn"

crawler = DocumentationCrawler(BASE_URL)
parser = DocumentationParser()

links = crawler.get_all_links()

print(f"Found {len(links)} links")

for link in links[:10]:

    data = parser.extract_content(link)

    if data:

        filename = (
            data["title"]
            .replace("/", "_")
            .replace(" ", "_")
            .replace(":", "_")
        )

        parser.save_json(data, filename)

        print(f"Saved: {filename}")

        print("=" * 50)
        print(data["title"])
        print(data["url"])
        print(data["headings"][:3])