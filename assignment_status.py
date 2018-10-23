#!/usr/bin/env python3
import argparse
import os
import sys

from os import access, getcwd, listdir
from os.path import abspath, dirname, join


__version__ = "0.1.0"
SCRIPT_ROOT = abspath(dirname(__file__))

# Config key of the Hardware Simulator executable path
KEY_HWEX = "hardware_simulator_executabe"


class ConfigManager(object):
    CONFIG_NAME = ".n2trc"
    DEFAULT_CONFIG_PATH = join(SCRIPT_ROOT, CONFIG_NAME)
    
    def __init__(self, configpath=None):
        """
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

    def write(self):
        with open(self._configpath, "wt") as outstream:
            for key, value in self._config.items():
                outstream.write("%s=%s\n" % (key, value))

        self._parse_config()
    
    def _parse_config(self):
        if not access(self._configpath, os.F_OK):
            # If the file does not exist, we create it empty and exit
            with open(self._configpath, "wt") as outstream:
                outstream.write("")
        elif not access(self._configpath, os.R_OK):
            raise OSError("%s has no read permissions" % self._configpath)
        else:
            with open(self._configpath) as instream:
                for line in instream:
                    key, value = line.split("=", maxsplit=1)

                    self._config[key] = value


def main():
    parser = argparse.ArgumentParser(
        description="Reports the status of .tst files of a Nand2Tetris "
        "assignment",
        epilog="Version %s" % __version__
    )

    parser.add_argument(
        "-e", "--set-executable", nargs=1, metavar="FULL PATH",
        help="Store the new location of the Hardware Simulator executable and"
        " exit."
    )
    parser.add_argument(
        "directory", nargs=1, required=False, default=getcwd(), metavar="DIR",
        help="Directory where to look for .tst files (defaults to ./)."
    )

    args = parser.parse_args()
    c = ConfigManager()

    if args.set_executable:
        c[KEY_HWEX] = abspath(args.set_executable[0])
        c.write()

        return 0
    else:
        if not KEY_HWEX in c:
            print(
                "No executable found for the Hardware Simulator. Please rerun"
                " the script and specify it in the [-e|--set-executable]"
                " option.", file=sys.stderr
            )

            return 1

        print("Hardware Simulator executable in %s" % c[KEY_HWEX])

        for e in listdir(args.directory[0]):
            if e.endswith(".tst"):
                print(e)

        # TO-DO Finish implementing


if __name__ == "__main__":
    exit(main())
