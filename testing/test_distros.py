from container_gui.distros import Distro, getdistro
from textwrap import dedent
from pytest import raises
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import remove, removedirs
from os import environ as local_environment
from os import makedirs as mkdir
from subprocess import run, PIPE, CalledProcessError

class TestDistroClass():
    distro_image = "invalid"
    distro_version = "distro"
    distro_update_cmd = "th1s iS n-t"
    distro_install_cmd = "a --rEal"
    distro_refresh_cmd = 'dist-ribUTi0n or anything'
    distro_kernel_version = 'fakekernel'
    def get_test_distro(self):
        """A distro object to work with."""
        return Distro(
            self.distro_image,
            version=self.distro_version,
            pkgs_update=self.distro_update_cmd,
            pkgs_install=self.distro_install_cmd,
            pkgs_refresh=self.distro_refresh_cmd,
            kernel_version=self.distro_kernel_version
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
