# Installation Instructions

Pondus is developed and tested on Debian GNU/Linux, but should run on
every system where Python 3 and GTK 3 are available.

## Software Requirements

System dependencies are Python and GTK 3. In particular, you need to `apt install gir1.2-gtk-3.0` on Debian-like systems and correspondingly on other systems.

Required Python packages can be installed with
`apt install python3-gi python3-matplotlib python3-gi-cairo`

## Testing without installation

You can test Pondus without installing it by executing `pondus.py`.

## Installation Instructions

### Linux/Unix:

Install Pondus by executing in the source directory
(as root):

    python setup.py install

The development package for python (python3-dev or similar) is needed
for this, so please install it first.

Then, you can start Pondus from the command line (remember to switch back to
the normal user) with:

    pondus

or from the menu of your desktop environment.

### Windows:

A Windows installer can be found at <https://github.com/enicklas/pondus/>

However, before installing Pondus, you have to make sure that Python and
GTK are installed. The installation directions for GTK can be found at
<https://www.gtk.org/docs/installations/windows>

Then, Pondus can be installed by executing the provided installer.

The executable script to start Pondus should now be in

    C:\Python<version>\Scripts\pondus-win.py

## Development setup
 
In order to build Pondus distrubition packages, you need to

`apt install build-essential
libgirepository1.0-dev python3-dev libcairo2-dev`

