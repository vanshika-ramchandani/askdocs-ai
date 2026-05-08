import requests
from bs4 import BeautifulSoup
import json
import os


class DocumentationParser:

    def extract_content(self, url):

        try:

            response = requests.get(url, timeout=10)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = (
                soup.title.text.strip()
                if soup.title
                else "No Title"
            )

            headings = [
                h.get_text(strip=True)
                for h in soup.find_all(["h1", "h2", "h3"])
            ]

            paragraphs = [
                p.get_text(strip=True)
                for p in soup.find_all("p")
            ]

            code_blocks = []

            for code in soup.find_all("code"):

                text = code.get_text(strip=True)

                if (
                    text
                    and text.lower() != "undefined"
                    and len(text) > 5
                ):

                    code_blocks.append(text)

            return {
                "url": url,
                "title": title,
                "headings": headings,
                "paragraphs": paragraphs,
                "code_blocks": code_blocks
            }

        except Exception as e:

            print(f"Error parsing {url}: {e}")

            return None


    def save_json(self, data, filename):

        os.makedirs(
            "backend/data/raw_docs",
            exist_ok=True
        )

        filepath = (
            f"backend/data/raw_docs/{filename}.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )