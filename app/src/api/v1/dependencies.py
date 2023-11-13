from fastapi import Query


def get_pagination_params(
        page_size: int = Query(10, gt=1),
        page_number: int = Query(0, gt=0)
):
    return {"size": page_size, "from": page_number}
