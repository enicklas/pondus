#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008  Eike Nicklas <eike@ephys.de>

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

config_default = {'window.remember_size': False,
                  'window.width': 180,
                  'window.height': 300,
                  'preferences.weight_unit': 'kg',
                  'preferences.plot_weight_plan': True}

def read_config(conffile):
    """Reads the configuration file and returns the config dictionary."""
    config = config_default
    if os.path.exists(conffile):
        conf = ConfigParser.SafeConfigParser()
        conf.read(conffile)
        if conf.getboolean('window', 'remember_size'):
            config['window.width'] = conf.getint('window', 'width')
            config['window.height'] = conf.getint('window', 'height')
            config['window.remember_size'] = \
                            conf.getboolean('window', 'remember_size')
        config['preferences.weight_unit'] = \
                            conf.get('preferences', 'weight_unit')
        try:
            config['preferences.plot_weight_plan'] = \
                            conf.getboolean('preferences', 'plot_weight_plan')
        except ConfigParser.NoOptionError:
            pass
    return config

def write_config(config, conffile):
    """Writes the config dictionary to the configuration file."""
    conf = ConfigParser.SafeConfigParser()
    for key in config.keys():
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
