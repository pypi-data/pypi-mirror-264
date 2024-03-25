import unittest
from unittest.mock import patch

from jfrog_ml.http.http_client import HTTPClient


class TestHttpClient(unittest.TestCase):

    @patch('jfrog_ml.http.http_client.HTTPClient._add_default_headers')
    @patch('requests.Session.post')
    def test_post_calls_add_default_headers_once(self, mock_post, mock_add_default_headers):
        auth = ('username', 'password')
        client = HTTPClient(auth)

        # Call the post method
        url = 'https://example.com/api/post'
        client.post(url)

        # Assert that _add_default_headers was called once
        mock_add_default_headers.assert_called_once()

        # Assert that session.post was called once
        mock_post.assert_called_once()

    @patch('jfrog_ml.http.http_client.HTTPClient._add_default_headers')
    @patch('requests.Session.get')
    def test_get_calls_add_default_headers_once(self, mock_get, mock_add_default_headers):
        auth = ('username', 'password')
        client = HTTPClient(auth)

        # Call the get method
        url = 'https://example.com/api/post'
        client.get(url)

        # Assert that _add_default_headers was called once
        mock_add_default_headers.assert_called_once()

        # Assert that session.get was called once
        mock_get.assert_called_once()

    @patch('jfrog_ml.http.http_client.HTTPClient._add_default_headers')
    @patch('requests.Session.request')
    def test_put_calls_add_default_headers_once(self, mock_requests, mock_add_default_headers):
        auth = ('username', 'password')
        client = HTTPClient(auth)

        # Call the put method
        url = 'https://example.com/api/post'
        client.put(url)

        # Assert that _add_default_headers was called once
        mock_add_default_headers.assert_called_once()

        # Assert that session.requests was called once
        mock_requests.assert_called_once()

    def test_add_default_headers_received_non_none_headers(self):
        auth = ('username', 'password')
        client = HTTPClient(auth)
        headers = {'Content-Type': 'application/json'}
        new_headers = client._add_default_headers(headers, '1.0.0')
        expected_headers = {'Content-Type': 'application/json', 'User-Agent': 'frogml-sdk-python/1.0.0'}
        self.assertEqual(new_headers, expected_headers)

    def test_add_default_headers_received_none_headers(self):
        auth = ('username', 'password')
        client = HTTPClient(auth)
        new_headers = client._add_default_headers(None, '2.0.0')
        expected_headers = {'User-Agent': 'frogml-sdk-python/2.0.0'}
        self.assertEqual(new_headers, expected_headers)


