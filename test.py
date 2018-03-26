from distros import Distro, getdistro
from deploy import Application, check_isdir
from textwrap import dedent
from pytest import raises
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import remove, removedirs
from os import environ as local_environment
from os import makedirs as mkdir

class TestApplicationClass():
    """Tests for the Application class."""
    this.package_name = "invalid"
    this.application_name = "application"
    this.distro = "ubuntu"
    this.version = "16.04"
    def get_test_application():
        """Retrieve a test Application object"""
        Application(
            package=this.package_name,
            application=this.application_name,
            distro=this.distro,
            version=this.version
        )
    def test_init_types(self):
        with raises(TypeError):
            Application(
                package=["can't", 'put', 'it in a list'],
                application=this.application_name,
                distro=this.distro,
                version=this.distro_version
            )
        with raises(TypeError):
            Application(
                package=this.package_name,
                application=["can't", 'put', 'it in a list'],
                distro=this.distro,
                version=this.distro_version
            )
        with raises(TypeError):
            Application(
                package=this.package_name,
                application=this.application_name,
                distro=["can't", 'put', 'it in a list'],
                version=this.distro_version
            )
        with raises(TypeError):
            Application(
                package=this.package_name,
                application=this.application_name,
                distro=this.distro,
                version=10  # must be a string not a number
            )
    def test_package_name():
        assert get_test_application().package == this.package_name, \
            f"Package name not set right, {get_test_application().package}"
    def test_application_name(self):
        assert get_test_application().package == this.package_name, \
            f"Application name not set right, {get_test_application().application}"
    def test_distro(self):
        with raises(ValueError):
            Application(
                package=this.package_name,
                application=this.application_name,
                distro="invalid distro"
            )
        with raises(ValueError):
            Application(
                package=this.package_name,
                application=this.application_name,
                distro=this.distro,
                version="Invalid version"
            )
        assert get_test_application().distro.pkgs_update == "apt-get upgrade -y"

    def test_files(self):
        testapp = get_test_application()
        with raises(FileExistsError):
            open("/tmp/testfile",'w').close()
            check_isdir("/tmp/testfile")
            remove("/tmp/testfile")
        check_isdir("/tmp/testdir")
        assert isdir("/tmp/testdir"), "check_isdir failed. Check out /tmp/testdir to see why."
        removedirs("/tmp/testdir")
        assert isdir(testapp.working_directory),\
            "Application's working directory doesn't exist."
        assert testapp.working_directory=="/usr/share/docker-gui",
            f"The working directory was incorrectly named: {testapp.working_directory}"
        assert isdir(testapp.application_directory),\
            "Application's storage directory doesn't exist."
        assert testapp.application_directory==\
            f"/usr/share/docker-gui/{self.application_name}",\
            f"Application's storage directory was named incorrectly: {self.application_name}"

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
        assert getdistro("DEBIAN", "STABLE").image="debian"
    def test_version(self):
        """check the that version label was set correctly"""
        assert self.get_test_distro().version == self.distro_version, \
            f"Version name not set right, {self.get_test_distro().version}"
        assert getdistro("DEBIAN", "STABLE").version="stable"
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
