"""A setuptools setup for this system."""
from os import getuid, getgid, access, chown
from os.path import join as getpath
from os.path import realpath, dirname, isdir
from os import W_OK as is_writable
from os import X_OK as is_executable
from setuptools import setup
from container_gui.misc_functions import runcmd
from shutil import copy
from pwd import getpwnam as get_user
from pwd import struct_passwd as LocalUser

def get_desired_user() -> LocalUser:
    """Ask the user who should own the installation.

    This is necessary because the setup script has to be run as root, but the
    user may desire the installation script and installed applications to be
    owned by a different user.
    """
    desired_user = input(
        "What is the username of the user who should own the scripts and files?"
        "This should be your username if you intend to use the installed"
        "applications or the installation script."
    )
    try:
        return get_user(desired_user)
    except KeyError:
        print("User", desired_user, "not found.")
        return get_desired_user()
user = get_desired_user()

if not access('/usr/share/docker-gui', is_writable | is_executable)\
        or not isdir('/usr/share/docker-gui'):
    runcmd(f"sudo mkdir -p /usr/share/docker-gui && sudo chown {user.pw_uid}:{user.pw_gid} /usr/share/docker-gui")
try:
    copy(
        getpath(
            dirname(realpath(__file__)),
            "container_gui",
            "runscript.pytemplate"
        ),
        getpath('/', 'usr', 'share', 'docker-gui', 'runscript.pytemplate')
    )
except FileExistsError:
    pass
chown(
    path=getpath('/', 'usr', 'share', 'docker-gui', 'runscript.pytemplate'),
    uid=user.pw_uid,
    gid=user.pw_gid
)
try:
    copy(
        getpath(
            dirname(realpath(__file__)),
            "container_gui",
            "Dockerfile.pytemplate"
        ),
        getpath('/', 'usr', 'share', 'docker-gui', 'Dockerfile.pytemplate')
    )
except FileExistsError:
    pass
chown(
    path=getpath('/', 'usr', 'share', 'docker-gui', 'Dockerfile.pytemplate'),
    uid=user.pw_uid,
    gid=user.pw_gid
)

with open(
            getpath('/home/scott/Documents/code/docker-gui/container_gui/config.py'),
            'a'
        ) as config:
    config.write("    user = %s\n    group = %s\n" % (user.pw_uid, user.pw_gid))

def read(*fname: str) -> str:
    """Get the contents of a file in the current directory."""
    return open(getpath(dirname(__file__), *fname)).read()


setup(
    name="Containerize_GUI_Applications",
    version="0.1.0",
    author="D. Scott Boggs",
    author_email="scott@tams.tech",
    description="A quick way to run an application from another distribution.",
    license="GPLv3",
    keywords="Containerization x11 xserver",
    url="https://github.com/dscottboggs/docker-gui",
    packages=['container_gui', 'testing'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Containerization",
        "License :: OSI Approved :: GPLv3",
    ],
    install_requires=[
        "jinja2",
        "docker"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
