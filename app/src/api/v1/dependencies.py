from fastapi import Query


def get_pagination_params(
        page_size: int = Query(10, gt=1),
        page_number: int = Query(0, gt=0)
):
    return {"size": page_size, "from": page_number}


def get_search_query(
        search: str = Query(None, max_length=50)
):
    return {"match_all": {}} if search is None else {"multi_match": {"query": search}}


def get_search_query_by_name(
        search: str = Query(None, max_length=50)
):
    return {"match_all": {}} if search is None else {"multi_match": {"query": search, "fields": ["name"]}}
