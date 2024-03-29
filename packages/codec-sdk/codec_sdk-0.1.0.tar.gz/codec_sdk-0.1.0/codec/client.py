from codec.resources import (
    Collections,
    Videos,
    Utils
)
from codec.resources.search import search_with_query
from codec.auth import CodecAuth
import logging


# Disable httpx logs (supabase)
logging.getLogger("httpx").setLevel(logging.CRITICAL)


class Codec:
    def __init__(self, api_key: str):
        self.auth = CodecAuth(api_key=api_key)

    @property
    def collections(self):
        return Collections(self.auth)

    @property
    def utils(self):
        return Utils(self.auth)

    @property
    def videos(self):
        return Videos(self.auth)

    def search(
        self,
        query: str,
        search_visual: bool = True,
        search_speech: bool = True,
        video: str = None,
        collection: str = None,
        max_results:int = 10
    ):
        results = search_with_query(
            query=query,
            auth=self.auth,
            search_visual=search_visual,
            search_speech=search_speech,
            video=video,
            collection=collection,
            max_results=max_results
        )

        return results
