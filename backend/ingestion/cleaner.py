class ContentCleaner:

    def clean_text(self, text):
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = " ".join(text.split())

        return text