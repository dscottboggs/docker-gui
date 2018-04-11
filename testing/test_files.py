"""Tests for files that should be present after setup."""
from os import access
from os.path import isdir
from os.path import join as build_path
from os import F_OK as FILE_EXISTS
from os import R_OK as FILE_IS_READABLE
from os import W_OK as FILE_IS_WRITABLE
from os import X_OK as FILE_IS_EXECUTABLE
from hashlib import sha256


class TestFiles():
    """Tests for files that should be present after setup."""
    BASE_DIR = build_path('/', 'usr', 'share', 'docker-gui')

    def test_base_folder(self):
        """Check for the base directory."""
        assert access(self.BASE_DIR, FILE_EXISTS), "Base dir doesn't exist"
        assert isdir(self.BASE_DIR), "Base dir {}.".format(
            "is a file, when it's supposed to be a directory" if access(
                self.BASE_DIR, FILE_EXISTS
            ) else "doesn't exist"
        )
        assert access(
                self.BASE_DIR,
                FILE_IS_WRITABLE | FILE_IS_EXECUTABLE
            ), "Permissions aren't right on base dir"

    def test_Dockerfile_template(self):
        """Check the location and content of Dockerfile.pytemplate."""
        assert access(
            build_path(self.BASE_DIR, "Dockerfile.pytemplate"),
            FILE_IS_READABLE
        ), "Can't access Dockefile template"
        template_file = open(
            build_path(self.BASE_DIR, 'Dockerfile.pytemplate')
        )
        assert sha256(template_file.read().encode('ascii')).hexdigest()\
            == '941b7c1d387604aca8ba8bba166e70b764d82b4c9329824c7128bf75f22497e0',\
            "Dockerfile template file contents are wrong"
        template_file.close()

    def test_runscript_template(self):
        """Check the location & content of the template for the run script."""
        assert access(
            build_path(self.BASE_DIR, "runscript.pytemplate"), FILE_IS_READABLE
        ), "Can't find the runscript template"
        template_file = open(build_path(self.BASE_DIR, "runscript.pytemplate"))
        assert sha256(template_file.read().encode('ascii')).hexdigest()\
            == 'df42d02d957ef5ef0f7aaa5adda7fc1bbca12101c40451c35ff9769b2e5b7c1c',\
            "Runscript contents are wrong."
        template_file.close()
