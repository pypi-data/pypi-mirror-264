from codec.resources.request import Request


def search_with_query(
    query,
    auth,
    search_types,
    video,
    collection,
    max_results
):
    endpoint = "/search"
    results = Request(auth).post(
        endpoint=endpoint,
        body={
            "query": query,
            "search_types": search_types,
            "video": video,
            "collection": collection,
            "max_results": max_results
        }
    )

    return results
