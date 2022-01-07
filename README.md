# "ALFRED" - Advanced Legendary Fucking Rapid Epic Development

## Installation

### Linux

Install dipendences from your distro repo

    sudo apt install git virtualenv build-essential python3-dev libdbus-glib-1-dev libgirepository1.0-dev bzcat psql

Then move to alfred folder

    $ cd ALFRED_PATH

as root do

    # pip3 install -r requirements.txt

### Windows

Install following software:

* Python3
* Git for Windows
* PostgreSQL (possibly latest version)

In case of pip compilation errors consider installing [Build Tools for VS](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019) (Select C++ build tools in the Workloads tab)


## Usage

First move in alfred path

    $ cd ALFRED_PATH

Show the command list

    $ python3 alfred.py

Or install it with

    $ sudo python3 setup.py install

and use it as system software

    $ alfred COMMAND [OPTIONS]

## Known Issues

Following features are not supported on Windows:

* Notification on 'restoredb' completion
* -f option of 'restoredb' command (Only available if Windows Subsystem for Linux is installed)
* .bz2 as file type to be passed to 'restoredb' completion. This kind of file must be decompressed and then passed as plain text
