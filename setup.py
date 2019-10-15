# Copyright 2019 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from setuptools import setup


setup(
    name='alfred',
    version='3.0.0',
    description='Alfred',
    url='https://github.com/OpenCode/alfred',
    author='Francesco Apruzzese',
    author_email='cescoap@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        ],
    keywords='alfred development odoo postgesql',
    license='AGPL',
    packages=['alfred'],
    install_requires=[
        'click',
        'passlib',
        'prettytable',
        'psycopg2-binary',
        'dbus-python',
        'cookiecutter',
        'pycodestyle',
    ],
    entry_points={
        'console_scripts': ['alfred=alfred.core:script'],
        },
    zip_safe=False,
    )
