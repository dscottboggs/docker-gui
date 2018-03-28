#!/usr/bin/env python3
from distros import Distro, getdistro
from deploy import Application, check_isdir
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
                f'{getpath(dirname(realpath(__file__)), "cli.py")} build x11-apps from ubuntu 16.04 launched with xeyes',
            ],
            stdout=PIPE,
            check=True,
            shell=self.shell_enabled
        )
    def test_run(self):
        run(
            [
                f'{getpath(dirname(realpath(__file__)), "cli.py")} run x11-apps from ubuntu 16.04 launched with xeyes',
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

                Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO version DISTRO_VERSION launched with APPLICATION_NAME
                """)

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

class TestDistroClass():
    distro_image = "invalid"
    distro_version = "distro"
    distro_update_cmd = "th1s iS n-t"
    distro_install_cmd = "a --rEal"
    distro_refresh_cmd = 'dist-ribUTi0n or anything'
    def get_test_distro(self):
        """A distro object to work with."""
        return Distro(
            self.distro_image,
            version=self.distro_version,
            pkgs_update=self.distro_update_cmd,
            pkgs_install=self.distro_install_cmd,
            pkgs_refresh=self.distro_refresh_cmd
        )
    def test_get_distro_function(self):
        with raises(ValueError):
            getdistro("nonsense", "bad version")
        assert getdistro("ubuntu", "16.04").pkgs_update == "apt-get upgrade -y"
    def test_init(self):
        """Test the actual __init__ function of the Distro class

        Checks for TypeErrors to be raised on invalid input."""
        with raises(TypeError):
            Distro()
        with raises(TypeError):
            Distro(
                ['invalid image attr'],
                version=self.distro_version,
                pkgs_update=self.distro_update_cmd,
                pkgs_install=self.distro_install_cmd,
                pkgs_refresh=self.distro_refresh_cmd
            )
        with raises(TypeError):
            Distro(
                self.distro_image,
                version=16.04, #versions must be numbers
                pkgs_update=self.distro_update_cmd,
                pkgs_install=self.distro_install_cmd,
                pkgs_refresh=self.distro_refresh_cmd
            )
        with raises(TypeError):
            Distro(
                self.distro_image,
                version=self.distro_version,
                pkgs_update=["invalid", "update", "cmd"],
                pkgs_install=self.distro_install_cmd,
                pkgs_refresh=self.distro_refresh_cmd
            )
        with raises(TypeError):
            Distro(
                self.distro_image,
                version=self.distro_version,
                pkgs_update=self.distro_update_cmd,
                pkgs_install= ["invalid"],
                pkgs_refresh=self.distro_refresh_cmd
            )
        with raises(TypeError):
            Distro(
                self.distro_image,
                version=self.distro_version,
                pkgs_update=self.distro_update_cmd,
                pkgs_install=self.distro_install_cmd,
                pkgs_refresh=["invalid"]
            )
    def test_image(self):
        """Check that the image name was set correctly."""
        assert self.get_test_distro().image == self.distro_image, \
            f"Image name not set right, {self.get_test_distro().image}"
        assert getdistro("DEBIAN", "STABLE").image == "debian"
    def test_version(self):
        """check the that version label was set correctly"""
        assert self.get_test_distro().version == self.distro_version, \
            f"Version name not set right, {self.get_test_distro().version}"
        assert getdistro("DEBIAN", "STABLE").version == "stable"
    def test_distro_desc(self):
        """check the that distro discription was set correctly"""
        assert self.get_test_distro().distro == \
            f"{self.distro_image.capitalize()}, version {self.distro_version}", \
            f"Distro description not set right, {self.get_test_distro().distro}"
    def test_pkgs_update(self):
        """check that the packages update command was set correctly"""
        assert self.get_test_distro().pkgs_update == self.distro_update_cmd,\
            f"Packages update command not set right, {self.get_test_distro().update}"
    def test_pkgs_install(self):
        """check that the packages install command was set correctly"""
        assert self.get_test_distro().pkgs_install("test package") \
            == f"{self.distro_install_cmd} test package",\
            dedent(f"\
                Packages install command not set right when passed as a \
                string, {self.get_test_distro().pkgs_install('test package')}."
            )
        assert self.get_test_distro().pkgs_install(["test","package"]) \
            == f"{self.distro_install_cmd} test package",\
            dedent(f"\
                Packages install command not set right when passed as a \
                list, {self.get_test_distro().pkgs_install('test package')}."
            )
        assert self.get_test_distro().pkgs_install( ("test", "package") ) \
            == f"{self.distro_install_cmd} test package",\
            dedent(f"\
                Packages install command not set right when passed as a \
                tuple, {self.get_test_distro().pkgs_install('test package')}."
            )
        with raises(AssertionError):
            self.get_test_distro().pkgs_install(['invalid', 'package name'])
        with raises(TypeError):
            self.get_test_distro().pkgs_install({'a wrongly-typed':'entry'})
    def test_pkgs_refresh(self):
        """check that the packages refresh command was set correctly"""
        assert self.get_test_distro().pkgs_refresh == self.distro_refresh_cmd,\
            f"Packages refresh command not set right, {self.get_test_distro().pkgs_refresh}"
