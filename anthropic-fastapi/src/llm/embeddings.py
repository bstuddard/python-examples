from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search


model = SentenceTransformer(
    "intfloat/e5-small-v2",
    cache_folder='src/model_download_cache'
)
print(model)


def get_top_k_results(queries: list[str], passages: list[str], top_k: int = 3) -> list[str]:
    """Get top k results using text embedding model.

    Args:
        queries (list[str]): Questions or queries to use to lookup.
        passages (list[str]): Possible results.

    Returns:
        list[str]: List of unique passages that best match the query, up to top_k matches per query.
    """
    input_texts = ['query: ' + query for query in queries] + ['passage: ' + passage for passage in passages]
    embeddings = model.encode(input_texts, normalize_embeddings=True)
    query_embeddings = embeddings[:len(queries)]
    passage_embeddings = embeddings[len(queries):]

    search_results = semantic_search(query_embeddings, passage_embeddings, top_k=top_k)
    text_only_result_list = []
    for result in search_results:
        for result_match in result:
            if passages[result_match['corpus_id']] not in text_only_result_list:
                text_only_result_list.append(passages[result_match['corpus_id']])

    return text_only_result_list
        