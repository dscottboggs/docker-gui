import os
from subprocess import run, PIPE
from setuptools import setup

runcmd = lambda cmd: run(cmd, check=True, shell=True, stdout=PIPE)

if not os.access('/usr/share/docker-gui', os.W_OK|os.X_OK) or not os.path.isdir('/usr/share/docker-gui'):
    runcmd(f"sudo mkdir -p /usr/share/docker-gui && sudo chown {os.getuid()}:{os.getgid()} /usr/share/docker-gui")

os.link(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "container_gui",
        "runscript.pytemplate"
    ),
    os.path.join('/', 'usr', 'share', 'docker-gui', 'runscript.pytemplate')
)

os.link(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "container_gui",
        "Dockerfile.pytemplate"
    ),
    os.path.join('/', 'usr', 'share', 'docker-gui', 'Dockerfile.pytemplate')
)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Containerize_GUI_Applications",
    version = "0.0.1",
    author = "D. Scott Boggs",
    author_email = "scott@tams.tech",
    description = "A quick way to run an application from another distribution.",
    license = "GPLv3",
    keywords = "Containerization x11 xserver",
    url = "https://github.com/dscottboggs/docker-gui",
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
