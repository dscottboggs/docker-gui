#!/usr/bin/env python3
from textwrap import dedent
from pytest import raises
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import remove, removedirs
from os import environ as local_environment
from os import makedirs as mkdir
from subprocess import run, PIPE, CalledProcessError

class TestCLI():
    """Testing for the CLI interface"""
    shell_enabled = True
    def test_build(self):
        run(
            [
                f'{getpath(dirname(realpath(__file__)), "cli.py")} build x11-apps from Ubuntu version 16.04 launched-with xeyes',
            ],
            stdout=PIPE,
            check=True,
            shell=self.shell_enabled
        )
    def test_run(self):
        run(
            [
                f'{getpath(dirname(realpath(__file__)), "cli.py")} run x11-apps from ubuntu version 16.04 launched-with xeyes',
            ],
            stdout=PIPE,
            check=True,
            shell=self.shell_enabled
        )
    def test_invalid(self):
        with raises(CalledProcessError):
            run(
                [
                    f'{getpath(dirname(realpath(__file__)), "cli.py")} wrong input',
                ],
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )
        with raises(CalledProcessError):
            run(
                f'{getpath(dirname(realpath(__file__)), "cli.py")} run invalid args but not all',
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )
        with raises(CalledProcessError):
            run(
                f'{getpath(dirname(realpath(__file__)), "cli.py")} run valid from up until here invalid now',
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )
        assert run(
                f'{getpath(dirname(realpath(__file__)), "cli.py")} usage',
                stdout=PIPE,
                shell=self.shell_enabled
            ).stdout.decode()==dedent("""
                Run a GUI program in a docker container.

                Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO [ version DISTRO_VERSION ] launched-with APPLICATION_NAME
                """)