import unittest

from main import process_get_request, HttpClass, SearchRepo
import requests_mock
import pytest


def test_process_get_request():
    url = 'https://api.github.com'
    with requests_mock.Mocker() as mocker:
        # Mock a successful response
        mock_response_success = {"key": "value"}
        mocker.get(url, json=mock_response_success, status_code=200)

        # Test the process_get_request function
        result = process_get_request(url)
        assert result == {"key": "value"}


def test_process_get_request_without_context_manager():
    # this doesn't work
    url = 'https://api.github.com'
    mocker = requests_mock.Mocker()
    mock_response_success = {"key": "value"}
    mocker.get(url, json=mock_response_success, status_code=200)

    result = process_get_request(url)
    assert result == {"key": "value"}


def test_process_get_request_with_mocker(mocker):
    mock_response = mocker.Mock(status_code=200)
    mock_response.json.return_value = {"key": "value"}
    mocker.patch("requests.get", return_value=mock_response)

    http_test_obj = HttpClass()
    result = http_test_obj.process_get_request('https://api.github.com')

    assert result == {"key": "value"}


class TestHttpClass:
    def test_process_get_request(self):
        url = 'https://api.github.com'
        with requests_mock.Mocker() as mocker:
            # Mock a successful response
            mock_response_success = {"key": "value"}
            mocker.get(url, json=mock_response_success, status_code=200)

            # Test the process_get_request method of the HttpClass
            http_test_obj = HttpClass()
            result = http_test_obj.process_get_request(url)
            assert result == {"key": "value"}

    @pytest.mark.parametrize(
        "url, expected_status, expected_result",
        [
            ("https://example.com/api/data", 200, {"key": "value"}),
            ("https://example.com/api/404", 404, None),
            # Add more test cases as needed
        ],
    )
    def test_process_get_request(self, url, expected_status, expected_result):
        with requests_mock.Mocker() as mocker:
            mocker.get(url, json=expected_result, status_code=expected_status)
            # Test the process_get_request method of the HttpClass
            http_test_obj = HttpClass()
            result = http_test_obj.process_get_request(url)
            assert result == expected_result


@unittest.mock.patch("main.HttpClass.process_get_request")
def test_search_repo_with_name_using_patch(mock_get_request):
    mock_get_request.return_value = {
        "repos": ["repo1", "repo2", "repo3"]
    }

    search_repo_obj = SearchRepo()
    result = search_repo_obj.search_repo_with_name('https://api.github.com', "repo2")
    assert result is True


def test_search_repo_with_name_using_patch_object():
    search_repo_obj = SearchRepo()

    with unittest.mock.patch.object(search_repo_obj, "call_http_class") as mock_call_http_class:
        mock_call_http_class.return_value = {
            "repos": ["repo1", "repo2", "repo3"]
        }

        result = search_repo_obj.search_repo_with_name('https://api.github.com', "repo2")
        assert result is True


def test_search_repo_with_name_error_using_patch():
    # Create an instance of SearchRepo
    search_repo_obj = SearchRepo()

    # Patch the process_get_request method within HttpClass
    with unittest.mock.patch("main.HttpClass.process_get_request") as mock_process_get_request:
        mock_process_get_request.return_value = None  # Simulate no response

        # Assert that ValueError is raised
        with pytest.raises(ValueError, match="No response received from the API"):
            search_repo_obj.search_repo_with_name('https://api.github.com', "repo2")
