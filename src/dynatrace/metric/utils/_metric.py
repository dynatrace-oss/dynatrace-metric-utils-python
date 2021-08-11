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

from typing import Optional, Mapping

from ._metric_values import MetricValue
from .metric_error import MetricError


class Metric:
    """
    Class that holds created metrics. Every metric contains a class derived
     from :class:`MetricValue`, which specifies the serialization logic.
    """

    def __init__(self,
                 metric_name: str,
                 value: MetricValue,
                 dimensions: Optional[Mapping[str, str]] = None,
                 timestamp: Optional[int] = None
                 ) -> None:
        """
        Create a new metric. Should not be called by the user.
        :param metric_name: The name of the metric. Cannot be None or empty.
        :param value: The :class:`MetricValue` to add
        :param dimensions: Optional dimensions for this metric
        :param timestamp: Optional timestamp in milliseconds (Unix time * 1000)
        """
        if not metric_name:
            raise MetricError("Metric name cannot be empty")

        self.__metric_name = metric_name
        self.__value = value
        self.__dimensions = dimensions if dimensions else {}

        if timestamp:
            # timestamp between the year 2000 and 3000
            if 946681200000 <= timestamp < 32503676400000:
                self.__timestamp = str(int(round(timestamp)))
            else:
                raise MetricError('timestamp needs to be between the years '
                                  '2000 and 3000 and specified in '
                                  'milliseconds.')
        else:
            self.__timestamp = None

    def get_metric_name(self) -> str:
        return self.__metric_name

    def get_value(self) -> MetricValue:
        return self.__value

    def get_dimensions(self) -> Mapping[str, str]:
        return self.__dimensions

    def get_timestamp(self) -> Optional[str]:
        return self.__timestamp
