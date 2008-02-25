#! /usr/bin/env python
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

import sys

try:
    import gtk
except ImportError, strerror:
    print strerror
    print _('Please make sure this library is installed.')
    sys.exit(1)

from pondus import datasets
from pondus import parameters
from pondus.core import config_parser
from pondus.gui import guiutil
from pondus.gui.dialog_add import AddDataDialog
from pondus.gui.dialog_remove import RemoveDataDialog
from pondus.gui.dialog_plot import PlotDialog
from pondus.gui.dialog_preferences import PreferencesDialog


class MainWindow(object):
    """Implements the main window and defines the functions to start
    the dialogs."""

    def __init__(self):
        # create the window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Pondus')
        self.window.set_default_size(
                            parameters.config['window.width'],
                            parameters.config['window.height'])
        gtk.window_set_default_icon_from_file(parameters.logo_path)

        # build the content
        mainbox = gtk.VBox()
        self.window.add(mainbox)

        # register icons
        guiutil.register_icons()

        # tooltip for plot icon depends on availability of matplotlib
        if parameters.have_mpl:
            plot_tooltip = _('Plot data')
        else:
            plot_tooltip = _('Matplotlib not available!')

        # set up UIManager
        uimanager = gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)
        action_group = gtk.ActionGroup('pondus_actions')
        action_group.add_actions([
            ('add', gtk.STOCK_ADD, None, '<Control>a',
                _('Add more data'), self.add_dialog),
            ('remove', gtk.STOCK_REMOVE, None, '<Control>d',
                _('Delete selected line'), self.remove_dialog),
            ('edit', gtk.STOCK_EDIT, None, '<Control>e',
                _('Edit selected line'), self.edit_dialog),
            ('plot', 'pondus_plot', None, '<Control>p',
                plot_tooltip, self.plot_dialog),
            ('preferences', gtk.STOCK_PREFERENCES, None, None,
                _('Preferences'), self.preferences_dialog)])
        self.removeaction = action_group.get_action('remove')
        self.editaction = action_group.get_action('edit')
        self.plotaction = action_group.get_action('plot')
        uimanager.insert_action_group(action_group, 0)

        ui = """<ui>
        <toolbar name='Toolbar'>
            <toolitem action='add'/>
            <toolitem action='remove'/>
            <toolitem action='edit'/>
            <toolitem action='plot'/>
            <toolitem action='preferences'/>
        </toolbar>
        </ui>"""
        uimanager.add_ui_from_string(ui)

        toolbar = uimanager.get_widget('/Toolbar')
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        for action in action_group.list_actions():
            action.connect_accelerator()
        mainbox.pack_start(toolbar, False, True)

        # add list displaying the datasets
        datawindow = gtk.ScrolledWindow()
        datawindow.set_policy(gtk.POLICY_AUTOMATIC, \
            gtk.POLICY_AUTOMATIC)
        datawindow.set_shadow_type(gtk.SHADOW_IN)
        self.datalist = gtk.ListStore(int, str, str)
        self.add_data()
        self.dataview = gtk.TreeView(self.datalist)
        self.add_column(_('Date'), 1)
        self.add_column(_('Weight'), 2)
        self.datalist.set_sort_func(2, guiutil.sort_function_weight, None)
        self.datalist.set_sort_column_id(1, gtk.SORT_DESCENDING)
        self.dataview.set_rules_hint(True)
        datawindow.add(self.dataview)
        mainbox.pack_start(datawindow)

        # get treeselection and deactivate actions if no selection
        self.treeselection = self.dataview.get_selection()
        self.set_add_edit_actions_active(self.treeselection)
        self.set_plot_action_active()

        # connect the signals
        self.dataview.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.treeselection.connect('changed', self.set_add_edit_actions_active)
        self.dataview.connect('button-press-event', self.button_pressed)
        self.dataview.connect('key-press-event', self.on_key_press)
        self.window.connect('destroy', self.destroy)

        # display window with content
        self.window.show_all()


    # callback functions

    def destroy(self, widget, data=None):
        """Quits the application cleanly and saves the data to the
        appropriate file."""
        datasets.all_datasets.write_to_file()
        if parameters.config['window.remember_size']:
            parameters.config['window.width'] = \
                                    self.window.get_allocation().width
            parameters.config['window.height'] = \
                                    self.window.get_allocation().height
        config_parser.write_config(parameters.config, parameters.configfile)
        gtk.main_quit()

    def add_dialog(self, widget):
        """Runs the dialog to add a new dataset and then adds it to
        all_datasets and datalist."""
        dialog = AddDataDialog(datasets.all_datasets.get_new_dataset())
        newdata = dialog.run()
        if newdata is not None:
            datasets.all_datasets.add(newdata)
            newiter = self.datalist.append(newdata.as_list())
            self.treeselection.select_iter(newiter)
            listmodel = self.dataview.get_model()
            path = listmodel.get_path(newiter)
            self.dataview.scroll_to_cell(path)
            self.set_plot_action_active()

    def remove_dialog(self, widget):
        """Runs the dialog to remove the selected dataset and then
        deletes it from all_datasets and datalist."""
        dialog = RemoveDataDialog()
        if dialog.run() == gtk.RESPONSE_YES:
            (listmodel, treeiter) = self.treeselection.get_selected()
            id_selected = listmodel.get_value(treeiter, 0)
            # remove selected dataset from all_datasets
            datasets.all_datasets.remove(id_selected)
            # remove selected dataset from displayed list
            listmodel.remove(treeiter)
            # select next row if it exists (treeiter was advanced by
            # listmodel.remove(treeiter))
            if self.datalist.iter_is_valid(treeiter):
                self.treeselection.select_iter(treeiter)
            else:
                lastpath = len(self.datalist)-1
                if lastpath >= 0:
                    self.treeselection.select_path(len(self.datalist)-1)
                else:
                    self.set_add_edit_actions_active(self.treeselection)
                    self.set_plot_action_active()

    def edit_dialog(self, widget):
        """Runs the dialog to edit the selected dataset and then adds it
        to all_datasets and datalist."""
        (listmodel, treeiter) = self.treeselection.get_selected()
        id_selected = listmodel.get_value(treeiter, 0)
        dialog = AddDataDialog(datasets.all_datasets.get(id_selected), \
                                edit=True)
        newdata = dialog.run()
        if newdata is not None:
            datasets.all_datasets.add(newdata)
            self.datalist.set(treeiter,
                1, str(newdata.data['date']),
                2, str(newdata.data['weight']))

    def plot_dialog(self, widget):
        """Runs the plotting dialog."""
        PlotDialog().run()

    def preferences_dialog(self, widget):
        """Runs the preferences dialog."""
        PreferencesDialog().run()

    def on_key_press(self, widget, event):
        """Tests, which key was pressed and triggers the appropriate
        callback function."""
        # delete selected dataset
        if event.keyval == gtk.keysyms.Delete and \
                    self.removeaction.get_sensitive() == True:
            self.remove_dialog(widget)
        # edit selected dataset
        if event.keyval == gtk.keysyms.Return and \
                    self.removeaction.get_sensitive() == True:
            self.edit_dialog(widget)

    def button_pressed(self, widget, event):
        """Tests, which mouse button was pressed and triggers the
        appropriate callback function."""
        # double-click on dataset opens edit dialog
        if event.type == 5:
            self.edit_dialog(widget)


    # other functions

    def set_add_edit_actions_active(self, widget):
        """Tests, whether a dataset is selected and sets sensitivity of
        actions accordingly."""
        if widget.get_selected()[1] == None:
            self.removeaction.set_sensitive(False)
            self.editaction.set_sensitive(False)
        elif self.removeaction.get_sensitive() == False:
            self.removeaction.set_sensitive(True)
            self.editaction.set_sensitive(True)

    def set_plot_action_active(self):
        """Tests, whether a dataset exists and matplotlib is available
        and sets sensitivity of the plot action accordingly."""
        if len(datasets.all_datasets) == 0 or not parameters.have_mpl:
            self.plotaction.set_sensitive(False)
        elif self.plotaction.get_sensitive() == False and parameters.have_mpl:
            self.plotaction.set_sensitive(True)

    def add_column(self, title, columnId):
        """Adds a column to the list view: First, create the
        gtk.TreeViewColumn and then set some needed properties."""
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), \
            text=columnId)
        column.set_sort_column_id(columnId)
        self.dataview.append_column(column)

    def add_data(self):
        """Reads the xml file with the data and appends the data to the
        list model."""
        for dataset in datasets.all_datasets:
            self.datalist.append(dataset.as_list())


    # main function
    def main(self):
        gtk.main()
