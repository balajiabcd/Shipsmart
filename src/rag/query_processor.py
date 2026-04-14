from typing import List, Dict
import re


class QueryProcessor:
    def __init__(self):
        self.stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "what",
            "how",
            "why",
            "when",
            "where",
            "of",
            "to",
            "for",
            "in",
            "on",
        }

    def process(self, query: str) -> Dict:
        return {
            "original": query,
            "lowercase": query.lower(),
            "tokens": self._tokenize(query),
            "keywords": self._extract_keywords(query),
            "entities": self._extract_entities(query),
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"\w+", text.lower())
        return [t for t in tokens if t not in self.stop_words]

    def _extract_keywords(self, text: str) -> List[str]:
        tokens = self._tokenize(text)
        keywords = [t for t in tokens if len(t) > 2]
        return list(set(keywords))

    def _extract_entities(self, text: str) -> Dict:
        entities = {}

        delivery_ids = re.findall(r"DEL[\w-]+", text, re.IGNORECASE)
        if delivery_ids:
            entities["delivery_ids"] = delivery_ids

        dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
        if dates:
            entities["dates"] = dates

        order_ids = re.findall(r"ORD[\w-]+", text, re.IGNORECASE)
        if order_ids:
            entities["order_ids"] = order_ids

        numbers = re.findall(r"\d+", text)
        if numbers:
            entities["numbers"] = numbers

        return entities

    def expand_query(self, query: str) -> List[str]:
        base_terms = self._extract_keywords(query)
        variations = [query]

        synonyms = {
            "delay": ["late", "slow", "behind schedule", "tardy"],
            "delivery": ["shipment", "package", "order", "parcel"],
            "problem": ["issue", "trouble", "concern", "delay"],
            "route": ["path", "way", "journey"],
            "driver": ["courier", "driver", "pilot"],
            "weather": ["climate", "conditions", "forecast"],
            "traffic": ["congestion", "flow", "roads"],
        }

        for term in base_terms:
            if term in synonyms:
                for syn in synonyms[term]:
                    variations.append(query.replace(term, syn))

        return variations[:5]

    def extract_intent(self, query: str) -> Dict:
        query_lower = query.lower()

        intents = []

        if any(w in query_lower for w in ["why", "reason", "cause", "explain"]):
            intents.append("explain")

        if any(w in query_lower for w in ["predict", "will", "estimate", "when"]):
            intents.append("predict")

        if any(w in query_lower for w in ["recommend", "suggest", "should", "better"]):
            intents.append("recommend")

        if any(
            w in query_lower for w in ["optimize", "fastest", "shortest", "best route"]
        ):
            intents.append("optimize")

        if any(w in query_lower for w in ["status", "tracking", "where"]):
            intents.append("status")

        if not intents:
            intents.append("general")

        return {"query": query, "intents": intents}


if __name__ == "__main__":
    processor = QueryProcessor()
    result = processor.process("Why is delivery DEL-12345 delayed?")
    print(f"Processed query: {result}")
