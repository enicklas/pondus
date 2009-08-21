# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-09  Eike Nicklas <eike@ephys.de>

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

from pondus import user_data
from pondus import parameters
from pondus.core import config_parser
from pondus.core import util
from pondus.gui import guiutil
from pondus.gui.dialog_add import AddDataDialog
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_preferences import PreferencesDialog
from pondus.gui.dialog_csv_import import CSVDialogImport
from pondus.gui.dialog_csv_export import CSVDialogExport

if parameters.have_mpl:
    from pondus.gui.dialog_plot import PlotDialog

class MainWindow(object):
    """Implements the main window and defines the functions to start
    the dialogs."""

    def __init__(self):
        # display weight measurements by default
        self.datasetdata = user_data.user.measurements

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
            ('edit', gtk.STOCK_EDIT, None, '<Control>e',
                _('Edit selected line'), self.edit_dialog),
            ('remove', gtk.STOCK_REMOVE, None, '<Control>d',
                _('Delete selected line'), self.remove_dialog),
            ('plot', 'pondus_plot', _('Plot'), '<Control>p',
                plot_tooltip, self.plot_dialog),
            ('preferences', gtk.STOCK_PREFERENCES, None, None,
                _('Preferences'), self.preferences_dialog),
            ('quit', gtk.STOCK_QUIT, None, '<Control>q',
                _('Quit'), self.destroy)])
        self.editaction = action_group.get_action('edit')
        self.removeaction = action_group.get_action('remove')
        self.plotaction = action_group.get_action('plot')
        prefaction = action_group.get_action('preferences')
        uimanager.insert_action_group(action_group, 0)

        ui = """
        <ui>
        <toolbar name='Toolbar'>
            <toolitem action='add'/>
            <toolitem action='edit'/>
            <toolitem action='remove'/>
            <toolitem action='plot'/>
            <toolitem action='quit'/>
        </toolbar>
        </ui>"""
        uimanager.add_ui_from_string(ui)

        prefbutton = gtk.MenuToolButton(gtk.STOCK_PREFERENCES)
        prefaction.connect_proxy(prefbutton)
        prefmenu = gtk.Menu()
        csv_import_item = gtk.MenuItem(_('CSV Import'))
        csv_export_item = gtk.MenuItem(_('CSV Export'))
        csv_import_item.show()
        csv_export_item.show()
        prefmenu.append(csv_import_item)
        prefmenu.append(csv_export_item)
        prefbutton.set_menu(prefmenu)

        toolbar = uimanager.get_widget('/Toolbar')
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.insert(prefbutton, -1)
        for action in action_group.list_actions():
            action.connect_accelerator()
        mainbox.pack_start(toolbar, False, True)

        # hide quit action
        action_group.get_action('quit').set_visible(False)
        self.editaction.set_visible(False)
        uimanager.get_widget('/Toolbar/edit').set_no_show_all(True)
        uimanager.get_widget('/Toolbar/quit').set_no_show_all(True)

        # add list displaying the datasets
        self.contentbox = gtk.VBox(spacing=5)
        datawindow = gtk.ScrolledWindow()
        datawindow.set_policy(gtk.POLICY_AUTOMATIC, \
            gtk.POLICY_AUTOMATIC)
        datawindow.set_shadow_type(gtk.SHADOW_IN)
        self.datalist = gtk.ListStore(int, str, str)
        self.display_data(self.datasetdata)
        self.dataview = gtk.TreeView(self.datalist)
        self.add_column(_('Date'), 1)
        self.add_column(_('Weight'), 2)
        self.datalist.set_sort_func(2, guiutil.sort_function_weight, None)
        self.datalist.set_sort_column_id(1, gtk.SORT_DESCENDING)
        self.dataview.set_rules_hint(True)
        datawindow.add(self.dataview)
        self.contentbox.pack_start(datawindow)

        # measurement or plan selector
        self.modeselector = gtk.combo_box_new_text()
        self.modeselector.append_text(_('Weight Measurements'))
        self.modeselector.append_text(_('Weight Planner'))
        self.modeselector.set_active(0)
        mainbox.pack_start(self.contentbox)

        # get treeselection and deactivate actions if no selection
        self.treeselection = self.dataview.get_selection()
        self.set_selection_active(self.treeselection)
        self.set_plot_action_active()
        self.check_modeselector()

        # connect the signals
        csv_import_item.connect('activate', self.csv_dialog_import)
        csv_export_item.connect('activate', self.csv_dialog_export)
        self.dataview.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.treeselection.connect('changed', self.set_selection_active)
        self.dataview.connect('button-press-event', self.button_pressed)
        self.dataview.connect('key-press-event', self.on_key_press)
        self.modeselector.connect('changed', self.update_mode)
        self.window.connect('destroy', self.destroy)

        # display window with content
        self.window.show_all()


    # callback functions

    def destroy(self, widget, data=None):
        """Quits the application cleanly and saves the data to the
        appropriate file."""
        if parameters.filelock.own_lock():
            user_data.user.write_to_file(filepath=parameters.userdatafile)
            if parameters.config['window.remember_size']:
                parameters.config['window.width'] = \
                                        self.window.get_allocation().width
                parameters.config['window.height'] = \
                                        self.window.get_allocation().height
            config_parser.write_config(parameters.config, \
                                        parameters.configfile)
            parameters.filelock.unlock()
        else:
            backupfile = parameters.userdatafile + '.backup'
            user_data.user.write_to_file(filepath=backupfile)
            print _('Not owning the file lock. Backing up the data to'), \
                    '\n', backupfile
        gtk.main_quit()

    def add_dialog(self, widget):
        """Runs the dialog to add a new dataset and then adds it to
        self.datasetdata and self.datalist."""
        dialog = AddDataDialog(self.datasetdata.get_new_dataset(), \
                                edit=False)
        newdata = dialog.run()
        if newdata is not None:
            self.datasetdata.add(newdata)
            newiter = self.append_dataset(newdata)
            self.treeselection.select_iter(newiter)
            listmodel = self.dataview.get_model()
            path = listmodel.get_path(newiter)
            self.dataview.scroll_to_cell(path)
            self.set_plot_action_active()

    def remove_dialog(self, widget):
        """Runs the dialog to remove the selected dataset and then
        deletes it from self.datasetdata and self.datalist."""
        title = _('Remove Data?')
        message = _('Do you really want to delete this dataset?')
        dialog = MessageDialog('question', title, message)
        if dialog.run() == gtk.RESPONSE_YES:
            (listmodel, treeiter) = self.treeselection.get_selected()
            id_selected = listmodel.get_value(treeiter, 0)
            # remove selected dataset from self.datasetdata
            self.datasetdata.remove(id_selected)
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
                    self.set_selection_active(self.treeselection)
                    self.set_plot_action_active()

    def edit_dialog(self, widget):
        """Runs the dialog to edit the selected dataset and then adds it
        to self.datasetdata and self.datalist."""
        (listmodel, treeiter) = self.treeselection.get_selected()
        id_selected = listmodel.get_value(treeiter, 0)
        dialog = AddDataDialog(self.datasetdata.get(id_selected), \
                                edit=True)
        newdata = dialog.run()
        if newdata is not None:
            self.datasetdata.add(newdata)
            new_weight = newdata.get('weight')
            if parameters.config['preferences.unit_system'] == 'imperial':
                new_weight = util.kg_to_lbs(new_weight)
            new_weight = round(new_weight, 1)
            self.datalist.set(treeiter,
                1, str(newdata.get('date')),
                2, str(new_weight))

    def plot_dialog(self, widget):
        """Runs the plotting dialog."""
        PlotDialog().run()

    def preferences_dialog(self, widget):
        """Runs the preferences dialog."""
        PreferencesDialog().run()
        self.set_plot_action_active()
        self.check_modeselector()
        self.display_data(self.datasetdata)

    def csv_dialog_import(self, widget):
        """Runs the csv import dialog and updates the display to show
        the imported data."""
        CSVDialogImport().run()
        self.display_data(self.datasetdata)
        self.set_plot_action_active()

    def csv_dialog_export(self, widget):
        """Runs the csv export dialog."""
        CSVDialogExport().run()

    def on_key_press(self, widget, event):
        """Tests, which key was pressed and triggers the appropriate
        callback function."""
        # delete selected dataset
        if event.keyval == gtk.keysyms.Delete and \
                    self.removeaction.get_sensitive():
            self.remove_dialog(widget)
        # edit selected dataset
        if event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter] \
                    and self.editaction.get_sensitive():
            self.edit_dialog(widget)

    def button_pressed(self, widget, event):
        """Tests, which mouse button was pressed and triggers the
        appropriate callback function."""
        # double-click on dataset opens edit dialog
        if event.type == 5:
            self.edit_dialog(widget)

    def update_mode(self, modeselector):
        """Updates the editing mode: whether weight measurements or
        the weight plan is displayed and edited."""
        key = self.modeselector.get_active()
        if key == 0:
            self.datasetdata = user_data.user.measurements
        elif key == 1:
            self.datasetdata = user_data.user.plan
        self.display_data(self.datasetdata)
        self.set_selection_active(self.treeselection)
        self.set_plot_action_active()

    def set_selection_active(self, widget):
        """Tests, whether a dataset is selected and sets sensitivity of
        actions accordingly."""
        if widget.get_selected()[1] is None:
            self.removeaction.set_sensitive(False)
            self.editaction.set_sensitive(False)
        elif not self.removeaction.get_sensitive():
            self.removeaction.set_sensitive(True)
            self.editaction.set_sensitive(True)


    # helper methods

    def set_plot_action_active(self):
        """Tests, whether a dataset exists and matplotlib is available
        and sets sensitivity of the plot action accordingly."""
        if (not user_data.user.measurements and \
                    (not user_data.user.plan \
                    or not parameters.config['preferences.use_weight_plan'])) \
                    or not parameters.have_mpl:
            self.plotaction.set_sensitive(False)
        elif not self.plotaction.get_sensitive() and parameters.have_mpl:
            self.plotaction.set_sensitive(True)

    def check_modeselector(self):
        """Checks, whether the modeselector should be displayed and
        hides or shows it accordingly."""
        if parameters.config['preferences.use_weight_plan'] \
            and self.modeselector not in self.contentbox.get_children():
            self.contentbox.pack_end(self.modeselector, False, True)
        elif not parameters.config['preferences.use_weight_plan'] \
            and self.modeselector in self.contentbox.get_children():
            self.modeselector.set_active(0)
            self.contentbox.remove(self.modeselector)
        self.contentbox.show_all()

    def add_column(self, title, columnId):
        """Adds a column to the list view: First, create the
        gtk.TreeViewColumn and then set some needed properties."""
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), \
            text=columnId)
        column.set_sort_column_id(columnId)
        self.dataview.append_column(column)

    def display_data(self, datasetdata):
        """Appends all datasets to the list model."""
        self.datalist.clear()
        for dataset in datasetdata:
            self.append_dataset(dataset)

    def append_dataset(self, dataset):
        """Appends a dataset to the list model."""
        dataset_list = dataset.as_list()
        if parameters.config['preferences.unit_system'] == 'imperial':
            dataset_list[2] = util.kg_to_lbs(dataset_list[2])
        dataset_list[2] = round(dataset_list[2], 1)
        return self.datalist.append(dataset_list)


    # main function
    def main(self):
        """Starts the gtk main loop."""
        gtk.main()
