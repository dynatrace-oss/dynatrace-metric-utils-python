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

class DynatraceMetricFactory:
    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def create_int_gauge(self,
                         metric_name: str,
                         value: int,
                         dimensions: Optional[Mapping[str, str]] = None,
                         timestamp: Optional[
                             float] = None,
                         ) -> Metric:
        self.__logger.debug("creating int gauge (%s) with value %d",
                            metric_name, value)

        return Metric(metric_name, GaugeValue(value), dimensions, timestamp)

    def create_float_gauge(self,
                           metric_name: str,
                           value: float,
                           dimensions: Optional[Mapping[str, str]] = None,
                           timestamp: Optional[float] = None,
                           ) -> Metric:
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
        self.__logger.debug("creating int counter (%s) with value %d",
                            metric_name, value)

        return Metric(metric_name, CounterValueDelta(value), dimensions,
                      timestamp)

    def create_float_counter_delta(
        self,
        metric_name: str,
        value: int,
        dimensions: Optional[Mapping[str, str]] = None,
        timestamp: Optional[float] = None,
    ) -> Metric:
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
        self.__logger.debug("creating float summary (%s) with values: "
                            "min: %f, max: %f, sum: %f, count: %f",
                            metric_name, min, max, sum, count)

        return Metric(metric_name, SummaryValue(min, max, sum, count),
                      dimensions, timestamp)
