#  Copyright 2021 Dynatrace LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from dynatrace.metric.utils._normalize import Normalize


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.normalizer = Normalize()

    def test_normalize_metric_key(self):
        self.assertEqual("asdf", self.normalizer.normalize_metric_key("asdf"))


if __name__ == '__main__':
    unittest.main()
