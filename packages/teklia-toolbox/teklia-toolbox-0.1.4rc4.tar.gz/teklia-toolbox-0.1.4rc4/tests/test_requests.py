from unittest import TestCase
from unittest.mock import patch

import requests_mock
from apistar.exceptions import ErrorResponse

from teklia_toolbox.requests import retried_request


@requests_mock.Mocker()
@patch(
    "teklia_toolbox.requests.retried_request.retry.wait",
    0,
)
class TestRetriedRequest(TestCase):
    def test_retried_request_only_500(self, mock):
        mock.get("https://arkindex.teklia.com/api/v1/corpus/notfound/", status_code=404)

        with self.assertRaises(ErrorResponse) as e:
            retried_request("RetrieveCorpus", id="notfound")

        self.assertEqual(e.exception.status_code, 404)
        self.assertListEqual(
            [(req.method, req.url) for req in mock.request_history],
            [
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/notfound/"),
            ],
        )

    def test_retried_request_5_attempts(self, mock):
        mock.get("https://arkindex.teklia.com/api/v1/corpus/corpusid/", status_code=500)

        with self.assertRaises(ErrorResponse) as e:
            retried_request("RetrieveCorpus", id="corpusid")

        self.assertEqual(e.exception.status_code, 500)
        self.assertListEqual(
            [(req.method, req.url) for req in mock.request_history],
            [
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/corpusid/"),
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/corpusid/"),
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/corpusid/"),
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/corpusid/"),
                ("GET", "https://arkindex.teklia.com/api/v1/corpus/corpusid/"),
            ],
        )
