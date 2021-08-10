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

from dynatrace.metric.utils import MetricError
from dynatrace.metric.utils._metric import Metric
from dynatrace.metric.utils._metric_values import GaugeValue


class TestMetric(unittest.TestCase):
    def test_defaults(self):
        metric = Metric("name", GaugeValue(2))
        self.assertEqual("name", metric.get_metric_name())
        self.assertEqual("gauge,2", metric.get_value().serialize_value())
        self.assertEqual({}, metric.get_dimensions())
        self.assertEqual(None, metric.get_timestamp())

    def test_with_dimensions(self):
        dims = {"key": "val", "key2": "val2"}
        metric = Metric("name", GaugeValue(2), dims)
        self.assertEqual("name", metric.get_metric_name())
        self.assertEqual("gauge,2", metric.get_value().serialize_value())
        self.assertDictEqual(dims, dict(metric.get_dimensions()))
        self.assertEqual(None, metric.get_timestamp())

    def test_with_timestamp(self):
        # 01/01/2021
        metric = Metric("name", GaugeValue(2), timestamp=1609455600000)
        self.assertEqual("name", metric.get_metric_name())
        self.assertEqual("gauge,2", metric.get_value().serialize_value())
        self.assertEqual({}, metric.get_dimensions())
        self.assertEqual("1609455600000", metric.get_timestamp())

    def test_invalid_timestamp(self):
        # 01/01/1999
        with self.assertRaises(MetricError):
            Metric("name", GaugeValue(2), timestamp=915145200000)

        # 01/01/3000 00:00:01
        with self.assertRaises(MetricError):
            Metric("name", GaugeValue(2), timestamp=32503676401000)

    def test_empty_metric_name(self):
        with self.assertRaises(MetricError):
            Metric("", GaugeValue(2))

