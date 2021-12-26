# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from pondus.core import parameters
from pondus.core import util


class PreferencesDialog(object):
    """Displays the preferences dialog."""

    def __init__(self):
        self.newconfig = dict(parameters.config)

        self.dialog = Gtk.Dialog()
        self.dialog.set_title(_('Preferences'))

        # get content area
        content_area = self.dialog.get_content_area()

        height_box = Gtk.VBox()
        height_box.set_border_width(5)
        height_label = Gtk.Label(label=_('User Height:'))
        height_label.set_alignment(xalign=0, yalign=0.5)
        height_box.pack_start(height_label, True, True, 0)
        height_hbox = Gtk.HBox(spacing=3)
        self.m_adj = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=3,
                                    step_incr=1,
                                    page_incr=1)
        self.cm_adj = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=99,
                                    step_incr=1,
                                    page_incr=10)
        self.ft_adj = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=10,
                                    step_incr=1,
                                    page_incr=2)
        self.in_adj = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=11,
                                    step_incr=1,
                                    page_incr=6)
        self.m_text = _('m')
        self.cm_text = _('cm')
        self.ft_text = _('ft')
        self.in_text = _('in')
        self.height_entry1 = Gtk.SpinButton()
        self.height_entry2 = Gtk.SpinButton()
        self.height_entry1.set_numeric(True)
        self.height_entry2.set_numeric(True)
        self.height_entry2.set_digits(1)
        self.height_label1 = Gtk.Label()
        self.height_label2 = Gtk.Label()
        if self.newconfig['preferences.unit_system'] == 'metric':
            self.set_metric(parameters.user.height)
        else:
            self.set_imperial(parameters.user.height)
        height_hbox.pack_start(self.height_entry1, True, True, 0)
        height_hbox.pack_start(self.height_label1, False, True, 0)
        height_hbox.pack_start(self.height_entry2, True, True, 0)
        height_hbox.pack_start(self.height_label2, False, True, 0)
        height_box.pack_start(height_hbox, True, True, 0)
        content_area.pack_start(height_box, True, True, 0)

        unit_box = Gtk.VBox()
        unit_box.set_border_width(5)
        unit_label = Gtk.Label(label=_('Preferred Unit System:'))
        unit_label.set_alignment(xalign=0, yalign=0.5)
        unit_box.pack_start(unit_label, True, True, 0)
        unit_hbox = Gtk.HBox(homogeneous=True)
        self.unit_button = Gtk.RadioButton(label=_('metric'))
        self.unit_button.connect('toggled', self.on_unit_change, 'metric')
        if self.newconfig['preferences.unit_system'] == 'metric':
            self.unit_button.set_active(True)
        unit_hbox.pack_start(self.unit_button, True, True, 0)
        self.unit_button = Gtk.RadioButton(
                            group=self.unit_button, label=_('imperial'))
        self.unit_button.connect('toggled', self.on_unit_change, 'imperial')
        if self.newconfig['preferences.unit_system'] == 'imperial':
            self.unit_button.set_active(True)
        unit_hbox.pack_start(self.unit_button, True, True, 0)
        unit_box.pack_start(unit_hbox, True, True, 0)
        content_area.pack_start(unit_box, True, True, 0)

        self.use_plan_button = Gtk.CheckButton(_('Enable Weight Planner'))
        self.use_plan_button.set_border_width(5)
        self.use_plan_button.set_active(
                        self.newconfig['preferences.use_weight_plan'])
        content_area.pack_start(self.use_plan_button, True, True, 0)

        self.use_bodyfat_button = Gtk.CheckButton(_('Track Bodyfat'))
        self.use_bodyfat_button.set_border_width(5)
        self.use_bodyfat_button.set_active(
                        self.newconfig['preferences.use_bodyfat'])
        content_area.pack_start(self.use_bodyfat_button, True, True, 0)

        self.use_muscle_button = Gtk.CheckButton(_('Track Muscle'))
        self.use_muscle_button.set_border_width(5)
        self.use_muscle_button.set_active(
                        self.newconfig['preferences.use_muscle'])
        content_area.pack_start(self.use_muscle_button, True, True, 0)

        self.use_water_button = Gtk.CheckButton(_('Track Water'))
        self.use_water_button.set_border_width(5)
        self.use_water_button.set_active(
                        self.newconfig['preferences.use_water'])
        content_area.pack_start(self.use_water_button, True, True, 0)

        self.use_note_button = Gtk.CheckButton(_('Append Notes to Datasets'))
        self.use_note_button.set_border_width(5)
        self.use_note_button.set_active(
                        self.newconfig['preferences.use_note'])
        content_area.pack_start(self.use_note_button, True, True, 0)

        self.use_calendar_button = \
                    Gtk.CheckButton(_('Use Calendar in Add Dialog'))
        self.use_calendar_button.set_border_width(5)
        self.use_calendar_button.set_active(
                        self.newconfig['preferences.use_calendar'])
        self.use_calendar_button.set_tooltip_text(_('Use a calendar widget \
instead of a text entry to enter dates in the add/edit dialog'))
        content_area.pack_start(self.use_calendar_button, True, True, 0)

        self.remember_button = Gtk.CheckButton(_('Remember Window Size'))
        self.remember_button.set_border_width(5)
        self.remember_button.set_active(self.newconfig['window.remember_size'])
        content_area.pack_start(self.remember_button, True, True, 0)

        # buttons in action area
        self.dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.dialog.show_all()

    def run(self):
        """Runs the dialog and updates the configuration."""
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            # set new config
            self.newconfig['window.remember_size'] = \
                                    self.remember_button.get_active()
            self.newconfig['preferences.use_weight_plan'] = \
                                    self.use_plan_button.get_active()
            self.newconfig['preferences.use_bodyfat'] = \
                                    self.use_bodyfat_button.get_active()
            self.newconfig['preferences.use_muscle'] = \
                                    self.use_muscle_button.get_active()
            self.newconfig['preferences.use_water'] = \
                                    self.use_water_button.get_active()
            self.newconfig['preferences.use_note'] = \
                                    self.use_note_button.get_active()
            self.newconfig['preferences.use_calendar'] = \
                                    self.use_calendar_button.get_active()
            parameters.config = self.newconfig
            # set new user height
            newheight1 = self.height_entry1.get_value()
            newheight2 = self.height_entry2.get_value()
            if self.newconfig['preferences.unit_system'] == 'metric':
                parameters.user.height = \
                            util.metric_to_height(newheight1, newheight2)
            else:
                parameters.user.height = \
                            util.imperial_to_height(newheight1, newheight2)
        self.dialog.hide()

    # callback functions
    def on_unit_change(self, widget, data):
        """Remembers the selected weight unit to be saved later."""
        if widget.get_active():
            if (data == 'metric'
                and self.newconfig['preferences.unit_system'] == 'imperial'):
                newheight1 = self.height_entry1.get_value()
                newheight2 = self.height_entry2.get_value()
                height_cm = util.imperial_to_height(newheight1, newheight2)
                self.set_metric(height_cm)
            elif (data == 'imperial'
                    and self.newconfig['preferences.unit_system'] == 'metric'):
                newheight1 = self.height_entry1.get_value()
                newheight2 = self.height_entry2.get_value()
                height_cm = util.metric_to_height(newheight1, newheight2)
                self.set_imperial(height_cm)
            self.newconfig['preferences.unit_system'] = data

    # helper methods
    def set_imperial(self, height_cm):
        """Sets the height display to imperial units."""
        feet, inches = util.height_to_imperial(height_cm)
        self.ft_adj.set_value(feet)
        self.in_adj.set_value(inches)
        self.height_entry1.set_adjustment(self.ft_adj)
        self.height_entry2.set_adjustment(self.in_adj)
        self.height_entry1.set_value(self.ft_adj.get_value())
        self.height_entry2.set_value(self.in_adj.get_value())
        self.height_label1.set_text(self.ft_text)
        self.height_label2.set_text(self.in_text)

    def set_metric(self, height_cm):
        """Sets the height display to metric units."""
        meters, cmeters = util.height_to_metric(height_cm)
        self.m_adj.set_value(meters)
        self.cm_adj.set_value(cmeters)
        self.height_entry1.set_adjustment(self.m_adj)
        self.height_entry2.set_adjustment(self.cm_adj)
        self.height_entry1.set_value(self.m_adj.get_value())
        self.height_entry2.set_value(self.cm_adj.get_value())
        self.height_label1.set_text(self.m_text)
        self.height_label2.set_text(self.cm_text)
