from json import dumps
from sys import maxsize
from textwrap import dedent
is_64bit = maxsize > 2**32  #check if arch is amd64, see https://stackoverflow.com/questions/9964396/python-check-if-a-system-is-32-or-64-bit-to-determine-whether-to-run-the-funct#9964440
distros = []

class Distro():
    """This object should hold various distro-specific commands.

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
      - @atrr pkgs_install [function]: a function that accepts a package
                                        name (as a string), or a list of package
                                        names (as a list or space-separated in
                                        a string) and returns the command used
                                        to install those packages for this
                                        distribution.
      - @param pkgs_update [str]: the command to run to update out-of-date
                                   packages
      """
    def __init__(self, image: str, version:str, pkgs_update: str,
            pkgs_install: str, pkgs_refresh: str, distro=None):
        self.image = image
        self.version = version
        self.pkgs_update = pkgs_update
        self.pkgs_install = lambda pkg: self._install(pkgs_install, pkg)
        self.pkgs_refresh = pkgs_refresh
        self.distro = distro if distro is not None else f"{image.capitalize()}, version {version}"
    @staticmethod
    def _install(cmd, pkg):
        if type(pkg) == type(''):
            return "%s %s" % (cmd, pkg)
        elif type(pkg) == type([]) or type(pkg) == type(tuple()):
            outstr = cmd
            for p in pkg:
                assert not ' ' in p, \
                    f"No spaces in package names! (package {p})"
                outstr += " %s"%(p)
            return outstr
        else:
            raise TypeError(
                "{} was not a string, tuple, or list, it was {}".format(
                    pkg, type(pkg)
                )
            )

distros.append(
    [
        Distro(
            image=distro,
            version=version,
            pkgs_update='apt-get upgrade -y',
            pkgs_install='apt-get install -y',
            pkgs_refresh='apt-get update'
        ) for distro, version in (
            ('ubuntu', '14.04'),
            ('ubuntu', '16.04'),
            ('ubuntu', '17.10'),
            ('debian', 'oldstable'),
            ('debian', 'stable'),
            ('debian', 'testing'),
            ('debian', 'experimental')
        )
    ]
)
distros.append(
    [
        Distro(
            image=distro,
            version=version,
            pkgs_refresh='true', # not necessary for this distro, pass.
            pkgs_install='yum install -y',
            pkgs_update='yum upgrade -y'
        ) for distro, version in [
            ('centos', '7'),
            ('centos', '6'),
            ('centos', "7.4.1708"),
            ('centos', "7.3.1611"),
            ('centos', '7.2.1511'),
            ('centos', '7.1.1503'),
            ('centos', '7.0.1406'),
            ('centos', '6.9'),
            ('centos', '6.8'),
            ('centos', '6.7'),
            ('centos', '6.6'),
            ('fedora', '27'),
            ('fedora', '26'),
            ('fedora', 'rawhide'),
            ('fedora', 'branched')
        ]
    ]
)
distros.append(
    Distro(
        image='antergos/archlinux-base-devel',
        version='latest',
        pkgs_refresh='true', # install/update also do refresh (pass)
        pkgs_install='pacman -Sy',
        pkgs_update='pacman -Syu',
        distro='Arch Linux (Antergos)'
    )
)

distros.append(
    [
        Distro(
            image="opensuse/amd64",
            distro="OpenSUSE",
            version=version,
            pkgs_refresh='zypper --non-interactive refresh',
            pkgs_install='zypper --non-interactive install',
            pkgs_update='zypper --non-interactive update'
        ) for version in ('leap', 'tumbleweed', 'latest')
    ]
)

def getdistro(distroname, version=None):
    getversion = lambda : version or "latest"
    for distro in distros:
        if distro['distro']==distroname and distro['version']==getversion():
            return distro
    else:
        raise ValueError("%s:%s is not a valid distro." % (distroname,version))
