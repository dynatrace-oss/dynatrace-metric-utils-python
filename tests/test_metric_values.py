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
import math
from unittest import TestCase

from dynatrace.metric.utils import MetricError
from dynatrace.metric.utils._metric_values import GaugeValue


class TestGaugeValue(TestCase):
    def test_serialize_value(self):
        int_gauge = GaugeValue(2)
        self.assertEqual("gauge,2", int_gauge.serialize_value())

        float_gauge = GaugeValue(2.3)
        self.assertEqual("gauge,2.3", float_gauge.serialize_value())

    def test_invalid(self):
        with self.assertRaises(MetricError):
            GaugeValue(math.nan)
            
        with self.assertRaises(MetricError):
            GaugeValue(math.inf)

        with self.assertRaises(MetricError):
            GaugeValue(-math.inf)


# todo counter and summary values

