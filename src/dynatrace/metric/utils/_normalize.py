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
import unicodedata
from typing import Mapping, Optional
from .metric_error import MetricError


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
    # in order to delete control characters, all control chars are replaced
    # with the null character (\u0000), and then all consecutive null chars
    # are replaced with one underscore.
    __re_dv_null_characters = re.compile(r"\u0000+")

    # characters to be escaped in the dimension value
    __re_dv_characters_to_escape = re.compile(r"([= ,\\\"])")
    # will match if the string has an odd number of escaped trailing
    # backslashes
    __re_dv_odd_number_of_trailing_slashes = re.compile(r"[^\\](?:\\\\)*\\$")

    __dv_max_length = 250

    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def normalize_metric_key(self, metric_key: str) -> Optional[str]:
        self.__logger.debug("normalizing metric key %s", metric_key)

        if not metric_key:
            return None

        if not isinstance(metric_key, str):
            raise MetricError(
                f"Unexpected metric key type: {type(metric_key)}")

        # trim if too long
        metric_key = metric_key[:self.__mk_max_length]

        first, *rest = metric_key.split(".")
        if not str(first).strip():
            return None

        first = self.__re_mk_invalid_characters.sub(
            "_",
            self.__re_mk_first_identifier_section_start.sub(
                "_",
                first,
            ),
        )

        rest = list(filter(None, map(
            self.__normalize_metric_key_section, rest
        )))

        return ".".join([first, *rest])

    @classmethod
    def __normalize_metric_key_section(cls, section: str) -> str:
        # delete invalid characters at the start of the section key
        section = cls.__re_mk_identifier_section_start.sub("_", section)
        # replace ranges of invalid characters in the key with one underscore.
        section = cls.__re_mk_invalid_characters.sub("_", section)
        return section

    def normalize_dimension_key(self, dimension_key: str) -> Optional[str]:
        self.__logger.debug("normalizing dimension key %s", dimension_key)

        if not dimension_key:
            return None

        if not isinstance(dimension_key, str):
            raise MetricError(
                f"Unexpected dimension key type: {type(dimension_key)}")

        dimension_key = dimension_key[:self.__dk_max_length]

        sections = list(filter(None, map(
            self.__normalize_dimension_key_section,
            dimension_key.split(".")
        )))

        return ".".join(sections)

    @classmethod
    def __normalize_dimension_key_section(cls, section: str):
        # convert to lowercase
        section = section.lower()
        # delete leading invalid characters
        section = cls.__re_dk_start.sub("_", section)
        # replace consecutive invalid characters with one underscore:
        section = cls.__re_dk_invalid_chars.sub("_", section)

        return section

    def normalize_dimension_value(self, dimension_value: str) -> str:
        self.__logger.debug("normalizing dimension value %s", dimension_value)
        if not dimension_value:
            # for dimension values, return an empty string, otherwise "None"
            # will be serialized.
            return ""

        if not isinstance(dimension_value, str):
            raise MetricError(
                f"Unexpected dimension value type: {type(dimension_value)}")
        dimension_value = dimension_value[:self.__dv_max_length]

        return self.__replace_control_characters(dimension_value)

    @classmethod
    def __replace_control_characters(cls, s: str):
        s = "".join(
            c if unicodedata.category(c)[0] != "C" else "\u0000" for c in s
        )
        return cls.__re_dv_null_characters.sub("_", s)

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

    def escape_dimension_value(self,
                               dimension_value: str,
                               ) -> str:
        self.__logger.debug("escaping dimension value: %s", dimension_value)
        escaped = self.__re_dv_characters_to_escape.sub(r"\\\g<1>",
                                                        dimension_value)

        escaped = escaped[:self.__dv_max_length]
        if self.__re_dv_odd_number_of_trailing_slashes.search(escaped):
            escaped = escaped[:len(escaped) - 1]

        return escaped
