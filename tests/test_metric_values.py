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
import sys
from unittest import TestCase

from dynatrace.metric.utils import MetricError
from dynatrace.metric.utils._metric_values import *
from dynatrace.metric.utils._metric_values import _format_number


class TestGaugeValue(TestCase):
    def test_serialize_value(self):
        int_gauge = GaugeValue(2)
        self.assertEqual("gauge,2", int_gauge.serialize_value())

        float_gauge = GaugeValue(2.3)
        self.assertEqual("gauge,2.3", float_gauge.serialize_value())

        negative_gauge = GaugeValue(-3.4)
        self.assertEqual("gauge,-3.4", negative_gauge.serialize_value())

    def test_invalid(self):
        with self.assertRaises(MetricError):
            GaugeValue(math.nan)

        with self.assertRaises(MetricError):
            GaugeValue(math.inf)

        with self.assertRaises(MetricError):
            GaugeValue(-math.inf)


class TestCounterValueDelta(TestCase):
    def test_serialize_value(self):
        int_counter = CounterValueDelta(3)
        self.assertEqual("count,delta=3", int_counter.serialize_value())

        float_counter = CounterValueDelta(2.3)
        self.assertEqual("count,delta=2.3", float_counter.serialize_value())

        negative_counter = CounterValueDelta(-3.4)
        self.assertEqual("count,delta=-3.4",
                         negative_counter.serialize_value())

    def test_invalid(self):
        with self.assertRaises(MetricError):
            CounterValueDelta(math.nan)

        with self.assertRaises(MetricError):
            CounterValueDelta(math.inf)

        with self.assertRaises(MetricError):
            CounterValueDelta(-math.inf)


class TestSummaryValue(TestCase):
    def test_serialize_value(self):
        int_summary = SummaryValue(0, 3, 4, 4)
        self.assertEqual("gauge,min=0,max=3,sum=4,count=4",
                         int_summary.serialize_value())

        float_summary = SummaryValue(0.1, 3.4, 5.6, 3)
        self.assertEqual("gauge,min=0.1,max=3.4,sum=5.6,count=3",
                         float_summary.serialize_value())

    def test_min_larger_than_max(self):
        with self.assertRaises(MetricError):
            SummaryValue(7, 3, 10, 4)

        with self.assertRaises(MetricError):
            SummaryValue(7.4, 3.2, 10.2, 4)

    def test_invalid(self):
        values = [1.2, -math.inf, math.inf, math.nan]
        for i in values:
            for j in values:
                for k in values:
                    if i == j == k == 1.2:
                        self.assertEqual(
                            "gauge,min=1.2,max=1.2,sum=1.2,count=1",
                            SummaryValue(i, j, k, 1).serialize_value()
                        )
                    else:
                        # any other combination is somehow invalid.
                        with self.assertRaises(MetricError):
                            SummaryValue(i, j, k, 1)

    def test_negative_count(self):
        with self.assertRaises(MetricError):
            SummaryValue(1, 3, 5, -3)

        with self.assertRaises(MetricError):
            SummaryValue(1.2, 3.4, 5.6, -3)


class TestFloatFormatting(TestCase):
    def test__format_number(self):
        self.assertEqual("0", _format_number(0))
        self.assertEqual("0", _format_number(-0))
        self.assertEqual("0", _format_number(0.0))
        self.assertEqual("0", _format_number(-0.0))
        self.assertEqual("0", _format_number(.0000000000000))
        self.assertEqual("0", _format_number(-0.0000000000000))
        self.assertEqual("1", _format_number(1.0000000000000))
        self.assertEqual("123.456", _format_number(123.456))
        self.assertEqual("-123.456", _format_number(-123.456))
        self.assertEqual("0.3333333333333333", _format_number(1.0 / 3))
        self.assertEqual("1.79769313e+308",
                         _format_number(sys.float_info.max))
        self.assertEqual("-1.79769313e+308",
                         _format_number(-sys.float_info.max))
        # smallest positive float.
        self.assertEqual("2.22507386e-308",
                         _format_number(sys.float_info.min))
        self.assertEqual("1.0e+100", _format_number(1e100))
        self.assertEqual("1.0e-100", _format_number(1e-100))
        self.assertEqual("-1.0e+100", _format_number(-1e100))
        self.assertEqual("-1.0e-100", _format_number(-1e-100))
        self.assertEqual("1.234e+100", _format_number(1.234e100))
        self.assertEqual("1.234e-100", _format_number(1.234e-100))
        self.assertEqual("-1.234e+100", _format_number(-1.234e100))
        self.assertEqual("-1.234e-100", _format_number(-1.234e-100))
        self.assertEqual("1.0e+18", _format_number(1_000_000_000_000_000_000))
        self.assertEqual("-1.0e+18", _format_number(-1_000_000_000_000_000_000))
        self.assertEqual("1.1e+18", _format_number(1_100_000_000_000_000_000))
        self.assertEqual("-1.1e+18", _format_number(-1_100_000_000_000_000_000))
        self.assertEqual("1.0e-18", _format_number(0.000_000_000_000_000_001))
        self.assertEqual("-1.0e-18", _format_number(-0.000_000_000_000_000_001))
        self.assertEqual("1.234e+18", _format_number(1_234_000_000_000_000_000))
        self.assertEqual("-1.234e+18",
                         _format_number(-1_234_000_000_000_000_000))
        self.assertEqual("1.234e-18",
                         _format_number(0.000_000_000_000_000_001_234))
        self.assertEqual("-1.234e-18",
                         _format_number(-0.000_000_000_000_000_001_234))
        self.assertEqual("1.1234567890123457",
                         _format_number(1.1234567890123456789))
        self.assertEqual("-1.1234567890123457",
                         _format_number(-1.1234567890123456789))
        self.assertEqual("200", _format_number(200.00000000000))
        self.assertEqual("-200", _format_number(-200.000000000000))

        # these should never happen.
        self.assertEqual("nan", _format_number(math.nan))
        self.assertEqual("inf", _format_number(math.inf))
        self.assertEqual("-inf", _format_number(-math.inf))
