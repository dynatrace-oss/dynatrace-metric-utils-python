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
from abc import ABC, abstractmethod
from typing import Union
from . import (
    metric_error,
)


def _raise_if_nan_or_inf(value: Union[int, float]):
    if math.isnan(value):
        raise metric_error.MetricError("Value is NaN")
    if math.isinf(value):
        raise metric_error.MetricError("Value is Infinite")


class MetricValue(ABC):
    @abstractmethod
    def serialize_value(self) -> str:
        pass


class GaugeValue(MetricValue):
    def __init__(self,
                 value: Union[float, int]
                 ) -> None:
        _raise_if_nan_or_inf(value)

        self._value = value

    def serialize_value(self) -> str:
        return "gauge,{}".format(self._value)


class CounterValueDelta(MetricValue):
    def __init__(self,
                 value: Union[float, int]
                 ) -> None:
        _raise_if_nan_or_inf(value)
        self._value = value

    def serialize_value(self) -> str:
        return "count,delta={}".format(self._value)


class SummaryValue(MetricValue):
    def __init__(self,
                 minimum: Union[float, int],
                 maximum: Union[float, int],
                 total: Union[float, int],
                 count: int
                 ) -> None:
        _raise_if_nan_or_inf(minimum)
        _raise_if_nan_or_inf(maximum)
        _raise_if_nan_or_inf(total)

        if count < 0:
            raise metric_error.MetricError("Count must be 0 or above.")

        if minimum > maximum:
            raise metric_error.MetricError("Min cannot be larger than max.")

        self._min = minimum
        self._max = maximum
        self._sum = total
        self._count = count

    def serialize_value(self) -> str:
        return "min={},max={},sum={},count={}".format(self._min, self._max,
                                                      self._sum, self._count)
