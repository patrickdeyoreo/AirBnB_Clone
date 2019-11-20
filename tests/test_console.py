#!/usr/bin/python3
"""
Test console
"""

import unittest
from console import HBNBCommand
from os import chdir, getcwd, path
from pep8 import StyleGuide
from shutil import rmtree
from tempfile import mkdtemp


MODEL = path.join(getcwd(), 'console.py')


class TestConsole(unittest.TestCase):
    """
    Tests for console
    """
    def setUp(self):
        """
        Create a temporary directory and enter it
        """
        chdir(mkdtemp())

    def tearDown(self):
        """
        Remove temporary files and directories
        """
        rmtree(getcwd(), ignore_errors=True)

    def test_emptyline(self):
        """
        Test emptyline method
        """
        pass

    def test_do_help(self):
        """
        Test do_help method
        """
        pass

    def test_do_quit(self):
        """
        Test do_quit method
        """
        pass

    def test_do_EOF(self):
        """
        Test do_EOF method
        """
        pass

    def test_do_all(self):
        """
        Test do_all method
        """
        pass

    def test_do_count(self):
        """
        Test do_count method
        """
        pass

    def test_do_create(self):
        """
        Test do_create method
        """
        pass

    def test_do_destroy(self):
        """
        Test do_destroy method
        """
        pass

    def test_do_show(self):
        """
        Test do_show method
        """
        pass

    def test_do_update(self):
        """
        Test do_update method
        """
        pass

    def test_precmd(self):
        """
        Test precmd method
        """
        pass

    def test_pep8(self):
        """
        Test PEP8 conformance
        """
        style = StyleGuide(quiet=True)
        check = style.check_files([MODEL])
        self.assertEqual(check.total_errors, 0)
