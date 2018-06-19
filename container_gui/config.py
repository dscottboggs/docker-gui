"""Config data for this particular system."""
from docker import DockerClient
from os import uname, sep, environ as local_environment
from os.path import join as getpath
from re import search as find_pattern

local_share = getpath(local_environment['HOME'], ".local", "share")
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
    kernel_index = kernels.index(kernel_version)
    dockerfile_template = getpath(local_share
                                  "docker-gui",
                                  "Dockerfile.pytemplate")
    runscript_template = getpath(local_share
                                 "docker-gui",
                                 "runscript.pytemplate")
    user = 1000
    group = 1000
    user = 1000
    group = 1000
