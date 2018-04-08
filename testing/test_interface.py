#!/usr/bin/env python3
"""Testing for the CLI interface."""
from textwrap import dedent
from pytest import raises
from os.path import join as getpath
from os import dirname, realpath
from subprocess import run, PIPE, CalledProcessError


class TestCLI():
    """Testing for the CLI interface."""
    shell_enabled = True
    cli_filename = getpath(dirname(realpath(__file__)).rsplit(
        '/', maxsplit=1)[0], "container_gui", "cli.py"
    )

    def test_build(self):
        """Check that the build command works."""
        run(
            f'{self.cli_filename} build x11-apps from Ubuntu version 16.04 launched-with xeyes',
            stdout=PIPE,
            check=True,
            shell=self.shell_enabled
        )

    def test_run(self):
        """Check that the run command works."""
        run(
            [
                f'{self.cli_filename} run x11-apps from ubuntu version 16.04 launched-with xeyes',
            ],
            stdout=PIPE,
            check=True,
            shell=self.shell_enabled
        )

    def test_invalid(self):
        """Try some invalid commands."""
        with raises(CalledProcessError):
            run(
                [
                    f'{self.cli_filename} wrong input',
                ],
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )
        with raises(CalledProcessError):
            run(
                f'{self.cli_filename} run invalid args but not all',
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )
        with raises(CalledProcessError):
            run(
                f'{self.cli_filename} run valid from up until here invalid now',
                stdout=PIPE,
                check=True,
                shell=self.shell_enabled
            )

    def test_usage_command(self):
        """Get the usage information with a command."""
        assert run(
                f'{self.cli_filename} usage',
                stdout=PIPE,
                shell=self.shell_enabled
            ).stdout.decode() == dedent("""
                Run a GUI program in a docker container.

                Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO [ version DISTRO_VERSION ] launched-with APPLICATION_NAME
                """)
