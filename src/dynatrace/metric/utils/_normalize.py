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
import re
from typing import Mapping, Optional


class Normalize:
    # Metric keys (mk)
    # characters not valid to start the first identifier key section
    __re_mk_first_identifier_section_start = (re.compile(r"^[^a-zA-Z_]+"))

    # characters not valid to start subsequent identifier key sections
    __re_mk_identifier_section_start = re.compile(r"^[^a-zA-Z0-9_]+")

    # for the rest of the metric key characters, alphanumeric characters as
    # well as hyphens and underscores are allowed.
    __re_mk_invalid_characters = re.compile(r"[^a-zA-Z0-9_\-]+")

    __mk_max_length = 250

    # Dimension keys (dk)
    # dimension keys have to start with a lowercase letter or an underscore.
    __re_dk_start = re.compile(r"^[^a-z_]+")

    # other valid characters in dimension keys are lowercase letters, numbers,
    # colons, underscores and hyphens.
    __re_dk_invalid_chars = re.compile(r"[^a-z0-9_\-:]+")

    __dk_max_length = 100

    # Dimension values (dv)
    # regex for control characters.
    __re_dv_cc = re.compile(r"\p{C}+")

    # characters to be escaped in the dimension value
    __re_dv_characters_to_escape = re.compile(r"([= ,\\\"])")

    __dv_max_length = 250

    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def normalize_metric_key(self, metric_key: str) -> Optional[str]:
        self.__logger.debug("normalizing metric key %s", metric_key)
        # TODO:
        if not metric_key.strip():
            return None

        # trim if too long
        metric_key = metric_key[:self.__mk_max_length]

        first, *rest = metric_key.split(".")
        if not str(first).strip():
            return None

        first = self.__re_mk_invalid_characters.sub(
            self.__re_mk_first_identifier_section_start.sub(
                first, "_"
            ), "_"
        )

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
            else:
                self.__logger.debug("Key is empty, dropping %s=%s", key, value)

        return return_dict
