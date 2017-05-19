# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Installs all of the dependencies for the Redfish Interface Emulator

import glob
import os
import sys
import zipfile
from importlib import import_module
import subprocess as sub

# Executes, "python ./setup.py install", which executes the setup.py
# script in the current directory
setup_py = lambda: sub.Popen(
    [sys.executable, os.path.join('.', 'setup.py'), 'install'],
    stdout=sub.PIPE, stderr=sub.PIPE)


class InstallError(Exception):
    pass


class Dependency(object):
    """
    Dependency Class
    """
    depenedncy_dir = 'dependencies'

    def __init__(self, zip_file, import_str):
        """
        Dependency Constructor

        Arguments:
            zip_file   - Zip file in the depenedncy_dir
            import_str - String to use to tell if the dependency has already
                         been installed
        """
        self.zip = zip_file
        self.extracted_dir = zip_file.split('.zip')[0]
        self.import_str = import_str

    def __str__(self):
        return self.import_str

    @property
    def installed(self):
        """
        True if the dependency has already been installed, and False if not
        """
        installed = True
        try:
            import_module(self.import_str)
        except ImportError:
            installed = False
        return installed

    def install(self):
        """
        Install the dependency

        Throws in InstallError if the installation encounters an error.
        """
        cwd = os.getcwd()
        os.chdir(self.depenedncy_dir)

        # Unzipping the dependency
        zipf = zipfile.ZipFile(self.zip)
        zipf.extractall('.')

        os.chdir(self.extracted_dir)

        # Installsstalling the dependency
        p = setup_py()
        out, err = p.communicate()

        os.chdir(cwd)

        if p.returncode != 0:
            raise InstallError('{0}\n{1}'.format(out, err))


_dependencies = [
    Dependency('setuptools-12.0.5.zip', 'setuptools'),
    Dependency('Werkzeug-0.10.1.zip', 'werkzeug'),
    Dependency('MarkupSafe-0.23.zip','markupsafe'),
    Dependency('Jinja2-2.7.3.zip', 'jinja2'),
    Dependency('itsdangerous-0.24.zip', 'itsdangerous'),
    Dependency('Flask-0.10.1.zip', 'flask'),
    Dependency('aniso8601-0.92.zip', 'aniso8601'),
    Dependency('six-1.9.0.zip', 'six'),
    Dependency('pytz-2014.10.zip', 'pytz'),
    Dependency('Flask-RESTful-0.3.1.zip', 'flask.ext.restful'),
    Dependency('Flask-HTTPAuth-master.zip', 'flask_httpauth'),
    Dependency('requests-2.5.1.zip', 'requests')]


def main():
    """
    Main Function
    """
    global _dependencies

    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print ('Checks if a given dependency has been installed and installs '\
              'it if it hasn\'t. \n\nThe following dependencies are checked:')
        for dep in _dependencies:
            print ('\t', dep)
    else:
        try:
            for dep in _dependencies:
                if not dep.installed:
                    print ('Installing dependency', dep)
                    dep.install()
                else:
                    print ('Dependency: "{0}" is already installed'.format(dep))
        except InstallError as e:
            print ('Error installing dependencies')
            print (e.message)


if __name__ == '__main__':
    main()
