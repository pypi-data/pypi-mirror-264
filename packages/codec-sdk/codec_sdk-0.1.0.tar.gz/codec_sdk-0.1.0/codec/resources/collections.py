from codec.resources.request import Request


class Collections:
    def __init__(self, auth):
        self.auth = auth

    def create(self, name: str):
        endpoint = "/collection"
        response = Request(self.auth).post(endpoint)
        
        return response
    
    def get(self, uid: str = None):
        if uid:
            endpoint = f"/collection/{uid}"
        else:
            endpoint = "/collection"
        
        response = Request(self.auth).get(endpoint)
        
        return response
