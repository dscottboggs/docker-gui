from os import access
from os.path import isdir
from os.path import join as build_path
from os import F_OK as FILE_EXISTS
from os import R_OK as FILE_IS_READABLE
from os import W_OK as FILE_IS_WRITABLE
from os import X_OK as FILE_IS_EXECUTABLE
from hashlib import sha256

class TestFiles():
    BASE_DIR = build_path('/', 'usr', 'share', 'docker-gui')
    def test_base_folder(self):
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
        assert access(
            build_path(self.BASE_DIR, "Dockerfile.pytemplate"),
            FILE_IS_READABLE
        ), "Can't access Dockefile template"
        template_file = open(
            build_path(self.BASE_DIR, 'Dockerfile.pytemplate')
        )
        assert sha256(template_file.read().encode('ascii')).hexdigest()\
            == '451d8484ffdeb00c350c06dfcea4239f588b5408bf95a2d349c40f3da3cf758f',\
            "Dockerfile template file contents are wrong"
        template_file.close()
    def test_runscript_template(self):
        assert access(
            build_path(self.BASE_DIR, "runscript.pytemplate"), FILE_IS_READABLE
        ), "Can't find the runscript template"
        template_file = open(build_path(self.BASE_DIR, "runscript.pytemplate"))
        assert sha256(template_file.read().encode('ascii')).hexdigest()\
            == '203717a49d5a918a3bd789defe02685d1473377523f82631a0200f023ef3675a',\
            "Runscript contents are wrong."
