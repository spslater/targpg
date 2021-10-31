"""Testing targpg"""
import getpass
from io import StringIO
from os import makedirs
from pathlib import Path
from shutil import rmtree
from unittest import TestCase
from unittest.mock import patch

from targpg import Targpg
from targpg.targpg import logger as gt_logger
gt_logger.setLevel("CRITICAL")

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

    def test_01_init(self):
        """Initalizing with different attributes"""
        with self.assertRaises(FileNotFoundError), \
            patch("builtins.input", return_value="n") as mock_input:
            Targpg(self.archive, passfile=self.passfile)
        self.assertFileNotExists(self.archive)

        with patch("builtins.input", return_value="y") as mock_input:
            gt = Targpg(self.archive, passfile=self.passfile)
        gt.save().exit()
        self.assertFileExists(self.archive)

        with self.assertRaises(PermissionError):
            Targpg(self.archive, passfile=self.wrongpass)

        self.archive.unlink()
        self.assertFileNotExists(self.archive)
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.save().exit()
        self.assertFileExists(self.archive)


    def test_02_add(self):
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.add(self.file1, self.file2)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        gt.save()
        self.assertFileExists(self.archive)
        list_value = mock_stdout.getvalue()
        self.assertNotEqual(len(list_value), 0)

        with self.assertRaises(ValueError):
            gt.add(self.file1, unique=True)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files = len(mock_stdout.getvalue().splitlines())
        gt.add(self.file1, update=True)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files_update = len(mock_stdout.getvalue().splitlines())
        gt.add(self.file1)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            gt.list()
        num_files_append = len(mock_stdout.getvalue().splitlines())
        self.assertEqual(num_files, num_files_update)
        self.assertNotEqual(num_files_update, num_files_append)

    def test_03_extract(self):
        gt = Targpg(self.archive, passfile=self.passfile, autocreate=True)
        gt.add(self.file1, self.file2)
        gt.extract(self.file1, outdir=self.extr)
        self.assertFileExists(Path(self.extr, self.file1))

        with patch("builtins.input", return_value="1") as mock_input:
            gt.extract(outdir=self.extr)
        self.assertFileExists(Path(self.extr, self.file2))
