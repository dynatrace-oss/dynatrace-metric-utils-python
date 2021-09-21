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
from typing import Optional, Mapping

from ._metric import Metric
from ._metric_values import GaugeValue, CounterValueDelta, SummaryValue


# float and int are currently pointing at the same underlying function
# (e.g.: create_float_gauge and create_int_gauge both return a GaugeValue)
# The point of having two separate functions for float and int here is that
# if we ever need to change something down the line that is only valid for
# one of these types, the API stays the same, and only the underlying
# implementation changes.

class DynatraceMetricsFactory:
    """
    Use the DynatraceMetricFactory to create :class:`Metric` objects.
    """

    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        """
        Create a metrics factory.
        :param logger: An optional logger. If None is specified, creates one
        with the name of the class.
        """
        self.__logger = logger if logger else logging.getLogger(__name__)

    def create_int_gauge(self,
                         metric_name: str,
                         value: int,
                         dimensions: Optional[Mapping[str, str]] = None,
                         timestamp: Optional[float] = None,
                         ) -> Metric:
        """
        Creates a gauge metric for an integer.
        The value will be serialized as "gauge,[value]".
        :param metric_name: The name of the metric
        :param value: The value to be set on the metric.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating int gauge (%s) with value %d",
                            metric_name, value)

        return Metric(metric_name, GaugeValue(value), dimensions, timestamp)

    def create_float_gauge(self,
                           metric_name: str,
                           value: float,
                           dimensions: Optional[Mapping[str, str]] = None,
                           timestamp: Optional[float] = None,
                           ) -> Metric:
        """
        Creates a gauge metric for a float.
        The value will be serialized as "gauge,[value]".
        :param metric_name: The name of the metric
        :param value: The value to be set on the metric.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating float gauge (%s) with value %f",
                            metric_name, value)

        return Metric(metric_name, GaugeValue(value), dimensions, timestamp)

    def create_int_counter_delta(
        self,
        metric_name: str,
        value: int,
        dimensions: Optional[Mapping[str, str]] = None,
        timestamp: Optional[float] = None,
    ) -> Metric:
        """
        Creates a counter metric for an integer.
        The value will be serialized as "count,delta=[value]".
        Only a delta to the previously exported value should be specified here.
        :param metric_name: The name of the metric
        :param value: The value to be set on the metric.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating int counter (%s) with value %d",
                            metric_name, value)

        return Metric(metric_name, CounterValueDelta(value), dimensions,
                      timestamp)

    def create_float_counter_delta(
        self,
        metric_name: str,
        value: float,
        dimensions: Optional[Mapping[str, str]] = None,
        timestamp: Optional[float] = None,
    ) -> Metric:
        """
        Creates a counter metric for a float.
        The value will be serialized as "count,delta=[value]".
        Only a delta to the previously exported value should be specified here.
        :param metric_name: The name of the metric
        :param value: The value to be set on the metric.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating float counter (%s) with value %f",
                            metric_name, value)

        return Metric(metric_name, CounterValueDelta(value), dimensions,
                      timestamp)

    def create_int_summary(
        self,
        metric_name: str,
        min: int,
        max: int,
        sum: int,
        count: int,
        dimensions: Optional[Mapping[str, str]] = None,
        timestamp: Optional[float] = None,
    ) -> Metric:
        """
        Creates a summary metric for integers.
        The value will be serialized as
        "gauge,min=[min],max=[max],sum=[sum],count=[count]".
        :param metric_name: The name of the metric.
        :param min: The smallest value in the summary.
        :param max: The largest value in the summary.
        :param sum: The sum of all values in the summary.
        :param count: The number of observations combined in the summary.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating int summary (%s) with values: "
                            "min: %d, max: %d, sum: %d, count: %d",
                            metric_name, min, max, sum, count)

        return Metric(metric_name, SummaryValue(min, max, sum, count),
                      dimensions, timestamp)

    def create_float_summary(
        self,
        metric_name: str,
        min: float,
        max: float,
        sum: float,
        count: int,
        dimensions: Optional[Mapping[str, str]] = None,
        timestamp: Optional[float] = None,
    ) -> Metric:
        """
        Creates a summary metric for floats.
        The value will be serialized as
        "gauge,min=[min],max=[max],sum=[sum],count=[count]".
        :param metric_name: The name of the metric.
        :param min: The smallest value in the summary.
        :param max: The largest value in the summary.
        :param sum: The sum of all values in the summary.
        :param count: The number of observations combined in the summary.
        :param dimensions: An optional dictionary to add as dimensions on this
         metric.
        :param timestamp: An optional timestamp (Unix time, in milliseconds).
        :return: A :class:`Metric` object.
        """
        self.__logger.debug("creating float summary (%s) with values: "
                            "min: %f, max: %f, sum: %f, count: %f",
                            metric_name, min, max, sum, count)

        return Metric(metric_name, SummaryValue(min, max, sum, count),
                      dimensions, timestamp)
