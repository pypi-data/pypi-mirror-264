import unittest
from unittest.mock import patch, MagicMock, ANY

from jfrog_ml._artifactory_api import ArtifactoryApi


class TestArtifactoryApi(unittest.TestCase):

    @patch('builtins.open', new_callable=MagicMock)
    @patch('jfrog_ml.http.http_client')
    @patch('os.stat')
    def test_upload_file_successfully(self, mock_stat, mock_http_client, mock_open):
        mock_response = MagicMock()
        mock_response.return_value = 200
        mock_http_client.put.return_value = mock_response
        mock_stat.return_value.st_size = 100

        mock_file = MagicMock()
        mock_file.path = "full/file/path"
        mock_open.return_value = mock_file

        ArtifactoryApi(uri='http://domain', auth=None, http_client=mock_http_client).upload_file(mock_file.path,
                                                                                                 'http://url/to/upload')
        mock_open.assert_called_once_with(mock_file.path, 'rb')
        mock_response.raise_for_status.assert_called_once()
        mock_http_client.put.assert_called_once_with(url='http://url/to/upload', payload=ANY)

    @patch('os.stat')
    def test_upload_file_not_found(self, mock_stat):
        mock_stat.side_effect = FileNotFoundError("No such file or directory")
        with self.assertRaises(FileNotFoundError):
            ArtifactoryApi("http://domain", "auth").upload_file("file_not_found", "URL")

    @patch('builtins.open', new_callable=MagicMock)
    @patch('jfrog_ml.http.http_client')
    @patch('os.stat')
    def test_upload_file_timeout(self, mock_stat, mock_http_client, mock_open):
        mock_http_client.put.side_effect = TimeoutError("Connection timed out")
        mock_stat.return_value.st_size = 100

        mock_file = MagicMock()
        mock_file.path = "full/file/path"
        mock_open.return_value = mock_file

        with self.assertRaises(TimeoutError):
            ArtifactoryApi(uri='http://domain', auth=None, http_client=mock_http_client).upload_file(mock_file.path,
                                                                                                     'http://example.com/upload')

    @patch('builtins.open', new_callable=MagicMock)
    @patch('jfrog_ml.http.http_client')
    @patch('os.path.exists', return_value=True)
    @patch('os.remove', return_value=True)
    def test_download_file_timeout(self, mock_remove, mock_path_exists, mock_http_client, mock_open):
        mock_http_client.get.side_effect = TimeoutError("Connection timed out")

        with self.assertRaises(TimeoutError):
            ArtifactoryApi(uri='http://domain', auth=None, http_client=mock_http_client).download_file("repo",
                                                                                                       "remote_file_path",
                                                                                                       "local_file_path")

        mock_open.assert_not_called()
        mock_remove.assert_called_with("local_file_path")

    @patch('builtins.open', new_callable=MagicMock)
    @patch('jfrog_ml.http.http_client')
    def test_download_file_not_found(self, mock_http_client, mock_open):
        mock_http_client.get.side_effect = FileNotFoundError("No such file or directory")

        with self.assertRaises(FileNotFoundError):
            ArtifactoryApi(uri='http://domain', auth=None, http_client=mock_http_client).download_file("repo",
                                                                                                       "remote_file_not_found_path",
                                                                                                       "local_path")

        mock_open.assert_not_called()
        mock_http_client.get.assert_called_with(url='http://domain/repo/remote_file_not_found_path', stream=True)

    @patch('builtins.open', create=True)
    @patch('jfrog_ml.http.http_client')
    def test_download_file_successfully(self, mock_http_client, mock_open):
        mock_response = MagicMock()
        mock_response.status_code.return_value = 200
        mock_response.iter_content.return_value = [b'data_chunk1', b'data_chunk2']
        mock_response.headers.get.return_value = len([b'data_chunk1', b'data_chunk2'])
        mock_http_client.get.return_value.__enter__.return_value = mock_response

        mock_file = MagicMock()
        mock_file.path = "full/file/path"
        mock_open.return_value = mock_file

        repository = 'repository_name'
        remote_file_path = 'path/to/remote/filename'
        local_path = 'path/to/local/file'

        ArtifactoryApi(uri='http://domain', auth=None, http_client=mock_http_client).download_file(repository,
                                                                                                   remote_file_path,
                                                                                                   local_path)
        mock_open.assert_called_once_with(local_path, 'wb')
        mock_response.raise_for_status.assert_called_once()
        mock_http_client.get.assert_called_once_with(url='http://domain/repository_name/path/to/remote/filename',
                                                     stream=True)
