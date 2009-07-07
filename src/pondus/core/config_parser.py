# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-09  Eike Nicklas <eike@ephys.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import ConfigParser
import os

from pondus import parameters

def read_config(default_config, conffile):
    """Reads the configuration file and returns the updated default_config
    dictionary."""
    config = dict(default_config)
    if os.path.isfile(conffile):
        conf = ConfigParser.RawConfigParser()
        conf.read(conffile)
        if conf.has_option('window', 'remember_size'):
            if conf.getboolean('window', 'remember_size'):
                config['window.remember_size'] = True
                if conf.has_option('window', 'width'):
                    config['window.width'] = conf.getint('window', 'width')
                if conf.has_option('window', 'height'):
                    config['window.height'] = conf.getint('window', 'height')
        if conf.has_option('preferences', 'unit_system'):
            config['preferences.unit_system'] = \
                            conf.get('preferences', 'unit_system')
        elif conf.has_option('preferences', 'weight_unit'):
            if conf.get('preferences', 'weight_unit') == 'kg':
                config['preferences.unit_system'] = 'metric'
            elif conf.get('preferences', 'weight_unit') == 'lbs':
                config['preferences.unit_system'] = 'imperial'
                parameters.convert_weight_data_to_kg = True
        if conf.has_option('preferences', 'use_weight_plan'):
            config['preferences.use_weight_plan'] = \
                            conf.getboolean('preferences', 'use_weight_plan')
        if conf.has_option('preferences', 'use_calendar'):
            config['preferences.use_calendar'] = \
                            conf.getboolean('preferences', 'use_calendar')
    return config

def write_config(config, conffile):
    """Writes the config dictionary to the configuration file."""
    conf = ConfigParser.RawConfigParser()
    for key in config.iterkeys():
        section, option = key.split('.')
        try:
            conf.set(section, option, str(config[key]))
        except ConfigParser.NoSectionError:
            conf.add_section(section)
            conf.set(section, option, str(config[key]))
    if not os.path.exists(os.path.dirname(conffile)):
        os.makedirs(os.path.dirname(conffile))
    config_file = open(conffile, 'w')
    conf.write(config_file)
    config_file.close()
    return None
