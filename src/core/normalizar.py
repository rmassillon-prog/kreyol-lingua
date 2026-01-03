import json

def normalize_articles(text):
    try:
        with open('data/lexicon/articles.json', 'r') as f:
            articles = json.load(f)
        
        words = text.split()
        normalized = []
        
        for word in words:
            found = False
            # Check definite articles (la, nan, an, etc.)
            for canon, data in articles['definite_articles'].items():
                if word in data['variants'] or word == canon:
                    normalized.append(canon)
                    found = True
                    break
            if not found:
                normalized.append(word)
                
        return " ".join(normalized)
    except Exception as e:
        return text
