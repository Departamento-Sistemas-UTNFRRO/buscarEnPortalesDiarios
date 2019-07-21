# -*- coding: utf-8 -*-

#    This file is part of escucharTweets.
#
#    escucharTweets is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    escucharTweets is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with escucharTweets; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
import json
import os
from datetime import datetime
logger = logging.getLogger(__name__)


class ConfigManager(object):
    def __init__(self):
        self.base_path = None
        self.input_filename = None
        self.input_init = 0
        self.input_end = None
        self.output_filename = None
        self.loadConfigData()

    def loadConfigData(self):
        logger.info("Loading Config Options")
        with open('config.json', 'r') as config_file:
            filecontents = json.load(config_file)
            self.base_path = filecontents['FileStorageConfig'][0]['base_path']
            input_filename_prefix = filecontents['FileStorageConfig'][0]['input_filename']
            self.input_filename = os.path.join(self.base_path, input_filename_prefix)
            self.input_init = filecontents['FileStorageConfig'][0]['input_init']
            self.input_end = filecontents['FileStorageConfig'][0]['input_end']
            output_filename_prefix = filecontents['FileStorageConfig'][0]['output_filename']
            self.output_filename = os.path.join(self.base_path, output_filename_prefix + "_" + str(self.input_init) + "_" + str(self.input_end) + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")
