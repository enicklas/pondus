# News

## 2021-12-29: Version 0.9.0
- **Migrated to Python 3 and GTK 3**
- Moved repository from bitbucket to https://github.com/enicklas/pondus
- Converted asciidoc documentation to markdown
- Updated documentation
- Added experimental setup with poetry

## 2021-12-26: Version 0.8.1

- Allow selection and deletion of multiple datasets
- Unify Im-/Export dialogs using different data formats
- Prepare for migration to Python 3
- Add Catalan translation (Thanks dmanye)
- Updated translations: ru

## 2011-06-09: Version 0.8.0

- **Bump minimum required version of python to 2.5**
- Add options to track bodyfat, muscle and water percentage (can be
  activated in preferences)
- Add option to add notes to datasets (can be activated in
  preferences)
- Plot bodyfat, muscle or water using second y-axis in graph
- Set default plot range to “Last Year” and replace “Last 3 months”
  with “Last 6 months”
- Display bodyfat, muscle, water and notes as tooltips in main window
- Add Finnish translation (Thanks Esa Rautiainen)
- Add Hebrew translation (Thanks Yaron Shahrabani)
- Add Russian translation (Thanks Alex Slabchenko)
- Add Turkish translation (Thanks Muhammet Kara)
- Updated translations: bg, de, sv

## 2011-01-21: Version 0.7.3

- Make add/edit dialog transient (Thanks niqueco for the initial
  patch)
- Documentation updates: official homepage is now at bitbucket
- Add Bulgarian translation (Thanks Yasen Pramatarov)
- Add Esperanto translation (Thanks Axel Rousseau)
- Updated translations: fr

## 2010-02-14: Version 0.7.2

- Disable threaded import on non-POSIX platforms; did not work on
  windows

## 2010-01-25: Version 0.7.1

- Update date range when in-/excluding the plan in the plot if
  necessary
- Add Swedish translation (Thanks Peter Landgren)
- Updated translations: it

## 2009-12-20: Version 0.7.0

- **Switch to MIT license**:
  <http://www.opensource.org/licenses/mit-license.php>
- **Bump minimum required version of pygtk to 2.12**
- Import matplotlib in a separate thread in the background to reduce
  startup time. Plotting is enabled once the import is completed.
- Add “Last 3 Months” daterange to plot dialog and make it default if
  the weight history goes further back than 3 months and if
  measurements exist in the last 3 months
- When using imperial units, interpret csv-im-/exported data as lbs
- Fix crash when trying to smooth nonexistent data
- Add more tooltips to improve usability
- Minor performance improvements and code cleanup
- Updated translations: de, es, pl

## 2009-07-19: Version 0.6.0

- The weight plot can be smoothed to filter out short-term fluctations
  and to emphasize the general trend of the weight (Thanks Stefano
  Maggiolo for the initial patch)
- Add option to replace the date entry with a calendar widget in the
  add/edit dialog (Thanks Stefano Costa for the initial patch)
- Use a spinbutton for entering the weight in the add/edit dialog
- Fix visibility of edit-/quit-button in toolbar with recent versions
  of pygtk
- Minor usability tweaks to the plot dialog
- Add information about the used format to the xml-file to ease future
  conversions to new formats
- Add Polish translation (Thanks Adam Piotrowicz)
- Updated translations: de, fr

## 2008-12-10: Version 0.5.3

- Fix crash on first startup
- Remove shebang from non-executable files (Thanks Sindre Pedersen
  Bjørdal for the patch)

## 2008-12-07: Version 0.5.2

- Add a file lock to prevent two instances of pondus from editing the
  same file
- Enable editing the selected row with `CTR-e` again
- Quit pondus with `CTR-q`
- Fix xml parsing problems when height element is missing
- Add Italian translation (Thanks Stefano Costa)
- Updated translations: de, es

## 2008-09-05: Version 0.5.1

- Fix crash on first startup

## 2008-09-02: Version 0.5.0

- Allow user to enter his/her height and to plot the body mass index
- Move option to plot the weight plan from the preferences dialog to
  the plot dialog
- Restructure xml scheme: all user data is now saved in a single file
  at `~/.pondus/user_data.xml` and weight is always saved as kg
- Fix sensitivity of plot action when not using weight planner
- Require python-elementtree (only for python &lt; 2.5)
- Add Spanish translation (Thanks Enrique José Hernández Blasco)
- Add Columbian Spanish translation (Thanks Abdón Sánchez)

## 2008-05-16: Version 0.4.1

- Fix crash if matplotlib is not available (Thanks Jorge Maroto)
- Add French translation (Thanks Fabrice Haberer-Proust)

## 2008-04-12: Version 0.4.0

- Add an optional weight planner to define “target weights” for the
  future and an option to plot the plan for comparison with the
  measured weight
- Add CSV Im-/Export dialogs
- Update plot if `Enter` is pressed in one of the date entry fields
- The edit dialog can no longer be opened with `CTR-e` or the toolbar
  button, please use `Enter` or double-click instead

## 2008-03-06: Version 0.3.0

- Add preferences dialog:
  - Option to use `kg` or `lbs` as the weight unit
  - Option to remember window size
- Plot can be saved to a file
- Disable plotting functions if matplotlib is not available to make
  matplotlib only recommended, but not required.
- Require pygtk &gt;= 2.6
- Drop build dependency on gettext

## 2008-02-19: Version 0.2.0

- Internationalization Support: Pondus can now be translated to
  languages other than English; see `po/README` for details on how to
  create a new translation.
- Select and scroll to newly created dataset after add
- Custom date range in plot: User can provide start/end date
- Add German translation

## 2008-02-01: Version 0.1.0

- Pondus now has an icon/logo
- add/edit dialog: pressing `Enter` in one of the entry fields has the
  same effect as clicking `OK`, i.e. adds/edits the dataset
- fix bugs in plot if no datasets are selected
- code cleanup

## 2008-01-26: Version 0.0.6

- plotting weight vs time is enabled
- `+` and `-` can be used to increment/decrement date and weight in
  the add/edit dataset dialog
- `,` can be used instead of `.` as the decimal separator in the
  add/edit dataset dialog
- code cleanup and documentation updates
- a Windows installer is provided
- install manpage and documentation
- requires Python &gt;= 2.4 due to use of generator expressions

## 2008-01-06: Version 0.0.5

- enable command line option parsing
- code cleanup, performance improvements and documentation updates

## 2008-01-02: Version 0.0.4

- add ability to edit datasets
- alternate background color of rows in main window
- add desktop file

## 2007-12-30: Version 0.0.3

- use uimanager for the toolbar to have keybindings and tooltips
- include a manpage
- remove button only active when a dataset is selected

## 2007-12-10: Version 0.0.2

- disable tooltips for now as they require pygtk &gt;= 2.12, which is
  not yet available on every system

## 2007-12-09: Version 0.0.1

- initial release
