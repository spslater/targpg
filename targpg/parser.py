"""Commandline Parser for Targpg"""
__all__ = ["targpg_parser"]

from argparse import Action, ArgumentParser

from .targpg import PROG_NAME
from .meta import __version__


class ComboListAction(Action):
    """Action will combine lists from flag used multiple times
    eg: `-a one two -a three four`
    becomes [one, two, three four]
    instead of [[one, two], [three, four]]
    """

    def __call__(self, parser, namespace, values, option_string=None):
        current = getattr(namespace, self.dest, self.default) or []
        if isinstance(values, list):
            current.extend(values)
        else:
            current.append(values)
        if isinstance(self.nargs, int) and len(current) > self.nargs:
            opt = option_string or self.dest
            raise ValueError(f"Too many arguments passed for {opt}")
        setattr(namespace, self.dest, current)


def targpg_parser() -> ArgumentParser:
    """Generate the command line parser for the script"""
    parser = ArgumentParser(
        prog=PROG_NAME,
        description="manage secure archive containing sensative docs",
    )
    parser.add_argument(
        "archive",
        help="tar file secured by gpg symetric password",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--add",
        "-a",
        action=ComboListAction,
        dest="add",
        nargs="*",
        help="add files to the archive",
    )
    parser.add_argument(
        "--create",
        "-c",
        action="store_true",
        dest="autocreate",
        default=False,
        help="create the file without confirmation if it does not exist",
    )
    parser.add_argument(
        "--extract",
        "-e",
        action=ComboListAction,
        dest="extr",
        nargs="*",
        help="extract the files from the archive, if no files given a prompt will ask",
    )
    parser.add_argument(
        "--passfile",
        "-p",
        dest="passfile",
        help="file with archive password stored in it",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        dest="list",
        default=False,
        help="list the contents of the archive",
    )
    parser.add_argument(
        "--unique",
        "-x",
        action="store_true",
        dest="unique",
        default=False,
        help="only add unique files, if the file exists an error is thrown",
    )
    parser.add_argument(
        "--update",
        "-u",
        action="store_true",
        dest="update",
        default=False,
        help="overwrite existing files if any being passed in match",
    )
    parser.add_argument(
        "--output",
        "-o",
        action="store_true",
        dest="output",
        default=".",
        help="directory to extract files to",
    )
    parser.add_argument(
        "--directory",
        "-d",
        dest="directory",
        default=".",
        help="when adding files, do it relative to this directory",
    )
    return parser
