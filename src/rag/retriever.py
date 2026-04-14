from typing import List, Dict, Optional
import asyncio


class Retriever:
    def __init__(self, pipeline, query_processor):
        self.pipeline = pipeline
        self.query_processor = query_processor

    async def retrieve(
        self, query: str, top_k: int = 5, filters: Dict = None
    ) -> List[Dict]:
        processed = self.query_processor.process(query)

        expanded_queries = self.query_processor.expand_query(query)

        all_results = []
        for q in expanded_queries[:3]:
            results = await self.pipeline.retrieve(q, top_k)

            if filters:
                results = self._apply_filters(results, filters)

            all_results.extend(results)

        return self._deduplicate_and_rank(all_results, top_k)

    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        filtered = []
        for r in results:
            match = True
            for key, value in filters.items():
                if r.get("metadata", {}).get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(r)
        return filtered

    def _deduplicate_and_rank(self, results: List[Dict], top_k: int) -> List[Dict]:
        seen_ids = set()
        unique = []

        for r in results:
            doc_id = r.get("doc_id") or r.get("id")
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                unique.append(r)

        return unique[:top_k]


class MultiRetriever:
    def __init__(self, retrievers: List[Retriever]):
        self.retrievers = retrievers

    async def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        all_results = []

        tasks = [retriever.retrieve(query, top_k) for retriever in self.retrievers]
        results_list = await asyncio.gather(*tasks)

        for results in results_list:
            all_results.extend(results)

        seen_ids = set()
        unique = []
        for r in all_results:
            doc_id = r.get("doc_id") or r.get("id")
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                unique.append(r)

        return sorted(unique, key=lambda x: x.get("score", 0), reverse=True)[:top_k]


if __name__ == "__main__":
    print("Retriever classes defined")
