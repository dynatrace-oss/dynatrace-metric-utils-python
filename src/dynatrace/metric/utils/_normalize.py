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

# todo
import logging
from typing import Mapping, Optional


class Normalize:
    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def normalize_metric_key(self, metric_key: str) -> str:
        self.__logger.debug("normalizing metric key %s", metric_key)
        return metric_key

    def normalize_dimension_key(self, key: str) -> str:
        self.__logger.debug("normalizing dimension key %s", key)
        return key

    def normalize_dimension_value(self, value: str) -> str:
        self.__logger.debug("normalizing dimension value %s", value)
        return value

    def normalize_dimensions(self,
                             dimensions: Mapping[str, str]
                             ) -> Mapping[str, str]:
        return_dict = {}
        for key, value in dimensions.items():
            normalized_key = self.normalize_dimension_key(key)
            if normalized_key:
                return_dict[normalized_key] = self.normalize_dimension_value(
                    value)

        return return_dict
