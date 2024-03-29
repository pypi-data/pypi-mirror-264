from codec.utils.file_utils import validate_path_and_get_filename
from codec.constants import SUPABASE_URL, SUPABASE_PUBLIC_KEY
from codec.resources.request import Request
from supabase import create_client


supabase = create_client(
    supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_PUBLIC_KEY
)


def _upload_video(path, auth, collection):
    # Validate video path and get video filename
    filename = validate_path_and_get_filename(path)
    file_extension = filename.split(".")[-1]

    # Upload video
    pre_upload_endpoint = "/upload/pre"
    pre_upload_response = Request(auth).post(
        pre_upload_endpoint,
        body={
            "original_filename": filename,
            "collection": collection
        }
    )

    with open(path, "rb") as f:
        supabase.storage.from_("codec-multi").upload_to_signed_url(
            path=pre_upload_response.path,
            token=pre_upload_response.token,
            file=f,
            file_options={
                "content-type": f"video/{file_extension}"
            }
        )

    return pre_upload_response


class Videos:
    def __init__(self, auth):
        self.auth = auth

    def get(self, uid: str, expand: list = None):
        endpoint = f"/video/{uid}"

        expand_parameter = None if expand is None else {"expand": ",".join(expand)}
        response = Request(self.auth).get(endpoint, params=expand_parameter)

        return response

    def delete(self, uid: str):
        endpoint = f"/video/{uid}"
        response = Request(self.auth).delete(endpoint)

        return response
    
    def upload(self, path: str, collection: str):
        response = _upload_video(path=path, auth=self.auth, collection=collection)

        return response

    def index(self, uid: str):
        endpoint = f"/index/search/{uid}"
        response = Request(self.auth).post(endpoint)

        return response
