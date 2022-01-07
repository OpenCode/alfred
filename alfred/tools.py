# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from passlib.hash import pbkdf2_sha512 as crypt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import click
import platform

try:
    import dbus
except ImportError:
    pass


@click.command()
@click.option('-p', '--password', required=True)
def crypt_password(password):
    """
        Crypt password to insert it in Odoo database
    """
    if password:
        password_crypted = crypt.encrypt(password)
        click.echo(password_crypted)
        return password_crypted
    return ''


@click.command()
@click.option('-m', '--message')
def notify(message):
    if platform.system() == 'Windows':
        return
        # TODO: add notification support for Windows
    body = ''
    app_name = 'Alfred'
    app_icon = ''
    timeout = 5000
    actions = []
    hints = []
    replaces_id = 0
    _bus_name = 'org.freedesktop.Notifications'
    _object_path = '/org/freedesktop/Notifications'
    _interface_name = _bus_name

    session_bus = dbus.SessionBus()
    obj = session_bus.get_object(_bus_name, _object_path)
    interface = dbus.Interface(obj, _interface_name)
    interface.Notify(app_name, replaces_id, app_icon,
                     message, body, actions, hints, timeout)


@click.command()
@click.argument('start', required=True)
@click.argument('end', required=True)
def hours(start='', end=''):
    """
        Calculate difference in hours between start and end
    """
    hour_start, minute_start = start.split(':')
    hour_end, minute_end = end.split(':')
    dt_start = datetime.strptime(
        '2000-01-01 %s:%s:00' % (hour_start.rjust(2, '0'), minute_start),
        '%Y-%m-%d %H:%M:%S')
    dt_end = datetime.strptime(
        '2000-01-01 %s:%s:00' % (hour_end.rjust(2, '0'), minute_end),
        '%Y-%m-%d %H:%M:%S')
    dt_diff = relativedelta(dt_end, dt_start)
    click.echo('%sh %sm' % (dt_diff.hours, dt_diff.minutes))
