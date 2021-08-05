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
from typing import Optional, Mapping, List
import logging
import _normalize
import _enrichment
import metrics

VERSION = "0.0.1a0"


class DynatraceMetricsSerializer:
    def __init__(self,
                 metric_key_prefix: Optional[str] = None,
                 default_dimensions: Optional[Mapping[str, str]] = None,
                 enrich_with_dynatrace_metadata: bool = True,
                 metrics_source: Optional[str] = None,
                 logger: Optional[logging.Logger] = None
                 ):

        self.__logger = logger if logger else logging.getLogger(__name__)

        if enrich_with_dynatrace_metadata:
            # create an enricher and get the Dynatrace metadata dimensions
            # this enricher uses a child logger of the serializer logger.
            enricher = _enrichment.DynatraceMetadataEnricher(
                self.__logger.getChild(
                    _enrichment.DynatraceMetadataEnricher.__name__))
            static_dimensions = enricher.get_dynatrace_metadata()
        else:
            static_dimensions = {}

        # create an instance of the normalizer class with a child logger
        self.__normalize = _normalize.Normalize(
            self.__logger.getChild(_normalize.Normalize.__name__)
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

    def serialize(self, metric: metrics.Metric) -> str:
        # todo sanity checks
        self.__logger.debug("serializing %s", metric.get_metric_name())
        builder = []

        metric_name = metric.get_metric_name()
        if self.__metric_key_prefix:
            metric_name = "{}.{}".format(self.__metric_key_prefix, metric_name)

        # todo break if the name is empty

        builder.append(self.__normalize.normalize_metric_key(metric_name))

        metric_dimensions = self.__normalize.normalize_dimensions(
            metric.get_dimensions())

        merged_dimensions = self.__merge_dimensions([
            self.__default_dimensions,
            metric_dimensions,
            self.__static_dimensions
        ])

        if merged_dimensions:
            builder.append(self.__serialize_dimensions(merged_dimensions))

        builder.append(" ")

        builder.append(metric.get_value().serialize_value())

        if metric.get_timestamp():
            builder.append(" ")
            builder.append(metric.get_timestamp())

        return "".join(builder)

    @staticmethod
    def __merge_dimensions(
        dimension_maps: List[Mapping[str, str]]
    ) -> Mapping[str, str]:
        combined = {}
        for dimension_map in dimension_maps:
            for k, v in dimension_map.items():
                combined[k] = v

        return combined

    @staticmethod
    def __serialize_dimensions(dimensions: Mapping[str, str]) -> str:
        builder = []
        for k, v in dimensions.items():
            builder.append("{}={}".format(k, v))

        return ",".join(builder)
