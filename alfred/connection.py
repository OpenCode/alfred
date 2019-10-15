# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from prettytable import PrettyTable
import click
import odoorpc
import subprocess


'''
DEPRECATED in MIGRATION 2.0 -> 3.0
TODO: Delete it or replace with another feature
@click.command()
@click.argument('server', default='0', type=int)
def ssh(server):
    """
        Connect automatically in ssh with a remote server
        :param ssh_id: id of server to connect with. Get from connecions list
    """
    if server:
        # server = int(server)
        odoo = odoorpc.ODOO('xxx', protocol='jsonrpc+ssl', port=443)
        odoo.login('xxx', 'xxx', 'xxx')
        connection = odoo.env['connection.data'].browse(server)
        command = 'sshpass -p \'{password}\' ssh {user}@{host} -p {port}'.\
            format(
                password=connection.password,
                user=connection.user,
                host=connection.host,
                port=connection.port or '22')
        click.echo('Using command: %s' % command)
        subprocess.call(command, shell=True)
    else:
        odoo = odoorpc.ODOO('xxx', protocol='jsonrpc+ssl', port=443)
        odoo.login('xxx', 'xxx', 'xxx')
        connection_type_id = odoo.env['connection.type'].search(
            [('name', '=', 'SSH')])[0]
        data_model = odoo.env['connection.data']
        conntection_ids = data_model.search(
            [('type_id', '=', connection_type_id)], order='partner_id')
        ptable = PrettyTable(
            ['#', 'Partner', 'Name', 'User', 'Host', 'Port', 'Note'])
        ptable.align['#'] = 'l'
        ptable.align['Partner'] = 'l'
        ptable.align['Name'] = 'l'
        ptable.align['User'] = 'l'
        ptable.align['Host'] = 'l'
        ptable.align['Port'] = 'l'
        ptable.align['Note'] = 'l'
        for connection in data_model.read(conntection_ids,
                                        ['id', 'partner_id', 'name', 'user',
                                        'host', 'port', 'notes']):
            ptable.add_row([connection['id'],
                            connection['partner_id'][1],
                            connection['name'] or '',
                            connection['user'] or '',
                            connection['host'] or '',
                            connection['port'] or '',
                            connection['notes'] or '',
                            ])
        print(ptable)
'''
