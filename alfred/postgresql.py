# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import click
import psycopg2
import psycopg2.extras
from prettytable import PrettyTable
from .tools import crypt_password, notify
import os
import subprocess


@click.command()
@click.option('-b', '--backup', required=True, help='Backup file path to fox')
def fix_postgres_version(backup):
    click.echo('Fix postegres problem version on backup file %s' % backup)
    subprocess.call(['sed', '-i', '-r', '-e', '/.+AS integer/d', backup])


def get_pg_connection(db='', user='', password=''):
    query = "dbname='{db}' user='{user}' host='localhost' password='{passw}'"
    # ------ Open Connection with database
    try:
        conn = psycopg2.connect(query.format(
            db=db, user=user, passw=password))
    except:
        print('Impossible to connect with {db}'.format(db=db))
        return False, False
    cr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cr


@click.command()
@click.option('-d', '--db', required=True,
              help='Database name')
@click.option('-u', '--user', default='odoo', show_default=True,
              help='Database user')
@click.option('-p', '--password', default='odoo', show_default=True,
              help='Database password')
def get_crons(db, user, password):
    """
        Get all crons in a Odoo database
    """
    # ------ Get cursor
    conn, cr = get_pg_connection(db=db, user=user, password=password)
    if not conn and not cr:
        return []
    # ------ Search all active cron
    cr.execute('SELECT * from ir_cron ORDER BY id asc')
    # ------ Create list of dicts of records
    records = [dict(r) for r in cr.fetchall()]
    # ------ Show records
    ptable = PrettyTable(['ID', 'Active', 'Name'])
    ptable.align['Name'] = 'l'
    for record in records:
        ptable.add_row([record['id'],
                        'X' if record['active'] else ' ',
                        record['name'], ])
    print(ptable)
    return records


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
@click.option('-p', '--password', default='odoo', show_default=True)
@click.option('-c', '--crons', required=True,
              help='Id or ids of crons separateed by "," or ";".'
              ' To disable all the crons use "*"')
@click.pass_context
@click.confirmation_option(help='Are you sure you want to disable crons?')
def disable_crons(ctx, db, user, password, crons):
    """
        Disable all or some crons in a Odoo database
    """
    # ------ Get cursor
    conn, cr = get_pg_connection(db=db, user=user, password=password)
    if not conn and not cr:
        return
    # ------ Disable all cron records
    if crons == '*':
        query = 'UPDATE ir_cron SET active=false'
    # ------ Disable passed records
    else:
        ids = crons.replace(';', ',')
        query = 'UPDATE ir_cron SET active=false WHERE id in ({ids})'.format(
            ids=ids,)
    cr.execute(query)
    conn.commit()
    # ----- Print result
    ctx.invoke(get_crons, db=db, user=user, password=password)


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
@click.option('-p', '--password', default='odoo', show_default=True)
def get_smtp(db, user, password):
    """
        Get all SMTP in a Odoo database
    """
    # ------ Get cursor
    conn, cr = get_pg_connection(db=db, user=user, password=password)
    if not conn and not cr:
        return
    # ------ Search all active cron
    cr.execute('SELECT * from ir_mail_server ORDER BY id asc')
    # ------ Create list of dicts of records
    records = [dict(r) for r in cr.fetchall()]
    # ------ Show records
    ptable = PrettyTable(['ID', 'Active', 'Name', 'Host', 'User'])
    ptable.align['Name'] = 'l'
    for record in records:
        ptable.add_row([record['id'],
                        'X' if record['active'] else ' ',
                        record['name'],
                        record['smtp_host'],
                        record['smtp_user'],
                        ])
    print(ptable)
    return records


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
@click.option('-p', '--password', default='odoo', show_default=True)
@click.option('-s', '--smtp', required=True,
              help='Id or ids of smtp server separateed by "," or ";".'
              ' To disable all the smtp server use "*"')
