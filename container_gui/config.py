from docker import DockerClient
from os import uname

class Config():
    if not uname().sysname=='Linux':
        raise(NotImplementedError(f"Your system, {uname().sysname}, has not been implemented yet"))
    dc = DockerClient('unix://run/docker.sock', version='1.30')
    network_name = "docker_application_network"
    try:
        application_network = dc.networks.list(names=[network_name])[0]
    except IndexError:
        application_network = dc.networks.create(network_name)
    kernel_version_match = find_pattern('\d\.\d\d?', uname().release)
    kernel_version = uname().release[
        self.kernel_version_match.start():self.kernel_version_match.end()
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
