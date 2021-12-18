# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-12  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

# workaround to support both python2 and python3
try:
    import configparser
except ImportError:
    import configparser as configparser
import os

from pondus.core import parameters


def read_config(default_config, conffile):
    """Reads the configuration file and returns the updated default_config
    dictionary."""
    config = dict(default_config)
    if os.path.isfile(conffile):
        conf = configparser.RawConfigParser()
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
        # support legacy weight unit configuration
        elif conf.has_option('preferences', 'weight_unit'):
            if conf.get('preferences', 'weight_unit') == 'kg':
                config['preferences.unit_system'] = 'metric'
            elif conf.get('preferences', 'weight_unit') == 'lbs':
                config['preferences.unit_system'] = 'imperial'
                parameters.convert_weight_data_to_kg = True
        for option in ['use_weight_plan', 'use_calendar', 'use_bodyfat',
                        'use_muscle', 'use_water', 'use_note']:
            if conf.has_option('preferences', option):
                config['.'.join(['preferences', option])] = \
                                conf.getboolean('preferences', option)
    return config


def write_config(config, conffile):
    """Writes the config dictionary to the configuration file."""
    conf = configparser.RawConfigParser()
    for key, value in config.items():
        section, option = key.split('.')
        try:
            conf.set(section, option, str(value))
        except configparser.NoSectionError:
            conf.add_section(section)
            conf.set(section, option, str(value))
    if not os.path.exists(os.path.dirname(conffile)):
        os.makedirs(os.path.dirname(conffile))
    config_file = open(conffile, 'w')
    conf.write(config_file)
    config_file.close()
