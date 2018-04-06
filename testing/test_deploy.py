from container_gui.deploy import Application, check_isdir
from textwrap import dedent
from pytest import raises
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import remove, removedirs
from os import environ as local_environment
from os import makedirs as mkdir
from subprocess import run, PIPE, CalledProcessError

class TestApplicationClass():
    """Tests for the Application class."""
    package_name = "invalid"
    application_name = "application"
    distro = "ubuntu"
    distro_version = "16.04"
    def get_test_application(self):
        """Retrieve a test Application object"""
        return Application(
            package=self.package_name,
            application=self.application_name,
            distro=self.distro,
            version=self.distro_version
        )
    def test_init_types(self):
        with raises(TypeError):
            Application(
                package=["can't", 'put', 'it in a list'],
                application=self.application_name,
                distro=self.distro,
                version=self.distro_version
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=["can't", 'put', 'it in a list'],
                distro=self.distro,
                version=self.distro_version
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro=["can't", 'put', 'it in a list'],
                version=self.distro_version
            )
        with raises(TypeError):
            Application(
                package=self.package_name,
                application=self.application_name,
                distro=self.distro,
                version=10  # must be a string not a number
            )
    def test_package_name(self):
        assert self.get_test_application().package == self.package_name, \
            f"Package name not set right, {self.get_test_application().package}"
    def test_application_name(self):
        assert self.get_test_application().package == self.package_name, \
            f"Application name not set right, {self.get_test_application().application}"
    def test_distro(self):
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
                distro=self.distro,
                version="Invalid version"
            )
        assert self.get_test_application().distro.pkgs_update == "apt-get upgrade -y"

    def test_files(self):
        testapp = self.get_test_application()
        with raises(FileExistsError):
            open("/tmp/testfile",'w').close()
            check_isdir("/tmp/testfile")
            remove("/tmp/testfile")
        check_isdir("/tmp/testdir")
        assert isdir("/tmp/testdir"), "check_isdir failed. Check out /tmp/testdir to see why."
        removedirs("/tmp/testdir")
        assert isdir(testapp.working_directory),\
            "Application's working directory doesn't exist."
        assert testapp.working_directory=="/usr/share/docker-gui",\
            f"The working directory was incorrectly named: {testapp.working_directory}"
        assert isdir(testapp.application_directory),\
            "Application's storage directory doesn't exist."
        assert testapp.application_directory==\
            f"/usr/share/docker-gui/{self.application_name}",\
            f"Application's storage directory was named incorrectly: {self.application_name}"
    def test_desktop_file(self):
        test_desktop_file = dedent(f"""
            [Desktop Entry]
            Version=From {self.distro.capitalize()}, version {self.distro_version}
            Name={self.application_name}
            Exec={getpath(self.get_test_application().application_directory, f"run_{self.application_name}")}
            Terminal=false
            Type=Application
            Categories=Containerized
            """)
        with open(getpath(
                    '/','usr','share','applications', f"run_{self.application_name}"
                ), 'r') as desktop_file:
            assert desktop_file.read()==test_desktop_file, \
                f"Desktop file should've been {desktop_file.read()} but it {test_desktop_file}"
