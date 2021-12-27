# Installation Instructions

Pondus is developed and tested on Debian GNU/Linux, but should run on
every system where Python 3 and GTK 3 are available.

## Software Requirements

System dependencies are Python and GTK 3. In particular, you need to
`apt install gir1.2-gtk-3.0` on Debian-like systems and correspondingly
on other systems.

Required Python packages can be installed with
`apt install python3-gi python3-matplotlib python3-gi-cairo`

## Testing without installation

Get the source code via `git clone https://github.com/enicklas/pondus.git` or
download and unpack it from `https://github.com/enicklas/pondus`.

Run Pondus without installation it by executing `python run_pondus.py` within
the source directory.

Note: An experimental setup with [poetry](https://python-poetry.org/) is
available as well. After installation of poetry, you can install pondus to
a virtual environment using `poetry install` and then start the application
with `poetry run pondus`. Some features (e.g. internationalization) may not
work with this approach.

## Installation Instructions

### Linux/Unix:

The simplest way is to download the package from
https://github.com/enicklas/pondus/releases and install it with
`pip install <path/to/package>`

Alternatively, you can install Pondus from the source directory via
`python setup.py install --user`. The development dependencies (see below) are
needed for this, so please install them first.

Then, you can run `pondus` from the command line or from the menu of your
desktop environment.

### Windows:

A Windows installer can be found at <https://github.com/enicklas/pondus>

However, before installing Pondus, you have to make sure that Python and
GTK are installed. The installation directions for GTK can be found at
<https://www.gtk.org/docs/installations/windows>

Then, Pondus can be installed by executing the provided installer.

The executable script to start Pondus should now be in

    C:\Python<version>\Scripts\pondus-win.py

## Development setup
 
In order to build Pondus distribution packages, you need to

`apt install build-essential libgirepository1.0-dev python3-dev libcairo2-dev pandoc gettext`
