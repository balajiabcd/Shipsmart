# Milestone #193: Build Query Processing

**Your Role:** AI/LLM Engineer

Handle user queries:

```python
# src/rag/query_processor.py

from typing import List, Dict
import re

class QueryProcessor:
    def __init__(self):
        self.stop_words = set(['the', 'a', 'an', 'is', 'are', 'what', 'how', 'why', 'when', 'where'])
    
    def process(self, query: str) -> Dict:
        return {
            "original": query,
            "lowercase": query.lower(),
            "tokens": self._tokenize(query),
            "keywords": self._extract_keywords(query),
            "entities": self._extract_entities(query)
        }
    
    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\w+', text.lower())
        return [t for t in tokens if t not in self.stop_words]
    
    def _extract_keywords(self, text: str) -> List[str]:
        tokens = self._tokenize(text)
        # Keep significant keywords
        keywords = [t for t in tokens if len(t) > 2]
        return list(set(keywords))
    
    def _extract_entities(self, text: str) -> Dict:
        entities = {}
        
        # Delivery ID pattern
        delivery_ids = re.findall(r'DEL[\w-]+', text, re.IGNORECASE)
        if delivery_ids:
            entities["delivery_ids"] = delivery_ids
        
        # Date patterns
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        if dates:
            entities["dates"] = dates
        
        return entities
    
    def expand_query(self, query: str) -> List[str]:
        """Generate query variations for better retrieval"""
        base_terms = self._extract_keywords(query)
        variations = [query]  # Original
        
        # Add synonyms
        synonyms = {
            "delay": ["late", "slow", "behind schedule"],
            "delivery": ["shipment", "package", "order"],
            "problem": ["issue", "trouble", "concern"]
        }
        
        for term in base_terms:
            if term in synonyms:
                for syn in synonyms[term]:
                    variations.append(query.replace(term, syn))
        
        return variations
```

Commit.