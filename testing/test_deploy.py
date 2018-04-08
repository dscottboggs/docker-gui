#!/usr/bin/env python3.6
"""Contains tests for the code in the "container_gui/deploy.py" file."""
from container_gui.deploy import Application
from textwrap import dedent
from pytest import raises
from os.path import isdir
from os.path import join as getpath


class TestApplicationClass():
    """Tests for the Application class."""
    package_name = "x11-apps"
    application_name = "xeyes"
    distro = {'name': "ubuntu", 'version': "16.04"}

    def get_test_application(self):
        """Retrieve a test Application object."""
        return Application(
            package=self.package_name,
            application=self.application_name,
            distro=self.distro['name'],
            version=self.distro['version']
        )

    def test_init_types(self):
        """Make sure that putting the wrong type of data throws an error.

        The checks are for the Application constructor.
        """
        with raises(TypeError):
            Application(
                package=["can't", 'put', 'it in a list'],
                application=self.application_name,
                distro=self.distro['name'],
                version=self.distro['version']
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=["can't", 'put', 'it in a list'],
                distro=self.distro['name'],
                version=self.distro['version']
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro=["can't", 'put', 'it in a list'],
                version=self.distro['version']
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro=self.distro['name'],
                version=10  # must be a string not a number
            )

    def test_package_name(self):
        """Check that setting the package name works right."""
        assert self.get_test_application().package == self.package_name, \
            dedent(f"""
                Package name not set right,
                {self.get_test_application().package}"""
            )

    def test_application_name(self):
        """Check that setting the application name works right."""
        assert self.get_test_application().package == self.package_name, \
            dedent(f"""
                Application name not set right,
                {self.get_test_application().application}"""
            )

    def test_distro(self):
        """Check that setting the distribution name works right."""
        with raises(ValueError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro="invalid distro"
            )
        with raises(ValueError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro=self.distro['name'],
                version="Invalid version"
            )
        assert self.get_test_application().distro.pkgs_update == \
            "apt-get upgrade -y"

    def test_directories(self):
        """Make sure the directories created during installation exist.

        Also contains checks for the content.
        """
        testapp = self.get_test_application()

        assert isdir(testapp.working_directory),\
            "Application's working directory doesn't exist."
        assert testapp.working_directory == "/usr/share/docker-gui",\
            dedent(f"""
                The working directory was incorrectly named:
                {testapp.working_directory}"""
            )
        assert isdir(testapp.application_directory),\
            "Application's storage directory doesn't exist."
        assert testapp.application_directory == \
            f"/usr/share/docker-gui/{self.application_name}",\
            dedent(f"""
                Application's storage directory was named incorrectly:
                {self.application_name}"""
            )

    def test_desktop_file(self):
        """Make sure the desktop file for the test application exists.

        Checks the content too.
        """
        test_desktop_file = dedent(f"""
            [Desktop Entry]
            Version=From {self.distro['name'].capitalize()}, version {self.distro['version']}
            Name={self.application_name}
            Exec={getpath(self.get_test_application().application_directory, f"run_{self.application_name}")}
            Terminal=false
            Type=Application
            Categories=Containerized
            """)
        with open(getpath(
                    '/',
                    'usr',
                    'share',
                    'applications',
                    f"run_{self.application_name}"
                ), 'r') as desktop_file:
            assert desktop_file.read() == test_desktop_file, dedent(f"""
                Desktop file should've been {test_desktop_file} but it was/is
                {desktop_file.read()}"""
            )
