# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import click
# from cookiecutter.main import cookiecutter
import pycodestyle
from termcolor import colored

'''
DEPRECATED in MIGRATION 2.0 -> 3.0
TODO: Delete it or replace with another feature
@click.command()
def generate_odoo_module():
    """
        Generate an Odoo module from a template
    """
    click.echo(
        'Using '
        'xxx.git'
        )
    cookiecutter(
        'xxx.git'
        )
'''


def _print_log_message_header(message):
    click.echo(''.rjust(len(message), '-'))
    click.echo(message)
    click.echo(''.rjust(len(message), '-'))


def _prepare_commit_check_pep(arguments):
    """
        Check PEP8 for all the files in path
    """
    path = arguments['path']
    style = pycodestyle.StyleGuide(paths=[path], quiet=False)
    report = style.check_files()
    if report.total_errors:
        response = 'error'
        message = '{errors} errors found!'.format(errors=report.total_errors)
    else:
        response = 'positive'
        message = 'It\'s all OK!'
    return {
        'response': response,
        'message': message}


def _prepare_commit_check_pdb(arguments):
    """
        Check pdb in all the files in path
    """
    keyword = 'import pdb'
    path = arguments['path']
    pdb_found = 0
    for root, _, files in os.walk(path, onerror=None):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'rb') as f:
                    for line_number, line in enumerate(f, 1):
                        try:
                            line = line.decode('utf-8')
                        except ValueError:
                            continue
                        if keyword in line:
                            click.echo(
                                f'{file_path}::Line {line_number}')
                            pdb_found += 1
            except (IOError, OSError):
                pass
    if pdb_found:
        response = 'error'
        message = f'{pdb_found} PDB found!'
    else:
        response = 'positive'
        message = 'It\'s all OK!'
    return {'response': response, 'message': message}


@click.command()
@click.option('-p', '--path',  help="Path of code to check", default='.')
def prepare_commit(path=None):
    """
        Check code before commit
    """
    # Create a list of steps to follow
    steps = {
        'check_pep8': {
            'header': 'Check PEP8',
            'function': _prepare_commit_check_pep,
            'arguments': {'path': path},
            },
        'check_pdb': {
            'header': 'Check PDB',
            'function': _prepare_commit_check_pdb,
            'arguments': {'path': path},
            },
        }
    total_steps = len(steps.keys())
    # For every step print an header message, execute a function
    # and print result
    for counter, step in enumerate(steps, 1):
        _print_log_message_header(
            '{counter}/{total_steps} - {header}'.format(
                counter=counter,
                total_steps=total_steps,
                header=steps[step]['header']
                ))
        result = steps[step]['function'](steps[step]['arguments'])
        if result['response'] == 'error':
            color = 'red'
        else:
            color = 'green'
        log_message = colored(result['message'], color)
        click.echo(log_message)
