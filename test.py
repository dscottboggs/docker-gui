from distros import Distro
from textwrap import dedent
from pytest import raises
class TestDistroClass():
    distro_image = "invalid"
    distro_version = "distro"
    distro_update_cmd = "this isn't"
    distro_install_cmd = "a real"
    distro_refresh_cmd = 'distribution or anything'
    def get_test_distro(self):
        return Distro(
            self.distro_image,
            version=self.distro_version,
            pkgs_update=self.distro_update_cmd,
            pkgs_install=self.distro_install_cmd,
            pkgs_refresh=self.distro_refresh_cmd
        )
    def test_init(self):
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
        assert self.get_test_distro().image == self.distro_image, \
            f"Image name not set right, {self.get_test_distro().image}"
    def test_version(self):
        assert self.get_test_distro().version == self.distro_version, \
            f"Version name not set right, {self.get_test_distro().version}"
    def test_distro_desc(self):
        assert self.get_test_distro().distro == \
            f"{self.distro_image.capitalize()}, version {self.distro_version}", \
            f"Distro description not set right, {self.get_test_distro().distro}"
    def test_pkgs_update(self):
        assert self.get_test_distro().pkgs_update == self.distro_update_cmd,\
            f"Packages update command not set right, {self.get_test_distro().update}"
    def test_pkgs_install(self):
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
        assert self.get_test_distro().pkgs_refresh == self.distro_refresh_cmd,\
            f"Packages refresh command not set right, {self.get_test_distro().pkgs_refresh}"
