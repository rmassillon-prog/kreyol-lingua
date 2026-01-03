class KreyolEngine:
    def __init__(self, normalizer, tam_module, clitic_module):
        self.normalizer = normalizer
        self.tam_module = tam_module
        self.clitic_module = clitic_module

    def analyze(self, text: str):
        # This is the sequence of your framework
        clean_text = self.normalizer(text)
        tokens = clean_text.split()
        # In the next step, we will add the TAM Anchor logic here
        return {
            "status": "success",
            "normalized": clean_text,
            "tokens": tokens
        }