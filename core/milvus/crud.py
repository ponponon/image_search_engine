from core.milvus.schemas import SearchResult
from core.milvus.models import collection
from pymilvus.orm.mutation import MutationResult
from constants import THRESHOLD


def has_hash_code(hash_code: str) -> bool:
    rows: list[dict] = collection.query(expr=f'hash_code == "{hash_code}"')
    return bool(rows)


def insert_vector(vector: list[float], hash_code: str) -> int:
    """ 

    """
    rows: list[dict] = collection.query(expr=f'hash_code == "{hash_code}"')
    if rows:
        return rows[0].get('id', 0)
    data = [
        [hash_code],
        [vector]
    ]
    insert_result: MutationResult = collection.insert(data)
    assert len(insert_result.primary_keys) == 1
    return insert_result.primary_keys[0]


def search_vector(vector: list[float], offset: int = 0, limit: int = 10) -> list[SearchResult]:
    from pymilvus.orm.search import SearchResult as MilvusSearchResult
    from loggers import logger

    logger.debug(f'offset: {offset}, limit: {limit}')
    rows: MilvusSearchResult = collection.search(
        data=[vector],
        param={
            "metric_type": 'L2',
            "nprobe": 32,
            "offset": offset
        },
        anns_field='image_vector',
        output_fields=['id', 'hash_code'],
        limit=limit,
        # offset=offset
    )
    if not rows:
        return []

    search_results: list[SearchResult] = []

    for hits in rows:
        for hit in hits:
            # if hit.distance > THRESHOLD:
            #     continue
            search_results.append(
                SearchResult(
                    id=hit.id,
                    hash_code=hit.entity.get('hash_code'),
                    distance=hit.distance,
                    score=distance_2_score(hit.distance, THRESHOLD)
                )
            )
    return search_results


def distance_2_score(distance: float, threshold: float = 2.0) -> float:
    return (threshold-distance)/threshold*100


def query_vector(hash_code: str) -> list:
    result = collection.query(
        expr=f'hash_code == "{hash_code}"',
        output_fields=['id', 'hash_code']
    )
    return result


def delete_vector(hash_code: str):
    query_result: list[dict[str, int]] = collection.query(
        expr=f"hash_code in ['{hash_code}']", output_fields=['id'])
    ids = [item.get('id') for item in query_result]
    if ids:
        expr = f'id in {ids}'
        collection.delete(expr=expr)
        collection.flush()
