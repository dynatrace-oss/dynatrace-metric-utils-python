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
import time

from dynatrace.metric.utils.dynatrace_metric_serializer import \
    DynatraceMetricSerializer
from dynatrace.metric.utils.metrics import MetricFactory

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    serializer = DynatraceMetricSerializer(
        "prefix",
        {"default": "dim"},
        True,
        "python-utils-example",
        logger.getChild(DynatraceMetricSerializer.__name__),
    )
    metrics_factory = MetricFactory(
        logger.getChild(MetricFactory.__name__)
    )

    double_gauge = metrics_factory.create_double_gauge(
        "double.gauge",
        2.3,
        {"metric": "dim"},
        time.time(),
    )

    serialized_double_gauge = serializer.serialize(double_gauge)
    print(serialized_double_gauge)
