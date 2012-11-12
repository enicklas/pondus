# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-12  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import pygtk
pygtk.require('2.0')

import gtk
from gtk import gdk
import os
import threading

from pondus.core import parameters
from pondus.core import initialize
from pondus.core.logger import logger
from pondus.gui import guiutil
from pondus.gui.dialog_add import AddDataDialog
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_preferences import PreferencesDialog
from pondus.gui.dialog_imexport import DialogExport, DialogImport

PlotDialog = None


class MainWindow(object):
    """Implements the main window and defines the functions to start
    the dialogs."""

    def __init__(self):
        # display weight measurements by default
        self.datasetdata = parameters.user.measurements

        # create the window
        self.window = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
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

        # set up UIManager
        uimanager = gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)
        action_group = gtk.ActionGroup('pondus_actions')
        action_group.add_actions([
            ('add', gtk.STOCK_ADD, None, '<Control>a',
                _('Add dataset'), self.add_dialog),
            ('edit', gtk.STOCK_EDIT, None, '<Control>e',
                _('Edit selected dataset'), self.edit_dialog),
            ('remove', gtk.STOCK_REMOVE, None, '<Control>d',
                _('Delete selected dataset'), self.remove_dialog),
            ('plot', 'pondus_plot', _('Plot'), '<Control>p',
                _('Matplotlib not available!'), self.plot_dialog),
            ('preferences', gtk.STOCK_PREFERENCES, None, None,
                _('Preferences'), self.preferences_dialog),
            ('quit', gtk.STOCK_QUIT, None, '<Control>q',
                _('Quit'), self.destroy)])
        self.editaction = action_group.get_action('edit')
        self.removeaction = action_group.get_action('remove')
        self.plotaction = action_group.get_action('plot')
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

        prefbutton = gtk.MenuToolButton(stock_id=gtk.STOCK_PREFERENCES)
        prefbutton.set_related_action(action_group.get_action('preferences'))
        prefmenu = gtk.Menu()
        import_item = gtk.MenuItem(label=_('Import Data'))
        export_item = gtk.MenuItem(label=_('Export Data'))
        import_item.show()
        export_item.show()
        prefmenu.append(import_item)
        prefmenu.append(export_item)
        prefbutton.set_menu(prefmenu)

        toolbar = uimanager.get_widget('/Toolbar')
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.insert(prefbutton, -1)
        for action in action_group.list_actions():
            action.connect_accelerator()
        mainbox.pack_start(toolbar, False, True, 0)

        # hide quit action
        action_group.get_action('quit').set_visible(False)
        self.editaction.set_visible(False)
        uimanager.get_widget('/Toolbar/edit').set_no_show_all(True)
        uimanager.get_widget('/Toolbar/quit').set_no_show_all(True)

        self.plotbutton = uimanager.get_widget('/Toolbar/plot')

        # add list displaying the datasets
        self.contentbox = gtk.VBox(spacing=5)
        datawindow = gtk.ScrolledWindow()
        datawindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        datawindow.set_shadow_type(gtk.SHADOW_IN)
        self.datalist = gtk.ListStore(int, str, str, str)
        self.display_data(self.datasetdata)
        self.dataview = gtk.TreeView(model=self.datalist)
        self.add_column(_('Date'), 1)
        self.add_column(_('Weight'), 2)
        self.datalist.set_sort_func(2, guiutil.sort_function_weight, None)
        self.datalist.set_sort_column_id(1, gtk.SORT_DESCENDING)
        self.dataview.set_rules_hint(True)
        self.dataview.set_rubber_banding(True)
        self.dataview.set_tooltip_column(3)
        datawindow.add(self.dataview)
        self.contentbox.pack_start(datawindow, True, True, 0)

        # measurement or plan selector
        self.modeselector = gtk.combo_box_new_text()
        self.modeselector.append_text(_('Weight Measurements'))
        self.modeselector.append_text(_('Weight Planner'))
        self.modeselector.set_active(0)
        mainbox.pack_start(self.contentbox, True, True, 0)

        # get treeselection and deactivate actions if no selection
        self.treeselection = self.dataview.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
        self.set_selection_active(self.treeselection)
        self.set_plot_action_active()
        self.check_modeselector()

        # connect the signals
        import_item.connect('activate', self.dialog_import)
        export_item.connect('activate', self.dialog_export)
        self.dataview.add_events(gdk.BUTTON_PRESS_MASK)
        self.treeselection.connect('changed', self.set_selection_active)
        self.dataview.connect('button-press-event', self.button_pressed)
        self.dataview.connect('key-press-event', self.on_key_press)
        self.modeselector.connect('changed', self.update_mode)
        self.window.connect('destroy', self.destroy)

        # display window with content
        self.window.show_all()

    # callback functions
    def destroy(self, widget, data=None):
        """Quits the application cleanly."""
        if parameters.config['window.remember_size']:
            parameters.config['window.width'] = \
                                    self.window.get_allocation().width
            parameters.config['window.height'] = \
                                    self.window.get_allocation().height
        initialize.shutdown()
        gtk.main_quit()

    def add_dialog(self, widget, data=None):
        """Runs the dialog to add a new dataset and then adds it to
        self.datasetdata and self.datalist."""
        dialog = AddDataDialog(self.window,
                            self.datasetdata.get_new_dataset(), edit=False)
        newdata = dialog.run()
        if newdata is not None:
            self.datasetdata.add(newdata)
            newiter = self.append_dataset(newdata)
            self.treeselection.unselect_all()
            self.treeselection.select_iter(newiter)
            listmodel = self.dataview.get_model()
            path = listmodel.get_path(newiter)
            self.dataview.scroll_to_cell(path)
            self.set_plot_action_active()

    def remove_dialog(self, widget, data=None):
        """Runs the dialog to remove the selected dataset and then
        deletes it from self.datasetdata and self.datalist."""
        title = _('Remove Data?')
        message = _('Do you really want to delete the selected datasets?')
        dialog = MessageDialog('question', title, message)
        if dialog.run() == gtk.RESPONSE_YES:
            (listmodel, treepaths) = self.treeselection.get_selected_rows()
            treeiters = [listmodel.get_iter(path) for path in treepaths]
            for treeiter in treeiters:
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
                lastpath = len(self.datalist) - 1
                if lastpath >= 0:
                    self.treeselection.select_path(len(self.datalist) - 1)
                else:
                    self.set_selection_active(self.treeselection)
                    self.set_plot_action_active()

    def edit_dialog(self, widget, data=None):
        """Runs the dialog to edit the selected dataset and then adds it
        to self.datasetdata and self.datalist."""
        (listmodel, treepaths) = self.treeselection.get_selected_rows()
        treeiter = listmodel.get_iter(treepaths[0])
        id_selected = listmodel.get_value(treeiter, 0)
        dialog = AddDataDialog(self.window,
                            self.datasetdata.get(id_selected), edit=True)
        newdata = dialog.run()
        if newdata is not None:
            self.datasetdata.add(newdata)
            if parameters.config['preferences.unit_system'] == 'imperial':
                new_weight = newdata.weight_lbs
            else:
                new_weight = round(newdata.weight, 1)
            self.datalist.set(treeiter,
                1, str(newdata.date),
                2, str(new_weight),
                3, guiutil.get_tooltip(newdata))

    def plot_dialog(self, widget, data=None):
        """Runs the plotting dialog."""
        PlotDialog().run()

    def preferences_dialog(self, widget, data=None):
        """Runs the preferences dialog."""
        PreferencesDialog().run()
        self.set_plot_action_active()
        self.check_modeselector()
        self.display_data(self.datasetdata)

    def dialog_import(self, widget, data=None):
        """Runs the import dialog and updates the display to show
        the imported data."""
        DialogImport().run()
        self.display_data(self.datasetdata)
        self.set_plot_action_active()

    def dialog_export(self, widget, data=None):
        """Runs the export dialog."""
        DialogExport().run()

    def on_key_press(self, widget, event):
        """Tests, which key was pressed and triggers the appropriate
        callback function."""
        # delete selected dataset
        if (event.keyval == gtk.keysyms.Delete
                and self.removeaction.get_sensitive()):
            self.remove_dialog(widget)
        # edit selected dataset
        if (event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter]
                    and self.editaction.get_sensitive()):
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
            self.datasetdata = parameters.user.measurements
        elif key == 1:
            self.datasetdata = parameters.user.plan
        self.display_data(self.datasetdata)
        self.set_selection_active(self.treeselection)
        self.set_plot_action_active()

    def set_selection_active(self, widget):
        """Tests, whether a dataset is selected and sets sensitivity of
        actions accordingly. A selection of multiple datasets can be deleted,
        but not edited."""
        number_rows_selected = widget.count_selected_rows()
        if number_rows_selected == 0:
            self.removeaction.set_sensitive(False)
            self.editaction.set_sensitive(False)
        elif number_rows_selected == 1:
            self.editaction.set_sensitive(True)
            self.removeaction.set_sensitive(True)
        elif number_rows_selected > 1:
            self.editaction.set_sensitive(False)
            self.removeaction.set_sensitive(True)

    # helper methods
    def set_plot_action_active(self):
        """Tests, whether a dataset exists and matplotlib is available
        and sets sensitivity of the plot action accordingly."""
        if ((not parameters.user.measurements and
                    (not parameters.user.plan
                    or not parameters.config['preferences.use_weight_plan']))
                    or not parameters.have_mpl):
            self.plotaction.set_sensitive(False)
        elif not self.plotaction.get_sensitive() and parameters.have_mpl:
            self.plotaction.set_sensitive(True)

    def check_modeselector(self):
        """Checks, whether the modeselector should be displayed and
        hides or shows it accordingly."""
        if (parameters.config['preferences.use_weight_plan']
            and self.modeselector not in self.contentbox.get_children()):
            self.contentbox.pack_end(self.modeselector, False, True, 0)
        elif (not parameters.config['preferences.use_weight_plan']
            and self.modeselector in self.contentbox.get_children()):
            self.modeselector.set_active(0)
            self.contentbox.remove(self.modeselector)
        self.contentbox.show_all()

    def add_column(self, title, column_id):
        """Adds a column to the list view: First, create the
        gtk.TreeViewColumn and then set some needed properties."""
        column = gtk.TreeViewColumn(
                            title, gtk.CellRendererText(), text=column_id)
        column.set_sort_column_id(column_id)
        self.dataview.append_column(column)

    def display_data(self, datasetdata):
        """Appends all datasets to the list model."""
        self.datalist.clear()
        for dataset in datasetdata:
            self.append_dataset(dataset)

    def append_dataset(self, dataset):
        """Appends a dataset to the list model."""
        if parameters.config['preferences.unit_system'] == 'imperial':
            weight = dataset.weight_lbs
        else:
            weight = round(dataset.weight, 1)
        dataset_list = [dataset.id, str(dataset.date), str(weight), \
                guiutil.get_tooltip(dataset)]
        return self.datalist.append(dataset_list)

    # main function
    def main(self):
        """Starts the gtk main loop."""
        if os.name == 'posix':
            gdk.threads_init()
            MplTester().start()
        else:
            import_mpl()
        gtk.main()


class MplTester(threading.Thread):
    """Tests availability of matplotlib in a separate thread."""

    def __init__(self):
        """Initializes the thread."""
        threading.Thread.__init__(self)

    def run(self):
        """Tries to import matplotlib and enable plotting."""
        import_mpl()


def import_mpl():
    """Tests availability of matplotlib and enables plotting, if possible."""
    try:
        from matplotlib import dates
    except ImportError:
        logger.warning( \
            _('python-matplotlib is not installed, plotting disabled!'))
    else:
        parameters.have_mpl = True
        # speed up opening of plot dialog by importing it here
        global PlotDialog
        if PlotDialog is None:
            from pondus.gui.dialog_plot import PlotDialog
        # enable plot action in main window
        mainwindow.set_plot_action_active()
        # set correct tooltip on plotbutton
        mainwindow.plotbutton.set_tooltip_text(_('Plot weight data'))

mainwindow = MainWindow()
