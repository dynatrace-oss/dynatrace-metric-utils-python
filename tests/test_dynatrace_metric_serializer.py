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

from unittest import TestCase

from dynatrace.metric.utils import DynatraceMetricFactory, \
    DynatraceMetricSerializer, MetricError


class TestDynatraceMetricSerializer(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_dims = {
            "dim1": "val1",
        }
        # 01/01/2021 00:00:00
        cls.test_timestamp = 1609455600000

        cls.factory = DynatraceMetricFactory()

    def test_default(self):
        # turn off enrichment to not break on systems that have a oneagent
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )

        self.assertEqual(
            "metric gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_with_metric_dims(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False)

        self.assertEqual(
            "metric,dim1=val1 gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, self.test_dims)
            ))

    def test_dimensions_normalized(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False)

        test_dims = {
            "dim~1": "\\=\" ==",
            "  dim 2!@": "\u0000val\u0009"
        }

        self.assertEqual(
            "metric,dim_1=\\\\\\=\\\"\\ \\=\\=,_dim_2_=_val_ gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, test_dims)
            ))

    def test_with_timestamp(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False)
        self.assertEqual(
            "metric gauge,100 " + str(self.test_timestamp),
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, None,
                                              self.test_timestamp)
            ))

    def test_with_metric_dims_and_timestamp(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False)
        self.assertEqual(
            "metric,dim1=val1 gauge,100 " + str(self.test_timestamp),
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, self.test_dims,
                                              self.test_timestamp)
            ))

    def test_with_prefix(self):
        # first parameter is the logger, which we dont need here.
        serializer = DynatraceMetricSerializer(
            None, "prefix", enrich_with_dynatrace_metadata=False
        )

        self.assertEqual(
            "prefix.metric gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_with_prefix_trailing_dot(self):
        # first parameter is the logger, which we dont need here.
        serializer = DynatraceMetricSerializer(
            None, "prefix.", enrich_with_dynatrace_metadata=False
        )

        self.assertEqual(
            "prefix.metric gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_with_default_dimensions(self):
        default_dims = {"default1": "value1", "default2": "value2"}
        serializer = DynatraceMetricSerializer(
            None, None, default_dims, enrich_with_dynatrace_metadata=False,
        )

        self.assertEqual(
            "metric,default1=value1,default2=value2 gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_metrics_source(self):
        serializer = DynatraceMetricSerializer(
            None, None, None, False, "test_source"
        )

        self.assertEqual(
            "metric,dt.metrics.source=test_source gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_metrics_source_escaped(self):
        serializer = DynatraceMetricSerializer(
            None, None, None, False, "test source!"
        )

        self.assertEqual(
            "metric,dt.metrics.source=test\\ source! gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100)
            ))

    def test_dimension_precedence(self):
        default_dims = {
            "dim1": "default1",
            "dim2": "default2",
            "dim3": "default3",
        }
        metric_dims = {
            "dim2": "metric2",
            "dim3": "metric3",
        }

        static_dims = {
            "dim3": "static3"
        }

        serializer = DynatraceMetricSerializer(
            None, None, default_dims, False
        )
        # setting a private variable from the outside should not be done but
        # is done here for testing purposes.
        serializer._DynatraceMetricSerializer__static_dimensions = static_dims

        self.assertEqual(
            "metric,dim1=default1,dim2=metric2,dim3=static3 gauge,100",
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, metric_dims)))

    def test_merge_correctly(self):
        default_dims = {
            "dim1": "default1",
            "dim2": "default2",
            "dim3": "default3",
        }
        metric_dims = {
            "dim2": "metric2",
            "dim3": "metric3",
        }
        static_dims = {
            "dim3": "static3"
        }

        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )
        merged = serializer._DynatraceMetricSerializer__merge_dimensions(
            [default_dims, metric_dims, static_dims]
        )
        self.assertDictEqual(
            {
                "dim1": "default1",
                "dim2": "metric2",
                "dim3": "static3"
            },
            merged
        )

    def test_merge_disjunct_keys(self):
        a = {"a1": "a1", "a2": "a2", "a3": "a3"}
        b = {"b1": "b1", "b2": "b2", "b3": "b3"}
        c = {"c1": "c1", "c2": "c2", "c3": "c3"}

        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )
        merged = serializer._DynatraceMetricSerializer__merge_dimensions(
            [a, b, c]
        )

        self.assertEqual(
            {
                "a1": "a1", "a2": "a2", "a3": "a3", "b1": "b1", "b2": "b2",
                "b3": "b3", "c1": "c1", "c2": "c2", "c3": "c3"
            },
            merged
        )

    def test_invalid_metric_key(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )

        self.assertEqual(
            "_ gauge,100",
            serializer.serialize(self.factory.create_int_gauge("!@#$", 100))
        )

    def test_empty_metric_key(self):
        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )
        with self.assertRaises(MetricError):
            serializer.serialize(self.factory.create_int_gauge("", 100))

    def test_serialized_line_too_long(self):
        test_dims = {}
        for i in range(20):
            test_dims["a" * 50 + str(i)] = "b" * 50 + str(i)

        serializer = DynatraceMetricSerializer(
            enrich_with_dynatrace_metadata=False
        )
        with self.assertRaises(MetricError):
            serializer.serialize(
                self.factory.create_int_gauge("metric", 100, test_dims)
            )
