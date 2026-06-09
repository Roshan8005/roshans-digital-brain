# Cerebellum Memory Retrieval - Local Search Indexer Engine
# Location: Cerebellum

import os
import json
import re

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_file = os.path.join(base_dir, "4_Limbic_System", "Hippocampus", "knowledge_index.json")

_KNOWLEDGE_CACHE = None
WORD_PATTERN = re.compile(r"\w+")

def _load_index():
    global _KNOWLEDGE_CACHE
    if _KNOWLEDGE_CACHE is not None:
        return _KNOWLEDGE_CACHE
    if not os.path.exists(index_file):
        return {}
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            _KNOWLEDGE_CACHE = json.load(f)
            return _KNOWLEDGE_CACHE
    except Exception as e:
        print(f"[Cerebellum Error] Failed to read memory index: {e}")
        return {}

def search_memory(query, limit=3):
    """
    Searches the compiled knowledge index for matching terms.
    Returns: List of dicts [{"file_path": str, "score": int, "region": str, "snippet": str}]
    """
    index = _load_index()
    if not index:
        return []
        
    # Standardize query terms
    query_terms = [term.lower() for term in WORD_PATTERN.findall(query) if len(term) > 2]
    if not query_terms:
        return []
        
    results = []
    
    for rel_path, data in index.items():
        score = 0
        content = data.get("snippet", "").lower()
        filename = data.get("filename", "").lower()
        
        # Calculate matching score based on term occurrence
        for term in query_terms:
            # Filename match is very important (highly weighted)
            if term in filename:
                score += 10
            # Content snippet match
            occurrences = content.count(term)
            score += min(occurrences, 5) # Cap term frequency weight to avoid spam
            
        if score > 0:
            results.append({
                "file_path": rel_path,
                "score": score,
                "region": data.get("region", "General"),
                "snippet": data.get("snippet", "")
            })
            
    # Sort results by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]
