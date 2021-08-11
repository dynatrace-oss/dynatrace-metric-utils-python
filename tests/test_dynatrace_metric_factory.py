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

from dynatrace.metric.utils import DynatraceMetricsFactory, MetricError


class TestDynatraceMetricFactory(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = DynatraceMetricsFactory()
        cls.test_dims = {
            "dim1": "val1",
            "dim2": "val2",
        }
        # 01/01/2021 00:00:00
        cls.test_timestamp = 1609455600000
        # 01/01/1999 00:00:00
        cls.invalid_timestamp = 915145200000

    def test_create_int_gauge(self):
        metric = self.factory.create_int_gauge("mymetric", 100)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertIsNotNone(metric.get_dimensions())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("gauge,100", metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_gauge_dims(self):
        metric = self.factory.create_int_gauge("mymetric", 100, self.test_dims)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,100", metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_gauge_timestamp(self):
        metric = self.factory.create_int_gauge(
            "mymetric", 100, self.test_dims, self.test_timestamp)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,100", metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_int_gauge_invalid_timestamp(self):
        with self.assertRaises(MetricError):
            self.factory.create_int_gauge(
                "mymetric", 100, self.test_dims, self.invalid_timestamp
            )

    def test_create_float_gauge(self):
        metric = self.factory.create_float_gauge("mymetric", 123.456)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("gauge,123.456", metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_gauge_dims(self):
        metric = self.factory.create_float_gauge("mymetric", 123.456,
                                                 self.test_dims)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,123.456", metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_gauge_timestamp(self):
        metric = self.factory.create_float_gauge(
            "mymetric", 123.456, self.test_dims, self.test_timestamp)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,123.456", metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_float_gauge_invalid(self):
        with self.assertRaises(MetricError):
            self.factory.create_float_gauge("mymetric", math.nan)

        with self.assertRaises(MetricError):
            self.factory.create_float_gauge("mymetric", math.inf)

        with self.assertRaises(MetricError):
            self.factory.create_float_gauge("mymetric", -math.inf)

        with self.assertRaises(MetricError):
            self.factory.create_float_gauge(
                "mymetric", 100, self.test_dims, self.invalid_timestamp
            )

    def test_create_int_counter_delta(self):
        metric = self.factory.create_int_counter_delta("mymetric", 100)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertIsNotNone(metric.get_dimensions())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("count,delta=100",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_counter_delta_dims(self):
        metric = self.factory.create_int_counter_delta(
            "mymetric", 100, self.test_dims)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("count,delta=100",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_counter_delta_timestamp(self):
        metric = self.factory.create_int_counter_delta(
            "mymetric", 100, self.test_dims, self.test_timestamp)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("count,delta=100",
                         metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_int_counter_delta_invalid_timestamp(self):
        with self.assertRaises(MetricError):
            self.factory.create_int_counter_delta(
                "mymetric", 100, self.test_dims, self.invalid_timestamp
            )

    def test_create_float_counter_delta(self):
        metric = self.factory.create_float_counter_delta("mymetric", 123.456)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertIsNotNone(metric.get_dimensions())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("count,delta=123.456",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_counter_delta_dims(self):
        metric = self.factory.create_float_counter_delta(
            "mymetric", 123.456, self.test_dims)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("count,delta=123.456",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_counter_delta_timestamp(self):
        metric = self.factory.create_float_counter_delta(
            "mymetric", 123.456, self.test_dims, self.test_timestamp)
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("count,delta=123.456",
                         metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_float_counter_delta_invalid(self):
        with self.assertRaises(MetricError):
            self.factory.create_float_counter_delta("mymetric", math.nan)

        with self.assertRaises(MetricError):
            self.factory.create_float_counter_delta("mymetric", math.inf)

        with self.assertRaises(MetricError):
            self.factory.create_float_counter_delta("mymetric", -math.inf)

        with self.assertRaises(MetricError):
            self.factory.create_float_counter_delta(
                "mymetric", 123.456, self.test_dims, self.invalid_timestamp
            )

    def test_create_int_summary(self):
        metric = self.factory.create_int_summary(
            "mymetric", 2, 5, 13, 5
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertIsNotNone(metric.get_dimensions())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("gauge,min=2,max=5,sum=13,count=5",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_summary_dims(self):
        metric = self.factory.create_int_summary(
            "mymetric", 2, 5, 13, 5, self.test_dims
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,min=2,max=5,sum=13,count=5",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_int_summary_timestamp(self):
        metric = self.factory.create_int_summary(
            "mymetric", 2, 5, 13, 5, self.test_dims, self.test_timestamp
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,min=2,max=5,sum=13,count=5",
                         metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_int_summary_invalid_timestamp(self):
        with self.assertRaises(MetricError):
            self.factory.create_int_summary(
                "mymetric", 2, 5, 13, 5, self.test_dims, self.invalid_timestamp
            )

    def test_create_int_summary_invalid(self):
        with self.assertRaises(MetricError):
            self.factory.create_int_summary(
                "mymetric", 14, 5, 12, 4
            )

        with self.assertRaises(MetricError):
            self.factory.create_int_summary(
                "mymetric", 2, 5, 13, -1
            )

    def test_create_float_summary(self):
        metric = self.factory.create_float_summary(
            "mymetric", 2.3, 5.6, 13.4, 7
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertIsNotNone(metric.get_dimensions())
        self.assertFalse(metric.get_dimensions())
        self.assertEqual("gauge,min=2.3,max=5.6,sum=13.4,count=7",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_summary_dims(self):
        metric = self.factory.create_float_summary(
            "mymetric", 2.3, 5.6, 13.4, 7, self.test_dims
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,min=2.3,max=5.6,sum=13.4,count=7",
                         metric.get_value().serialize_value())
        self.assertIsNone(metric.get_timestamp())

    def test_create_float_summary_timestamp(self):
        metric = self.factory.create_float_summary(
            "mymetric", 2.3, 5.6, 13.4, 7, self.test_dims, self.test_timestamp
        )
        self.assertEqual("mymetric", metric.get_metric_name())
        self.assertEqual(self.test_dims, metric.get_dimensions())
        self.assertEqual("gauge,min=2.3,max=5.6,sum=13.4,count=7",
                         metric.get_value().serialize_value())
        self.assertEqual(str(self.test_timestamp), metric.get_timestamp())

    def test_create_float_summary_invalid_timestamp(self):
        with self.assertRaises(MetricError):
            self.factory.create_float_summary(
                "mymetric", 2.3, 5.6, 13.4, 7, self.test_dims,
                self.invalid_timestamp
            )

    def test_create_float_summary_invalid(self):
        with self.assertRaises(MetricError):
            self.factory.create_float_summary(
                "mymetric", 14.3, 5.6, 12.3, 4
            )

        with self.assertRaises(MetricError):
            self.factory.create_float_summary(
                "mymetric", 2.3, 5.6, 13.4, -1
            )

    def test_create_float_summary_invalid_values(self):
        values = [1.2, math.nan, math.inf, -math.inf]

        for i in values:
            for j in values:
                for k in values:
                    if i == j == k == 1.2:
                        # skip the only valid version
                        continue
                    else:
                        with self.assertRaises(MetricError):
                            self.factory.create_float_summary(
                                "mymetric", i, j, k, 1
                            )

    def test_create_metrics_with_empty_name(self):
        with self.assertRaises(MetricError):
            self.factory.create_int_gauge("", 100)

        with self.assertRaises(MetricError):
            self.factory.create_float_gauge("", 123.456)

        with self.assertRaises(MetricError):
            self.factory.create_int_counter_delta("", 100)

        with self.assertRaises(MetricError):
            self.factory.create_float_counter_delta("", 123.456)

        with self.assertRaises(MetricError):
            self.factory.create_int_summary("", 2, 5, 13, 4)
        with self.assertRaises(MetricError):
            self.factory.create_float_summary("", 2.2, 5.6, 13.4, 4)
