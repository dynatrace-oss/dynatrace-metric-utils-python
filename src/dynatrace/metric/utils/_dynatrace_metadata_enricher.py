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
from typing import Mapping, Optional, List


class DynatraceMetadataEnricher:
    """
    Reads Dynatrace metadata using the magic file.
    """

    def __init__(self,
                 logger: Optional[logging.Logger] = None
                 ) -> None:
        self.__logger = logger if logger else logging.getLogger(__name__)

    def get_dynatrace_metadata(self) -> Mapping[str, str]:
        """
        Get all available Dynatrace metadata in a dictionary.
        :return: A dictionary containing all read Dynatrace metadata.
        """
        return self._parse_dynatrace_metadata(
            self._get_metadata_file_content()
        )

    def _get_metadata_file_name(self,
                                indirection_filename: str) -> Optional[str]:
        file_name = None
        if not indirection_filename:
            return None

        try:
            with open(indirection_filename, "r") as metadata_indirection_file:
                file_name = metadata_indirection_file.read()

            if not file_name:
                self.__logger.warning("Dynatrace metadata file not specified "
                                      "in indirection file.")

        except OSError:
            self.__logger.warning("Could not read Dynatrace metadata "
                                  "enrichment file. This is normal if no "
                                  "OneAgent is installed.")

        return file_name

    def _get_metadata_file_content(self) -> List[str]:
        try:
            metadata_file_name = self._get_metadata_file_name(
                "dt_metadata_e617c525669e072eebe3d0f08212e8f2.properties"
            )

            if not metadata_file_name:
                return []

            with open(metadata_file_name, "r") as attributes_file:
                return attributes_file.readlines()
        except OSError:
            self.__logger.warning("Could not read Dynatrace metadata file.")

        return []

    def _parse_dynatrace_metadata(self, lines) -> Mapping[str, str]:
        key_value_pairs = {}
        for line in lines:
            self.__logger.debug("Parsing line %s", line.rstrip("\n"))

            # remove leading and trailing whitespace and split at the first '='
            split = line.strip().split("=", 1)

            if len(split) != 2:
                self.__logger.warning("Could not parse line '%s'", line)
                continue

            key, value = split

            # None or empty:
            if not key or not value:
                self.__logger.warning("Could not parse line '%s'", line)
                continue

            key_value_pairs[key] = value

        return key_value_pairs
