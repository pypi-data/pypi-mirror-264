from codec.resources.request import Request


def search_with_query(
    query,
    auth,
    search_visual,
    search_speech,
    video,
    collection,
    max_results
):
    endpoint = "/search"
    results = Request(auth).post(
        endpoint=endpoint,
        body={
            "query": query,
            "search_visual": search_visual,
            "search_speech": search_speech,
            "video": video,
            "collection": collection,
            "max_results": max_results
        }
    )

    return results
