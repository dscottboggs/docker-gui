"""Config data for this particular system."""
from docker import DockerClient
from os import uname, sep
from os.path import join as getpath
from re import search as find_pattern


class Config():
    """Config data for this particular system.

    This currently includes the location of the local docker client and the
    local kernel version.
    """
    if not uname().sysname == 'Linux':
        raise(NotImplementedError(
            f"Your system, {uname().sysname}, has not been implemented yet"
        ))
    dc = DockerClient('unix://run/docker.sock', version='1.30')
    network_name = "docker_application_network"
    try:
        application_network = dc.networks.list(names=[network_name])[0]
    except IndexError:
        application_network = dc.networks.create(network_name)
    kernel_version_match = find_pattern('\d\.\d\d?', uname().release)
    kernel_version = uname().release[
        kernel_version_match.start():kernel_version_match.end()
    ]
    kernels = [
        '2.6',
        '3.10',
        '3.13',
        '3.16',
        '4.4',
        '4.9',
        '4.14',
        '4.15'
    ]
    kernel_index = kernels.index(kernel_version)
    dockerfile_template = getpath(
        sep,
        "usr",
        "share",
        "docker-gui",
        "Dockerfile.pytemplate"
    )
    runscript_template = getpath(
        sep,
        "usr",
        "share",
        "docker-gui",
        "runscript.pytemplate"
    )
    user = 1000
    group = 1000
    user = 1000
    group = 1000
