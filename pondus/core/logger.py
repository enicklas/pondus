# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2011  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import logging

console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
console_handler.setFormatter(formatter)

logger = logging.getLogger('pondus')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
