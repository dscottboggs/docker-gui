"""Test the container_gui/distros.py file contents."""
from container_gui.distros import Distro, getdistro
from textwrap import dedent
from pytest import raises
from re import sub


class TestDistroClass():
    """Test the Distro class in container_gui/distros.py."""
    distro_image = "invalid"
    distro_version = "distro"
    distro_update_cmd = "th1s iS n-t"
    distro_install_cmd = "a --rEal"
    distro_refresh_cmd = 'dist-ribUTi0n or anything'
    distro_kernel_version = 'fakekernel'

    def get_test_distro(self) -> Distro:
        """Retrieve distro object to work with."""
        return Distro(
            self.distro_image,
            version=self.distro_version,
            pkgs_update=self.distro_update_cmd,
            pkgs_install=self.distro_install_cmd,
            pkgs_refresh=self.distro_refresh_cmd,
            kernel_version=self.distro_kernel_version
        )

    def test_init(self):
        """Test the actual __init__ function of the Distro class.

        Checks for TypeErrors to be raised on invalid input.
        """
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
                version=16.04,                       # versions must be numbers
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
                pkgs_install=["invalid"],
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
        """Check the that version label was set correctly."""
        assert self.get_test_distro().version == self.distro_version, \
            f"Version name not set right, {self.get_test_distro().version}"
        assert getdistro("DEBIAN", "STABLE").version == "stable"

    def test_distro_desc(self):
        """Check the that distro discription was set correctly."""
        assert self.get_test_distro().distro == \
            sub('\n', '', dedent(f"""
                {self.distro_image.capitalize()}, version
                 {self.distro_version}"""  # when "style" decreases readability
            )), dedent(f"""
                Distro description not set right,
                {self.get_test_distro().distro}"""
            )

    def test_pkgs_update(self):
        """Check that the packages update command was set correctly."""
        assert self.get_test_distro().pkgs_update == self.distro_update_cmd,\
            dedent(f"""
                Packages update command not set right,
                {self.get_test_distro().update}"""
            )

    def test_pkgs_install(self):
        """Check that the packages install command was set correctly."""
        assert self.get_test_distro().pkgs_install == self.distro_install_cmd,\
            "Packages install command wasn't set right."

    def test_pkgs_refresh(self):
        """Check that the packages refresh command was set correctly."""
        assert self.get_test_distro().pkgs_refresh == self.distro_refresh_cmd,\
            dedent(f"""
                Packages refresh command not set right,
                {self.get_test_distro().pkgs_refresh}"""
            )


class Test_get_distro_Function():
    """Make sure the "getdistro" function works right."""
    def test_get_distro_function(self):
        """Make sure the "getdistro" function works right."""
        with raises(ValueError):
            getdistro("nonsense", "bad version")
        assert getdistro("ubuntu", "16.04").pkgs_update == "apt-get upgrade -y"
