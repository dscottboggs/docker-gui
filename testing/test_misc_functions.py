#!/usr/bin/env python3.6
"""Tests for the functions in misc_functions.py."""
from os import remove, removedirs
from os.path import isdir
from pytest import raises
from subprocess import CalledProcessError

from container_gui.misc_functions import check_isdir, runcmd


class Test_MiscFunctions():
    """Tests for the functions in misc_functions.py."""
    def test_runcmd(self):
        """Make sure the runcmd function works right."""
        with raises(CalledProcessError):
            runcmd("invalid shell command")
        assert runcmd("echo a test phrase").stdout.decode()\
            == "a test phrase\n",\
            "Running a command resulted in the wrong output"

    def test_check_isdir_function(self):
        """Make sure the check_isdir function works properly."""
        with raises(FileExistsError):
            open("/tmp/testfile", 'w').close()
            check_isdir("/tmp/testfile")
            remove("/tmp/testfile")

        check_isdir("/tmp/testdir")
        assert isdir("/tmp/testdir"), \
            "check_isdir failed. Check out /tmp/testdir to see why."
        removedirs("/tmp/testdir")
