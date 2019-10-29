# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import re
import click
import git
# from cookiecutter.main import cookiecutter
import pycodestyle
from termcolor import colored

REGEX_GIT_DIFF_OLD_LINE = \
    r'\-(.+)(\'|\")version(\'|\")(.|):(\s|)(\'|\")(.+)(\'|\")'
REGEX_GIT_DIFF_NEW_LINE = \
    r'\+(.+)(\'|\")version(\'|\")(.|):(\s|)(\'|\")(.+)(\'|\")'

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
    return [{
        'response': response,
        'message': message}]


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
    return [{'response': response, 'message': message}]


def _prepare_commit_check_odoo_module_version(arguments):
    """
        Check if version of odoo module is changed
    """
    path = arguments['path']
    repo = git.Repo(path)
    diffs = repo.index.diff(None, create_patch=True)
    if not diffs:
        response = 'positive'
        message = 'It\'s all OK!'
        return [{'response': response, 'message': message}]
    manifest_diffs = [
        diff
        for diff
        in diffs
        if diff.a_path.endswith('__manifest__.py') and not diff.new_file
        ]
    if not manifest_diffs:
        response = 'error'
        message = 'Change \'version\' key value in __manifest__.py'
        return [{'response': response, 'message': message}]
    responses = []
    for manifest_diff in manifest_diffs:
        old_version = ''
        new_version = ''
        diff = manifest_diff.diff.decode("utf-8")
        changes = diff.split('\n')
        for change in changes:
            if not old_version:
                search_old = re.search(REGEX_GIT_DIFF_OLD_LINE, change)
                if search_old:
                    old_version = search_old.group(7)
            if not new_version:
                search_new = re.search(REGEX_GIT_DIFF_NEW_LINE, change)
                if search_new:
                    new_version = search_new.group(7)
        if not old_version or not new_version:
            response = 'error'
            message = 'Change \'version\' key value in {mnf}'.format(
                mnf=manifest_diff.a_path
                )
        else:
            response = 'positive'
            message = \
                f'Version changed: ' \
                f'{old_version} -> {new_version} in {manifest_diff.a_path}'
        responses.append({'response': response, 'message': message})
    return responses


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
        'check_odoo_module_version': {
            'header': 'Check Odoo Module Version',
            'function': _prepare_commit_check_odoo_module_version,
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
        results = steps[step]['function'](steps[step]['arguments'])
        for result in results:
            if result['response'] == 'error':
                color = 'red'
            else:
                color = 'green'
            log_message = colored(result['message'], color)
            click.echo(log_message)
