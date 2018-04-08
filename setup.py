"""A setuptools setup for this system."""
from os import isdir, getuid, getgid, access, link
from os.path import join as getpath
from os.path import realpath, dirname
from os import W_OK as is_writable
from os import X_OK as is_executable
from setuptools import setup
from container_gui.misc_functions import runcmd

if not access('/usr/share/docker-gui', is_writable | is_executable)\
        or not isdir('/usr/share/docker-gui'):
    runcmd(f"sudo mkdir -p /usr/share/docker-gui && sudo chown {getuid()}:{getgid()} /usr/share/docker-gui")
try:
    link(
        getpath(
            dirname(realpath(__file__)),
            "container_gui",
            "runscript.pytemplate"
        ),
        getpath('/', 'usr', 'share', 'docker-gui', 'runscript.pytemplate')
    )
except FileExistsError:
    pass
try:
    link(
        getpath(
            dirname(realpath(__file__)),
            "container_gui",
            "Dockerfile.pytemplate"
        ),
        getpath('/', 'usr', 'share', 'docker-gui', 'Dockerfile.pytemplate')
    )
except FileExistsError:
    pass


def read(*fname: str) -> str:
    """Get the contents of a file in the current directory."""
    return open(getpath(dirname(__file__), *fname)).read().decode()


setup(
    name="Containerize_GUI_Applications",
    version="0.0.1",
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
        "pystache",
        "docker"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
