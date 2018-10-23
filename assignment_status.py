#!/usr/bin/env python3
import argparse
import os
import sys

from os import access, getcwd, listdir
from os.path import abspath, dirname, join
from subprocess import call


__version__ = "0.3.1"
SCRIPT_ROOT = abspath(dirname(__file__))

# Config key of the Hardware Simulator executable path
CONFIG_FILENAME = ".n2trc"
KEY_HWEX = "hardware_simulator_executable"

ACT_EXECUTABLE = "set_executable"
ACT_REPORT = "report"
ACT_CONFIG = "show_config"


class ConfigManager(object):
    DEFAULT_CONFIG_PATH = join(SCRIPT_ROOT, CONFIG_FILENAME)
    
    def __init__(self, configpath=None):
        """
        Manages the project configuration in a ``key=value`` format.

        :param configpath: file path of the script configuration.
        """
        self._config = dict()

        if not configpath:
            self._configpath = self.DEFAULT_CONFIG_PATH
        else:
            configdir = dirname(configpath)

            if not access(configdir, F_OK):
                raise OSError("Directory %s does not exist" % configdir)
            elif not access(configdir, R_OK | W_OK):
                raise OSError("Directory %s is not RW" % configdir)
            else:
                self._configpath = configpath

        self._parse_config()

    def __getitem__(self, key):
        if key in self._config:
            return self._config[key]

        raise ValueError("key %s not found in config" % key)

    def __setitem__(self, key, value):
        self._config[key] = value

    def __contains__(self, key):
        return key in self._config

    def __del__(self):
        self._config = None
        self._configpath = None

    def __iter__(self):
        """Return an iterator of ``(key, value)`` pairs."""
        for key, value in self._config.items():
            yield key, value

    def write(self):
        with open(self._configpath, "wt") as outstream:
            for key, value in self._config.items():
                outstream.write("%s=%s\n" % (key, value))

        self._parse_config()

    @property
    def configpath(self):
        return self._configpath
    
    def _parse_config(self):
        """
        Parses the configuration from a file input to ``__init__()`` and reads
        it into memory.
        """
        if not access(self._configpath, os.F_OK):
            # If the file does not exist, we create it empty and exit
            with open(self._configpath, "wt") as outstream:
                outstream.write("")
        elif not access(self._configpath, os.R_OK):
            raise OSError("%s has no read permissions" % self._configpath)
        else:
            with open(self._configpath) as instream:
                for line in instream:
                    if line and not line.isspace() and not line.startswith("#"):
                        key, value = line.split("=", maxsplit=1)

                        self._config[key.strip()] = value.strip()


def print_report(c, path, colwidth=20):
    """
    Subroutine to print a Nand2Tetris Hardware Simulator report on ``path``
    by means of the configuration from ``c``.

    :param c: ``ConfigManager`` instance.
    :param path: directory path containing ``*.tst`` files.
    :param colwidth: minimum width (in units of spaces) of the first column.
    :return: exit status of the operation.
    """
    extension = ".tst"
    # Whether *.tst files have been reported in the current directory
    tst_found = False

    if not KEY_HWEX in c:
        print(
            "No executable found for the Hardware Simulator. Please rerun"
            " the script with the %s option." % ACT_EXECUTABLE,
            file=sys.stderr
        )

        return 1

    print("[Hardware Simulator executable in %s]\n" % c[KEY_HWEX])

    for e in listdir(path):
        if e.endswith(extension):
            tst_found = True
            space_padding = max(colwidth - len(e), 0)
            fullpath = abspath(join(path, e))

            print(e, " " * space_padding, end="", flush=True)
            call(
                [c[KEY_HWEX], fullpath],
                stdout=sys.stdout,
                stderr=sys.stderr
            )

    if not tst_found:
        print("No %s files found in %s" % (extension, path))

    return 0


def main():
    """
    :return: exit status code of the program.
    """
    parser = argparse.ArgumentParser(
        description="Reports the status of .tst files of a Nand2Tetris "
        "assignment",
        epilog="Version %s" % __version__
    )
    subparsers = parser.add_subparsers(title="Commands", dest="action")
    subparsers.required = True

    executable_parser = subparsers.add_parser(
        ACT_EXECUTABLE, help="Store the new location of the Hardware Simulator"
        " executable and exit."
    )
    report_parser = subparsers.add_parser(
        ACT_REPORT, help="Run the Hardware Simulator on a batch of files and"
        " report their individual result."
    )
    config_parser = subparsers.add_parser(
        ACT_CONFIG, help="Print out the configuration settings stored in %s." %
        CONFIG_FILENAME
    )
    # TO-DO Add uninstall sub command

    executable_parser.add_argument("filepath", nargs=1, metavar="FILE PATH")
    report_parser.add_argument(
        "directory", nargs='?', default=getcwd(), metavar="DIR",
        help="Directory where to look for .tst files (defaults to ./)."
    )

    c = ConfigManager()
    args = parser.parse_args()

    if args.action == ACT_EXECUTABLE:
        c[KEY_HWEX] = abspath(args.filepath[0])
        c.write()

        return 0
    elif args.action == ACT_REPORT:
        return print_report(c, args.directory)
    elif args.action == ACT_CONFIG:
        print("[Config settings stored in %s]\n" % c.configpath)

        for key, value in c:
            print("%s=%s" % (key, value))
    else:
        print("Action %s not recognized" % args.action, file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
