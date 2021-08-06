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

from . import _metric_values


class Metric:
    def __init__(self,
                 metric_name: str,
                 value: _metric_values.MetricValue,
                 dimensions: Optional[Mapping[str, str]] = None,
                 timestamp: Optional[int] = None
                 ) -> None:
        self.__metric_name = metric_name
        self.__value = value
        self.__dimensions = dimensions if dimensions else {}
        self.__timestamp = str(
            int(round(timestamp * 1000))) if timestamp else None

    def get_metric_name(self) -> str:
        return self.__metric_name

    def get_value(self) -> _metric_values.MetricValue:
        return self.__value

    def get_dimensions(self) -> Mapping[str, str]:
        return self.__dimensions

    def get_timestamp(self) -> Optional[str]:
        return self.__timestamp


class MetricFactory:
    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def create_double_gauge(self,
                            metric_name: str,
                            value: float,
                            dimensions: Optional[Mapping[str, str]] = None,
                            timestamp: Optional[float] = None,
                            ) -> Metric:
        # todo check not empty etc.
        self.__logger.debug("creating double gauge with value %f", value)
        return Metric(metric_name, _metric_values.GaugeValue(value),
                      dimensions, timestamp)
