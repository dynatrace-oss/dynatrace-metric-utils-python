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
from typing import Optional, Mapping, List

from ._dynatrace_metadata_enricher import DynatraceMetadataEnricher
from ._normalize import Normalize
from ._metric import Metric
from .metric_error import MetricError


class DynatraceMetricsSerializer:
    """
    The DynatraceMetricsSerializer transforms :class:`Metric` objects into
    strings, while also enriching them with application- or Dynatrace-
    specific metadata.
    """
    METRIC_LINE_MAX_LENGTH = 50_000

    def __init__(self,
                 logger: Optional[logging.Logger] = None,
                 metric_key_prefix: Optional[str] = None,
                 default_dimensions: Optional[Mapping[str, str]] = None,
                 enrich_with_dynatrace_metadata: bool = True,
                 metrics_source: Optional[str] = None,
                 ):

        self.__logger = logger if logger else logging.getLogger(__name__)

        if enrich_with_dynatrace_metadata:
            # create an enricher and get the Dynatrace metadata dimensions
            # this enricher uses a child logger of the serializer logger.
            enricher = DynatraceMetadataEnricher(
                self.__logger.getChild(DynatraceMetadataEnricher.__name__))
            static_dimensions = enricher.get_dynatrace_metadata()
        else:
            static_dimensions = {}

        # create an instance of the normalizer class with a child logger
        self.__normalize = Normalize(
            self.__logger.getChild(Normalize.__name__)
        )

        # String is not None and non-empty.
        if metrics_source:
            static_dimensions['dt.metrics.source'] = metrics_source

        # None or empty string
        if not metric_key_prefix:
            self.__metric_key_prefix = None
        else:
            self.__metric_key_prefix = metric_key_prefix

        # None or empty dict
        if not default_dimensions:
            self.__default_dimensions = {}
        else:
            self.__default_dimensions = self.__normalize.normalize_dimensions(
                default_dimensions)

        if not static_dimensions:
            self.__static_dimensions = {}
        else:
            self.__static_dimensions = self.__normalize.normalize_dimensions(
                static_dimensions)

    def serialize(self, metric: Metric) -> str:
        """
        Serialize the metric object and create a valid metric line that can
        be ingested with the Dynatrace metrics API
        :param metric: The metric to be serialized.
        :return: The string representation of the metric.
        """
        self.__logger.debug("serializing %s", metric.get_metric_name())
        builder = []

        metric_name = metric.get_metric_name()
        if self.__metric_key_prefix:
            metric_name = "{}.{}".format(self.__metric_key_prefix, metric_name)

        metric_key = self.__normalize.normalize_metric_key(metric_name)

        if not metric_key:
            raise MetricError("Metric name is empty")

        builder.append(metric_key)

        merged_dimensions = self.__merge_dimensions([
            self.__default_dimensions,
            self.__normalize.normalize_dimensions(metric.get_dimensions()),
            self.__static_dimensions
        ])

        if merged_dimensions:
            builder.append(",")
            builder.append(self.__serialize_dimensions(merged_dimensions))

        builder.append(" ")
        builder.append(metric.get_value().serialize_value())

        timestamp = metric.get_timestamp()
        if timestamp:
            builder.append(" {}".format(timestamp))

        metric_str = "".join(builder)

        if len(metric_str) > DynatraceMetricsSerializer.METRIC_LINE_MAX_LENGTH:
            raise MetricError(
                "Metric line exceeds maximum length of {} characters."
                " Metric name: {}".format(
                    DynatraceMetricsSerializer.METRIC_LINE_MAX_LENGTH,
                    metric_key))

        return metric_str

    @staticmethod
    def __merge_dimensions(
        dimension_maps: List[Mapping[str, str]]
    ) -> Mapping[str, str]:
        """
        Merge multiple dicts of dimensions. Only normalized dimensions should
        be passed to this method. Dimensions in dictionaries passed further
        left in the list will overwrite dimensions in dictionaries passed
        further right, if they share the same key.

        :param dimension_maps: A list of dimension dictionaries.
        :return: A dictionary that contains all dimensions from the passed
        dictionaries.
        """
        combined = {}
        for dimension_map in dimension_maps:
            for k, v in dimension_map.items():
                combined[k] = v

        return combined

    def __serialize_dimensions(self,
                               dimensions: Mapping[str, str]
                               ) -> str:
        """
        Combine a dimension list into a string of key=value pairs, separated
        by a comma.
        :param dimensions: the dimensions map to serialize
        :return: A string representing the dimensions.
        """
        builder = []
        for k, v in dimensions.items():
            builder.append("{}={}".format(
                k,
                self.__normalize.escape_dimension_value(v)
            ))

        return ",".join(builder)
