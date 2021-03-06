"""Secure a compressed tarfile with gpg password"""
__all__ = ["Targpg", "tglog"]

import gzip
import logging
import sys
import tarfile
from getpass import getpass
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from gnupg import GPG

from .meta import __author__, __version__

PROG_NAME = Path(__file__).stem

tglog = logging.getLogger(PROG_NAME)
tglog.setLevel(logging.INFO)
handle = logging.StreamHandler(sys.stdout)
handle.setFormatter(logging.Formatter("> %(message)s"))
tglog.addHandler(handle)

Pathname = Union[str, Path]

Path.__eq__ = lambda self, b: str(self) == str(b)


class Targpg:
    """Mangae a password protected tar archvie

    :param filename: archive file to manage
    :type filename: Pathname, optional
    :param passfile: file to load password from, defaults to None
    :type passfile: Pathname
    :param autocreate: if archive does not exist create it without confirmation,
        defaults to False
    :type autocreate: bool
    """

    def __init__(
        self,
        filename: Pathname,
        passfile: Optional[Pathname] = None,
        autocreate: bool = False,
    ):
        self.gpg = GPG()
        self.filename = Path(filename)
        self.exists = self.filename.is_file()
        if not self.exists and not autocreate:
            create = input("Secure file does not exist; Create new? ").lower()
            if not create.startswith("y"):
                raise FileNotFoundError("No secure file to load")
        self.password = self._load_pass(passfile)
        self.raw = BytesIO()
        # pylint: disable=consider-using-with
        self.tar = tarfile.TarFile(fileobj=self.raw, mode="w")
        if self.exists:
            self._load_tar()

    def _load_tar(self):
        try:
            with tarfile.open(fileobj=self._decrypt(), mode="r:gz") as fp:
                for member in fp.getmembers():
                    self.tar.addfile(member, fp.extractfile(member))
        except tarfile.ReadError:
            pass

    def _load_pass(self, passfile: Pathname) -> Optional[str]:
        if passfile:
            with open(passfile, "r", encoding="utf-8") as fp:
                return fp.read()
        if not self.exists:
            return getpass("New Password: ")
        return getpass()

    def _readmode(self):
        if not self.tar.mode.startswith("r"):
            self.tar.close()
            self.raw.seek(0)
            # pylint: disable=consider-using-with
            self.tar = tarfile.TarFile(fileobj=self.raw, mode="r")

    def _writemode(self):
        if not self.tar.mode.startswith("w"):
            self.tar.close()
            self.raw.seek(0)
            # pylint: disable=consider-using-with
            self.tar = tarfile.TarFile(fileobj=self.raw, mode="w")

    def _decrypt(self) -> BytesIO:
        with open(self.filename, "rb") as fp:
            data = self.gpg.decrypt_file(fp, passphrase=self.password)

        if not data.ok:
            raise PermissionError(f"Unable to decrypt {self.filename}; {data.status}")

        return BytesIO(data.data)

    def _encrypt(self, data) -> BytesIO:
        data = self.gpg.encrypt(
            data,
            recipients=None,
            symmetric=True,
            passphrase=self.password,
        )
        if not data.ok:
            raise RuntimeError(f"Unable to encrypt that tarfile data; {data.status}")

        return data.data

    @staticmethod
    def _compress(bytesio) -> bytes:
        cur = bytesio.tell()
        bytesio.seek(0)
        data = gzip.compress(bytesio.read())
        bytesio.seek(cur)
        return data

    @staticmethod
    def _path(filepath: Pathname, directory: Pathname) -> str:
        if not isinstance(filepath, Path):
            filepath = Path(filepath)
        tglog.debug("dir: %s", directory)
        if not directory and filepath.is_absolute():
            tglog.debug("file is abs; %s", filepath)
            return str(filepath), str(filepath)

        if not directory:
            directory = "."

        if not isinstance(directory, Path):
            directory = Path(directory)
        directory = directory.resolve()
        tglog.debug("working dir; %s", directory)

        abspath = directory.joinpath(filepath).resolve()
        tglog.debug("abs path; %s", abspath)
        tglog.debug("rel path; %s", abspath.relative_to(directory))
        return str(abspath), str(abspath.relative_to(directory))

    def add(
        self,
        *filenames: Pathname,
        directory: Optional[Pathname] = None,
        unique: bool = False,
        update: bool = False,
    ) -> "Targpg":
        """Add new files to the archive

        :param *filenames: Pathnames to add to the archive
        :type *filenames: Pathname
        :param directory: archive filepath is relative to this directory,
            defaults to None
        :type directory: Optional[Pathname], optional
        :param unique: only allow unique files to be added, defaults to False
        :type unique: bool, optional
        :param update: update a file if it exists otherwise add a duplicate,
            defaults to False
        :type update: bool, optional
        :raises ValueError: a duplicate file is being added when uniqueness is
            being enforced
        :return: self to allow chaining
        :rtype: Targpg
        """
        if not filenames:
            return self

        self._writemode()

        if unique or update:
            tarfiles = self.tar.getnames()

        if unique:
            dupes = [f for f in filenames if str(f) in tarfiles]
            if dupes:
                raise ValueError(f"File(s) already exists in archive; {dupes}")

        filenames = list(filenames)
        if update:
            upfiles = [f for f in filenames if str(f) in tarfiles]
            tglog.debug("update; %s", upfiles)
            self.update(*upfiles, directory=directory)
            filenames = [f for f in filenames if f not in upfiles]

        for filename in filenames:
            fullfile, addfile = self._path(filename, directory)
            tglog.debug("adding; %s", addfile)
            self.tar.add(fullfile, arcname=addfile)

        return self

    def update(
        self,
        *filenames: Pathname,
        directory: Optional[Pathname] = None,
    ) -> "Targpg":
        """Update an existing file in the archvie

        :param *filenames: Pathnames to update in the archive
        :type *filenames: Pathname
        :param directory: archive filepath is relative to this directory,
            defaults to None
        :type directory: Optional[Pathname], optional
        :return: self to allow chaining
        :rtype: Targpg
        """
        temp = BytesIO()
        # pylint: disable=consider-using-with
        newtar = tarfile.TarFile(fileobj=temp, mode="w")
        self._readmode()
        filenames = list(filenames)
        for member in self.tar.getmembers():
            if member.name in filenames:
                tglog.debug("updating; %s", member.name)
                filenames.remove(member.name)
                newtar.add(member.name)
            else:
                newtar.addfile(member, self.tar.extractfile(member))

        filenames = [self._path(filename, directory) for filename in filenames]
        for filepath, arcname in filenames:
            tglog.debug("adding; %s", arcname)
            newtar.add(filepath, arcname=arcname)

        self.raw.close()
        self.raw = temp
        self.tar = newtar

        return self

    def extract(self, *filenames: Pathname, outdir: Pathname = ".") -> "Targpg":
        """Extract a file from the archive.

            If no filenames are given, a list will be displayed  and input will
            be taken from stdin.

        :param *filenames: Pathnames to extract from the archive
        :type *filenames: Pathname
        :param outdir: directory to export files into, defaults to "."
        :type outdir: Pathname, optional
        :return: self to allow chaining
        :rtype: Targpg
        """
        names = self.tar.getnames()
        filenames = [str(f) for f in filenames]
        if not filenames:
            pad = len(str(len(names)))
            for idx, name in enumerate(names):
                tglog.info("%s %s", str(idx).rjust(pad), name)
            res = input("Extract? ")
            idxs = [int(r) for r in res.split()]
            filenames = [names[i] for i in idxs]
        else:
            oknames = []
            for filename in filenames:
                if filename not in names:
                    tglog.debug("name not in opts; %s", filename)
                else:
                    oknames.append(filename)
            filenames = oknames
        self._readmode()
        for filename in filenames:
            tglog.debug("extracting; %s", filename)
            self.tar.extract(filename, path=outdir)

        return self

    def list(self):
        """List contents of the archvie to stdout"""
        self.tar.list()

    def save(self, filename: Pathname = None) -> "Targpg":
        """Save the archive to file

        If no filename is given, original filename is used.
        No data is written to disk until this method is called.

        :param filename: Pathname to save archive to,
            defaults to loaded archive name
        :type filename: Pathname
        :return: self to allow chaining
        :rtype: Targpg
        """
        tocrypt = self._compress(self.raw)
        data = self._encrypt(tocrypt)
        with open(filename or self.filename, "wb") as fp:
            fp.write(data)

        return self

    def exit(self):
        """Close the tar and byte streams in memory for cleanup"""
        self.tar.close()
        self.raw.close()
