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

import os
import sys
import gtk

from pondus import parameters
from pondus.gui.dialog_message import MessageDialog


class FileLock(object):

    def __init__(self):
        """Gets data neccessary to lock the datafile, asks for confirmation
        if the file is already locked and performs the lock if wanted."""
        self.lockfilename = parameters.userdatafile + '.lck'
        self.pid = str(os.getpid())
        self.first_lock()

    def first_lock(self):
        """Locks the datafile, asks for confirmation if the file is already
        locked and performs the lock if wanted."""
        if not self.is_locked():
            self.lock()
            return
        elif not self.own_lock():
            title = _('Datafile locked, continue?')
            message = _('Another instance of pondus seems to be editing the same datafile. Do you really want to continue and loose all the changes from the other instance?')
            response = MessageDialog('question', title, message).run()
            if response == gtk.RESPONSE_YES:
                self.take_over_lock()
                return
            elif response == gtk.RESPONSE_NO:
                sys.exit(1)

    def lock(self):
        """Locks the datafile to prevent editing with a second instance."""
        lockfile = open(self.lockfilename, 'w')
        lockfile.write(self.pid)
        lockfile.close()

    def unlock(self):
        """Unlocks the datafile if the instance owns the lock."""
        if self.own_lock():
            os.remove(self.lockfilename)

    def is_locked(self):
        """Checks, whether the datafile is locked."""
        return os.path.exists(self.lockfilename)

    def own_lock(self):
        """Checks, whether the current instance owns the lock."""
        if self.is_locked():
            lockfile = open(self.lockfilename, 'r')
            lockpid = lockfile.read()
            lockfile.close()
            return self.pid == lockpid

    def take_over_lock(self):
        """Deletes the current lockfile and creates a new one."""
        os.remove(self.lockfilename)
        self.lock()
