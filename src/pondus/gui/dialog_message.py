# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-08  Eike Nicklas <eike@ephys.de>

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

import gtk


class MessageDialog(object):
    """Shows a message. The message type, title and the message to be
    displayed can be passed when initializing the class."""

    def __init__(self, type, title, message):
        if type == 'error':
            self.dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, \
                                            buttons=gtk.BUTTONS_CLOSE)
        elif type == 'info':
            self.dialog = gtk.MessageDialog(type=gtk.MESSAGE_INFO, \
                                            buttons=gtk.BUTTONS_CLOSE)
        elif type == 'question':
            self.dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, \
                                            buttons=gtk.BUTTONS_YES_NO)
        self.dialog.set_title(title)
        self.dialog.set_markup(message)
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        self.dialog.hide()
        return response
