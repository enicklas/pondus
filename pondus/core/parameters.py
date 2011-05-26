# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-10  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os

# path of configuration and data files
configfile = os.path.expanduser('~/.config/pondus/pondusrc')
userdatafile = os.path.expanduser('~/.pondus/user_data.xml')
# legacy filepaths
datafile_old = os.path.expanduser('~/.pondus/datasets.xml')
planfile_old = os.path.expanduser('~/.pondus/weight-plan.xml')
# using standard or custom location for datafile?
use_custom_file = False

# user data
user = None

# configuration
config_default = {'window.remember_size': False,
                  'window.width': 180,
                  'window.height': 300,
                  'preferences.unit_system': 'metric',
                  'preferences.use_calendar': False,
                  'preferences.use_bodyfat': False,
                  'preferences.use_muscle': False,
                  'preferences.use_water': False,
                  'preferences.use_note': False,
                  'preferences.use_weight_plan': False}
config = dict(config_default)
have_mpl = False
convert_weight_data_to_kg = False

# tags used in the xml file and dataset objects
keys_required = ('id', 'date', 'weight')
keys_optional = ('bodyfat', 'muscle', 'water', 'note')

# paths to button/logo icons used
plot_button_path = '/usr/share/pondus/plot.png'
logo_path = '/usr/share/icons/hicolor/48x48/apps/pondus.png'
