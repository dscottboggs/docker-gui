#!/usr/bin/env python3
"""The list of available distributions to work with this system."""
from sys import maxsize
from textwrap import dedent
is_64bit = maxsize > 2**32  # check if arch is amd64, see https://stackoverflow.com/questions/9964396/python-check-if-a-system-is-32-or-64-bit-to-determine-whether-to-run-the-funct#9964440
distros = []


class Distro():
    """Hold various distro-specific commands.

    This should contain the image tag to pull, and any package manager
    commands.

      - @param distro [str]: A readable version of the name of the distro.
      - @param image [str]: the image tag to be used for docker
      - @param version [str]: the version of the image to pull
      - @param pkgs_refresh [str]: the command to run to refresh the package
                                   repos.
      - @param pkgs_install [str]: the command that the pkgs_install function
                                   will need to return in order to install
                                   packages on this particular distro.
      - @param pkgs_update [str]: the command to run to update out-of-date
                                   packages
    """
    def __init__(
                self, image: str, version: str, pkgs_update: str,
                pkgs_install: str, pkgs_refresh: str, kernel_version: str,
                distro=None
            ):
        """Init a Distro."""
        if not type('') == type(image) == type(version) == type(pkgs_update)\
                == type(pkgs_install) == type(pkgs_refresh)\
                == type(kernel_version):
            raise TypeError(dedent(f"""
                One of the following was not a string:
                  - image: {image} (type {type(image)})
                  - version: {version} (type {type(version)})
                  - pkgs_update: {pkgs_update} (type {type(pkgs_update)})
                  - pkgs_install: {pkgs_install} (type {type(pkgs_install)})
                  - pkgs_refresh: {pkgs_refresh} (type {type(pkgs_refresh)})
                  - kernel_version: {kernel_version} (type {type(kernel_version)})
                  """))
        self.image = image.lower()
        self.version = version.lower()
        self.pkgs_update = pkgs_update
        self.pkgs_install = pkgs_install
        self.pkgs_refresh = pkgs_refresh
        self.distro = distro if distro is not None else\
            f"{image.capitalize()}, version {version.lower()}"
        self.kernel_version = kernel_version

distros += [
    Distro(
        image=distro,
        version=version,
        pkgs_update='apt-get upgrade -y',
        pkgs_install='apt-get install -y',
        pkgs_refresh='apt-get update',
        kernel_version=kern
    ) for distro, version, kern in (
        ('ubuntu', '14.04', '3.13'),
        ('ubuntu', '16.04', '4.4'),
        ('ubuntu', 'latest', '4.4'),
        ('ubuntu', '17.10', '4.13'),
        ('debian', 'oldstable', '3.16'),
        ('debian', 'stable', '4.9'),
        ('debian', 'testing', '4.15'),
        ('debian', 'unstable', '4.15'),
        ('debian', 'latest', '4.9'),

    )
]

distros += [
    Distro(
        image=distro,
        version=version,
        pkgs_refresh='true',             # not necessary for this distro, pass.
        pkgs_install='yum install -y',
        pkgs_update='yum upgrade -y',
        kernel_version=kern
    ) for distro, version, kern in [
        ('centos', '7', '3.10'),
        ('centos', 'latest', '3.10'),
        ('centos', '6', '2.6'),
        ('centos', "7.4.1708", '3.10'),
        ('centos', "7.3.1611", '3.10'),
        ('centos', '7.2.1511', '3.10'),
        ('centos', '7.1.1503', '3.10'),
        ('centos', '7.0.1406', '3.10'),
        ('centos', '6.9', '2.6'),
        ('centos', '6.8', '2.6'),
        ('centos', '6.7', '2.6'),
        ('centos', '6.6', '2.6'),
        ('fedora', '27', '4.13'),
        ('fedora', '26', '4.11'),
        ('fedora', 'rawhide', '4.15'),
        ('fedora', 'latest', '4.13')
    ]
]
distros.append(
    Distro(
        image='antergos/archlinux-base-devel',
        version='latest',
        pkgs_refresh='true',            # install/update also do refresh (pass)
        pkgs_install='pacman -Sy',
        pkgs_update='pacman -Syu',
        kernel_version='4.9',                                         # minimum
        distro='Arch Linux (Antergos)'
    )
)

distros += [
    Distro(
        image="opensuse/amd64",
        distro="OpenSUSE",
        version=version,
        pkgs_refresh='zypper --non-interactive refresh',
        pkgs_install='zypper --non-interactive install',
        pkgs_update='zypper --non-interactive update',
        kernel_version=kern
    ) for version, kern in (
        ('leap', '4.4'),
        ('tumbleweed', '4.15'),
        ('latest', '4.4')
    )
]


def getdistro(distroname: str, version: str='') -> Distro:
    """Find the appropriate distro in the list and return it."""
    _version = version or "latest"
    for distro in distros:
        if distro.image == distroname.lower()\
                and distro.version == _version.lower():
            return distro
    else:
        raise ValueError(
            "%s:%s is not a valid distro." % (distroname, version)
        )
