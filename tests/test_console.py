#!/usr/bin/python3
"""
Contains the TestConsoleDocs class for testing documentation
"""

import console
import inspect
import pep8
import unittest
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for verifying the documentation of the console"""
    def test_pep8_conformance_console(self):
        """Check if console.py conforms to PEP8 standards."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "PEP8 style violations found in console.py.")

    def test_pep8_conformance_test_console(self):
        """Check if tests/test_console.py conforms to PEP8 standards."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "PEP8 style violations found in tests/test_console.py.")

    def test_console_module_docstring(self):
        """Verify the presence and length of the console.py module docstring."""
        self.assertIsNot(console.__doc__, None,
                         "The console.py module requires a docstring.")
        self.assertTrue(len(console.__doc__) >= 1,
                        "The console.py module docstring should be at least one character long.")

    def test_HBNBCommand_class_docstring(self):
        """Verify the presence and length of the HBNBCommand class docstring."""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "The HBNBCommand class requires a docstring.")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "The HBNBCommand class docstring should be at least one character long.")

