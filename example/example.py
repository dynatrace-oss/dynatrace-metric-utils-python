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


import logging
import math
import time

from dynatrace.metric.utils import (
    DynatraceMetricSerializer,
    DynatraceMetricFactory,
    MetricError,
)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    metric_factory = DynatraceMetricFactory(
        logger.getChild(DynatraceMetricFactory.__name__)
    )

    default_serializer = DynatraceMetricSerializer(
        logger.getChild(DynatraceMetricSerializer.__name__)
    )

    serializer_with_prefix_and_dimensions = DynatraceMetricSerializer(
        logger.getChild(DynatraceMetricSerializer.__name__),
        "prefix",
        {"default": "dim"},
        True,
        "python-utils-example",
    )
    metric_dims = {"metric_dim": "val"}
    # metric_dims = {}

    current_milliseconds = time.time() * 1000

    metrics = [
        metric_factory.create_int_gauge(
            "int.gauge", 2, metric_dims, current_milliseconds),
        metric_factory.create_float_gauge(
            "float.gauge", 2.3, metric_dims, current_milliseconds),
        metric_factory.create_int_counter_delta(
            "int.counter", 3, metric_dims, current_milliseconds),
        metric_factory.create_float_counter_delta(
            "float.counter", 3.14, metric_dims, current_milliseconds),
        metric_factory.create_int_summary(
            "int.summary", 0, 3, 5, 4, metric_dims, current_milliseconds),
        metric_factory.create_float_summary(
            "float.summary", 0.1, 3.4, 5.6, 4, metric_dims, current_milliseconds),
    ]

    for metric in metrics:
        # print the metric
        print(default_serializer.serialize(metric))
        # print the same metric with metric key prefix, metrics source,
        # and default dimensions
        print(serializer_with_prefix_and_dimensions.serialize(metric))

    try:
        metric_factory.create_int_gauge("", 2)
    except MetricError as err:
        print("MetricError:", err)

    try:
        metric_factory.create_float_gauge("nan.gauge", math.nan)
    except MetricError as err:
        print("MetricError:", err)

    try:
        metric_factory.create_float_gauge("inf.gauge", math.inf)
    except MetricError as err:
        print("MetricError:", err)

    try:
        default_serializer.serialize(
            metric_factory.create_float_gauge(
                "line.too.long", 3.2,
                dict([
                    ("some_long_dimension_key{}".format(x),
                     "some_equally_long_dimension_value{}".format(x))
                    for x in range(33)
                ])
            ))
    except MetricError as err:
        print("MetricError:", err)
