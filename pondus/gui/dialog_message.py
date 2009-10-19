# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-09  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gtk


class MessageDialog(object):
    """Shows a message. The message type, title and the message to be
    displayed can be passed when initializing the class."""

    def __init__(self, type_, title, message):
        if type_ == 'error':
            self.dialog = gtk.MessageDialog(
                    type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
        elif type_ == 'info':
            self.dialog = gtk.MessageDialog(
                    type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE)
        elif type_ == 'question':
            self.dialog = gtk.MessageDialog(
                    type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
        self.dialog.set_title(title)
        self.dialog.set_markup(message)
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        self.dialog.hide()
        return response
