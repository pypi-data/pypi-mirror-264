from urllib.parse import urlparse

from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


def join_url(base_uri, *parts):
    cleaned_parts = [part.strip("/") for part in parts if part.strip("/")]
    return f"{base_uri}/{'/'.join(cleaned_parts)}"


def extract_uri_and_repo_name(uri):
    parsed_url = urlparse(uri)
    if parsed_url.scheme not in ["http", "https"]:
        raise Exception(f"Not a valid Artifactory URI: {uri}. "
                        f"Artifactory URI example: `https://frogger.jfrog.io/artifactory/ml-local`")
    path_segments = parsed_url.path.strip('/').split('/')
    if len(path_segments) != 1 or path_segments[0] != 'artifactory':
        raise Exception(f"Not a valid Artifactory URI: {uri}. "
                        f"Artifactory URI example: `https://frogger.jfrog.io/artifactory`")
    artifactory_uri = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_segments[0]}"
    return artifactory_uri

def extract_uri_and_artifact_path(uri):
    parsed_url = urlparse(uri)
    if parsed_url.scheme not in ["http", "https"]:
        raise Exception(f"Not a valid Artifactory URI: {uri}. "
                        f"Artifactory URI example: `https://frogger.jfrog.io/artifactory/ml-local`")
    path_segments = parsed_url.path.strip('/').split('/')
    if len(path_segments) < 2 or path_segments[0] != 'artifactory' or not path_segments[1]:
        raise Exception(f"Not a valid Artifactory URI: {uri}. "
                        f"Artifactory URI example: `https://frogger.jfrog.io/artifactory/ml-local`")
    artifactory_uri = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_segments[0]}"

    # iterate over path_segments[] to the end of it and join them with a "/" to get the artifact path
    artifact_path = "/".join(path_segments[1:])

    return artifactory_uri, artifact_path