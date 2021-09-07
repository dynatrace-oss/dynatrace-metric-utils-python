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


def _format_number(value: Union[int, float]):
    if abs(value) > 1e15:
        as_string = "{:.8e}".format(value)
    elif 0 < abs(value) < 1e-15:
        as_string = "{:.8e}".format(value)
    else:
        as_string = str(value)

    if "0e" in as_string:
        # remove trailing zeroes in exponential notation
        start, end = as_string.split("e")
        start = str(start).rstrip("0")
        if start.endswith("."):
            start = start + "0"
        return start + "e" + end

    if as_string.endswith(".0"):
        no_trailing_zero = as_string[0:len(as_string) - 2]
        if no_trailing_zero == "-0":
            return "0"
        return no_trailing_zero

    return as_string


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
        return "gauge,{}".format(_format_number(self._value))


class CounterValueDelta(MetricValue):
    def __init__(self,
                 value: Union[float, int]
                 ) -> None:
        _raise_if_nan_or_inf(value)
        self._value = value

    def serialize_value(self) -> str:
        return "count,delta={}".format(_format_number(self._value))


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
        return "gauge,min={},max={},sum={},count={}".format(
            _format_number(self._min),
            _format_number(self._max),
            _format_number(self._sum),
            self._count
        )
