import gzip
import json
import os
from pathlib import Path
from unittest import mock

import responses  # type: ignore

from launchable.utils.session import read_session, write_build
from tests.cli_test_case import CliTestCase


class AdbTest(CliTestCase):
    test_files_dir = Path(__file__).parent.joinpath('../data/adb/').resolve()
    subset_input = """INSTRUMENTATION_STATUS: class=com.launchableinc.rocketcar.ExampleInstrumentedTest2
INSTRUMENTATION_STATUS: current=1
INSTRUMENTATION_STATUS: id=AndroidJUnitRunner
INSTRUMENTATION_STATUS: numtests=2
INSTRUMENTATION_STATUS: stream=
com.launchableinc.rocketcar.ExampleInstrumentedTest2:
INSTRUMENTATION_STATUS: test=useAppContext
INSTRUMENTATION_STATUS_CODE: 1
INSTRUMENTATION_STATUS: class=com.launchableinc.rocketcar.ExampleInstrumentedTest2
INSTRUMENTATION_STATUS: current=1
INSTRUMENTATION_STATUS: id=AndroidJUnitRunner
INSTRUMENTATION_STATUS: numtests=2
INSTRUMENTATION_STATUS: stream=.
INSTRUMENTATION_STATUS: test=useAppContext
INSTRUMENTATION_STATUS_CODE: 0
INSTRUMENTATION_STATUS: class=com.launchableinc.rocketcar.ExampleInstrumentedTest
INSTRUMENTATION_STATUS: current=2
INSTRUMENTATION_STATUS: id=AndroidJUnitRunner
INSTRUMENTATION_STATUS: numtests=2
INSTRUMENTATION_STATUS: stream=
com.launchableinc.rocketcar.ExampleInstrumentedTest:
INSTRUMENTATION_STATUS: test=useAppContext
INSTRUMENTATION_STATUS_CODE: 1
INSTRUMENTATION_STATUS: class=com.launchableinc.rocketcar.ExampleInstrumentedTest
INSTRUMENTATION_STATUS: current=2
INSTRUMENTATION_STATUS: id=AndroidJUnitRunner
INSTRUMENTATION_STATUS: numtests=2
INSTRUMENTATION_STATUS: stream=.
INSTRUMENTATION_STATUS: test=useAppContext
INSTRUMENTATION_STATUS_CODE: 0
INSTRUMENTATION_RESULT: stream=

Time: 0.011

OK (2 tests)


INSTRUMENTATION_CODE: -1
"""

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset(self):
        # emulate launchable record build
        write_build(self.build_name)

        result = self.cli('subset', '--target', '10%', 'adb', input=self.subset_input)
        self.assert_success(result)

        self.assertEqual(read_session(self.build_name), self.session)

        payload = json.loads(gzip.decompress(responses.calls[1].request.body).decode())
        expected = self.load_json_from_file(self.test_files_dir.joinpath('subset_result.json'))
        self.assert_json_orderless_equal(payload, expected)
