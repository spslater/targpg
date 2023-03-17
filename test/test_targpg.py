"""Testing targpg"""
import getpass
from io import StringIO
from os import makedirs
from pathlib import Path
from shutil import rmtree
from unittest import TestCase
from unittest.mock import patch

from targpg import Targpg, tglog

tglog.setLevel("CRITICAL")


class TargpgTests(TestCase):
    """Test functionality of BatchRenamer"""

    @staticmethod
    def assertFileExists(filepath, msg=None):
        """Assert if a path exists or not"""
        if not Path(filepath).exists():
            raise AssertionError(msg or f"{filepath} does not exist")

    @staticmethod
    def assertFileNotExists(filepath, msg=None):
        """Assert if a path exists or not"""
        if Path(filepath).exists():
            raise AssertionError(msg or f"{filepath} does exist")

    @staticmethod
    def _make_clean(dirname):
        dirpath = Path(dirname)
        rmtree(dirpath, ignore_errors=True)
        dirpath.mkdir(parents=True, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.test = "test"
        cls.work = Path(cls.test, "work")
        cls._make_clean(cls.work)
        cls.extr = Path(cls.test, "extr")
        cls._make_clean(cls.extr)
        cls.archive = Path(cls.work, "secure.tgz.gpg")

        cls.passfile = Path(cls.work, "passfile")
        cls.password = "password"
        cls.passfile.write_text(cls.password, encoding="utf-8")
        cls.wrongpass = Path(cls.work, "wrongpass")
        cls.wrongpass.touch()

        cls.file1 = Path(cls.work, "file1.txt")
        cls.file1_data = "hello"
        cls.file1.write_text(cls.file1_data, encoding="utf-8")

        cls.file2 = Path(cls.work, "file2.txt")
        cls.file2_data = "goodbye"
        cls.file2.write_text(cls.file2_data, encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.work, ignore_errors=True)
        rmtree(cls.extr, ignore_errors=True)

    def tearDown(self):
        try:
            self.archive.unlink()
        except FileNotFoundError:
            pass

    def _create(self):
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.add(self.file1, self.file2)
        gt.save()
        return gt

    def test_01_init(self):
        """Initalizing with different attributes"""
        with self.assertRaises(FileNotFoundError), patch(
            "builtins.input", return_value="n"
        ) as mock_input:
            Targpg(self.archive, passfile=self.passfile)
        self.assertFileNotExists(
            self.archive,
            "File should not exist when create confirmation is negative",
        )

        with patch("builtins.input", return_value="y") as mock_input:
            gt = Targpg(self.archive, passfile=self.passfile)
        gt.save().exit()
        self.assertFileExists(
            self.archive,
            "File should exist when create confirmation is positive (begins with `y`)",
        )

        with self.assertRaises(
            PermissionError,
            msg="Should not open file with wrong password",
        ):
            Targpg(self.archive, passfile=self.wrongpass)

        self.archive.unlink()
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.save().exit()
        self.assertFileExists(
            self.archive,
            msg="File be created without prompt with autocreate `True`",
        )

    def test_02_add(self):
        """Add files to the archive"""
        gt = self._create()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        self.assertFileExists(
            self.archive,
            "File should be saved when files are added",
        )
        list_value = mock_stdout.getvalue()
        self.assertNotEqual(
            len(list_value),
            0,
            "Files in archive should appear when listed",
        )

    def test_03_dupe(self):
        """Add dupe file to the archive fails"""
        gt = self._create()
        with self.assertRaises(
            ValueError,
            msg="Should not be able to add the same file",
        ):
            gt.add(self.file1)

    def test_04_dupe(self):
        """Add dupe file to the archive fails"""
        gt = self._create()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files = len(mock_stdout.getvalue().splitlines())

        gt.update(self.file1)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files_update = len(mock_stdout.getvalue().splitlines())

        self.assertEqual(
            num_files,
            num_files_update,
            "Update should replace the file in the archive",
        )

    def test_05_remove(self):
        """Remove file from the archive"""
        gt = self._create()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files = len(mock_stdout.getvalue().splitlines())

        gt.remove(self.file1)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files_remove = len(mock_stdout.getvalue().splitlines())

        self.assertNotEqual(
            num_files,
            num_files_remove,
            "File should be removed from the archive",
        )

    def test_06_extract(self):
        """Extract files from the archive"""
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.add(self.file1, self.file2)
        gt.extract(self.file1, outdir=self.extr)
        self.assertFileExists(
            Path(self.extr, self.file1),
            "File should be extracted when passed as an argument",
        )

        with patch("builtins.input", return_value="1") as mock_input:
            gt.extract(outdir=self.extr)
        self.assertFileExists(
            Path(self.extr, self.file2),
            "File should be extracted when selected from the command line",
        )
