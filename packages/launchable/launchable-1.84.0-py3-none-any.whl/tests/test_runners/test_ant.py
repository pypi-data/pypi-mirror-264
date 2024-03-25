import gzip
import json
import os
from pathlib import Path
from unittest import mock

import responses  # type: ignore

from tests.cli_test_case import CliTestCase


class AntTest(CliTestCase):
    test_files_dir = Path(__file__).parent.joinpath('../data/ant/').resolve()

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset(self):
        result = self.cli('subset', '--target', '10%', '--session',
                          self.session, 'ant', str(self.test_files_dir.joinpath('src').resolve()))
        self.assert_success(result)

        payload = json.loads(gzip.decompress(responses.calls[0].request.body).decode())

        expected = self.load_json_from_file(self.test_files_dir.joinpath('subset_result.json'))

        self.assert_json_orderless_equal(expected, payload)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_record_test_ant(self):
        result = self.cli('record', 'tests', '--session', self.session,
                          'ant', str(self.test_files_dir) + "/junitreport/TESTS-TestSuites.xml")
        self.assert_success(result)

        payload = json.loads(gzip.decompress(responses.calls[1].request.body).decode())

        def removeDate(data):
            for e in data["events"]:
                del e["created_at"]

        expected = self.load_json_from_file(self.test_files_dir.joinpath("record_test_result.json"))

        removeDate(payload)
        removeDate(expected)

        self.assert_json_orderless_equal(expected, payload)
