import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import jfrog_ml
from jfrog_ml._log_config import logger


class HTTPClient:

    def __init__(self, auth, session: Optional[requests.Session] = None):
        self.auth = auth
        if session is None:
            self.session = self._create_session()
        self.timeout = os.getenv("JFML_TIMEOUT", default=10)

    def _create_session(self):
        session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=RetryWithLog(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]))
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def post(self, url, data=None, params=None, headers=None):
        new_headers = self._add_default_headers(headers, jfrog_ml.__version__)
        return self.session.post(url, auth=self.auth, timeout=self.timeout, data=data, params=params, headers=new_headers)

    def get(self, url, params=None, stream=False, headers=None):
        new_headers = self._add_default_headers(headers, jfrog_ml.__version__)
        return self.session.get(url, auth=self.auth, params=params, stream=stream, headers=new_headers)

    def put(self, url, payload=None, files=None, stream=False, headers=None):
        new_headers = self._add_default_headers(headers, jfrog_ml.__version__)
        return self.session.request(method="PUT", url=url, data=payload, auth=self.auth, files=files, stream=stream,
                                    timeout=self.timeout, headers=new_headers)

    @staticmethod
    def _add_default_headers(headers: dict, frogml_version: str):
        default_user_agent = 'frogml-sdk-python/{}'.format(frogml_version)
        if headers is not None:
            headers.setdefault('User-Agent', default_user_agent)
            return headers
        else:
            return {'User-Agent': default_user_agent}

class RetryWithLog(Retry):
    """
     Adding extra logs before making a retry request
    """

    def __init__(self, *args, **kwargs):
        history = kwargs.get("history")
        if history is not None:
            logger.info(f'Error: ${history[-1].error}\nretrying...')
        super().__init__(*args, **kwargs)
