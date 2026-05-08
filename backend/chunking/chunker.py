class DocumentChunker:

    def format_document(self, data):

        formatted_text = f"TITLE: {data['title']}\n\n"

        # Add headings
        if data.get("headings"):

            formatted_text += "HEADINGS:\n"

            for heading in data["headings"]:
                formatted_text += f"- {heading}\n"

        formatted_text += "\nCONTENT:\n"

        # Add paragraphs
        if data.get("paragraphs"):

            for para in data["paragraphs"]:

                if para.strip():
                    formatted_text += para + "\n\n"

        # Add code blocks
        if data.get("code_blocks"):

            formatted_text += "\nCODE EXAMPLES:\n"

            for code in data["code_blocks"]:

                if code.strip():

                    formatted_text += (
                        f"```python\n{code}\n```\n\n"
                    )

        return formatted_text


    def create_chunks(self, text, chunk_size=800):

        paragraphs = text.split("\n\n")

        chunks = []
        current_chunk = ""

        for para in paragraphs:

            if len(current_chunk) + len(para) < chunk_size:

                current_chunk += para + "\n\n"

            else:

                chunks.append(current_chunk)
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk)

        return chunks