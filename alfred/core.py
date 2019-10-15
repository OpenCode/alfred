# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import click
from .tools import crypt_password, hours
from .postgresql import get_crons, disable_crons, \
    get_smtp, disable_smtp, \
    reset_admin_password, \
    createdb, dropdb, restoredb
from .development import prepare_commit


@click.group('alfred_command')
def alfred_command():
    pass


# ----- Register tools functions
alfred_command.add_command(crypt_password)
alfred_command.add_command(hours)
# ----- Register postgresql functions
alfred_command.add_command(get_crons)
alfred_command.add_command(disable_crons)
alfred_command.add_command(get_smtp)
alfred_command.add_command(disable_smtp)
alfred_command.add_command(reset_admin_password)
alfred_command.add_command(createdb)
alfred_command.add_command(dropdb)
alfred_command.add_command(restoredb)
# ----- Development functions
alfred_command.add_command(prepare_commit)


def script():
    alfred_command()