@click.pass_context
@click.confirmation_option(help='Are you sure you want to disable smtp?')
def disable_smtp(ctx, db, user, password, smtp):
    """
        Disable all or some SMTP in a Odoo database
    """
    # ------ Get cursor
    conn, cr = get_pg_connection(db=db, user=user, password=password)
    # ------ Disable all cron records
    if smtp == '*':
        query = 'UPDATE ir_mail_server SET active=false'
    # ------ Disable passed records
    else:
        ids = smtp.replace(';', ',')
        query = 'UPDATE ir_mail_server SET active=false WHERE id in ({ids})'\
            .format(ids=ids,)
    cr.execute(query)
    conn.commit()
    # ----- Print result
    ctx.invoke(get_smtp, db=db, user=user, password=password)


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
@click.option('-p', '--password', default='odoo', show_default=True)
@click.pass_context
@click.confirmation_option(
    help='Are you sure you want to reset admin password?')
def reset_admin_password(ctx, db, user, password):
    """
        Reset admin password to 'admin'
    """
    # ------ Get cursor
    conn, cr = get_pg_connection(db=db, user=user, password=password)
    query = "SELECT state FROM ir_module_module WHERE name = 'auth_crypt'"
    cr.execute(query)
    rows = cr.fetchall()
    admin_password_value = 'admin'
    admin_password_field = 'password'
    if rows[0][0] == 'installed':
        admin_password_value = ctx.invoke(crypt_password,
                                          password=admin_password_value)
        admin_password_field = 'password_crypt'
    query = "UPDATE res_users SET {field}='{value}' WHERE login='admin'".\
        format(field=admin_password_field, value=admin_password_value)
    cr.execute(query)
    conn.commit()


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
def createdb(db, user):
    """
        Create a new db in postegresql
    """
    click.echo('Creating database %s...' % db)
    subprocess.call(['createdb', '-U', user, db])
    click.echo('Database %s created' % db)


@click.command()
@click.option('-d', '--db', required=True)
@click.option('-u', '--user', default='odoo', show_default=True)
@click.confirmation_option(help='Are you sure you want to drop database?')
def dropdb(db, user):
    """
        Drop a db in postegresql
    """
    click.echo('Dropping database %s...' % db)
    subprocess.call(['dropdb', '-U', user, db])
    click.echo('Database %s dropped' % db)


@click.command()
@click.option('-d', '--db', required=True, help="Name of new database")
@click.option('-b', '--backup', required=True,
              help="Path of backup file to restore")
@click.option('-t', '--type', default='binary', show_default=True,
              type=click.Choice(['binary', 'plain', 'bz2']),
              help="Type of file to restore")
@click.option('-f', '--fix', is_flag=True, default=False, show_default=True,
              help='Fix a problem when restore a backup of a new version '
              'of postgres on a previuos version of postgres')
@click.option('-u', '--user', default='odoo', show_default=True,
              help='User to create db')
@click.option('-p', '--password', default='odoo', show_default=True,
              help='Password to create db')
@click.pass_context
def restoredb(ctx, db, backup, type, fix, user, password):
    """
        Create a new db in postegresql, restore a backup and disable all crons
    """
    # ----- Create database
    ctx.invoke(createdb, db=db, user=user)
    # ----- Fix Postgres version incompatibility from 10.X to 9.X
    if fix:
        ctx.invoke(fix_postgres_version, backup=backup)
    # ----- Restore backup
    click.echo('Restore backup')
    if type == 'binary':
        subprocess.call('pg_restore -O -U %s -d %s %s' % (user, db,  backup),
                        shell=True)
    elif type == 'bz2':
        subprocess.call('bzcat %s | psql -U %s -d %s' % (backup, user, db),
                        shell=True)
    elif type == 'plain':
        subprocess.call(
            'psql %s -U %s < %s' % (db, user, backup.replace('.bz2', '')),
            shell=True)
    # ----- Disable crons
    click.echo('Disable all crons for database %s' % db)
    ctx.invoke(disable_crons, db=db, user=user, password=password, crons='*')
    # ----- Disable SMTP
    click.echo('Disable all smtp servers for database %s' % db)
    ctx.invoke(disable_smtp, db=db, user=user, password=password, smtp='*')
    # ----- Change admin password to 'admin' to run base test without problem
    click.echo('Change admin password to "admin" for database %s' % db)
    ctx.invoke(reset_admin_password, db=db, user=user, password=password)
    message = 'Database {db} restored with admin password set to "admin"'.\
        format(db=db)
    ctx.invoke(notify, message=message)
