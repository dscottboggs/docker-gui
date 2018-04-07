#!/usr/bin/env python3
from container_gui.distros import getdistro
test_input = {
    "package": "x11-apps",
    "application": "xeyes",
    "distro": getdistro("ubuntu", "16.04"),
}

from yaml import dump
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import environ as local_environment
from os import getuid, getgid
from os import makedirs as mkdir
from os import F_OK as file_exists
from os import access
from textwrap import dedent
from pystache import render
from docker import DockerClient
from docker.types import Mount
from os import uname
from re import search
from subprocess import run, PIPE

runcmd = lambda cmd: run(cmd, check=True, shell=True, stdout=PIPE, stdin=PIPE)
sysinfo = uname()

if not sysinfo.sysname=='Linux':
    raise(NotImplementedError(f"Your system, {sysinfo.sysname}, has not been implemented yet"))

class Config():
    dc = DockerClient('unix://run/docker.sock', version='1.30')
    network_name = "docker_application_network"
    try:
        application_network = dc.networks.list(names=[network_name])[0]
    except IndexError:
        application_network = dc.networks.create(network_name)
    log=print
    kernel_version_match = search('\d\.\d\d?', sysinfo.release)
    kernel_version = sysinfo.release[
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

def check_isdir(filepath:str):
    if not isdir(filepath):
        if access(filepath, mode=file_exists):
            raise FileExistsError("Goal directory {filepath} exists as a file.")
        else:
            mkdir(filepath, mode=0o755)
            return True
    return False

class Application():
    """An application to deploy"""
    def __init__(self, package: str, application: str, distro: str, version: str=''):
        if not type('')==type(package)==type(application)==type(distro)==type(version):
            raise TypeError(dedent(f"""
                One of the following attributes was not a string:
                  - package {package} (type {type(package)})
                  - application {application} (type {type(application)})
                  - distro {distro} (type {type(distro)})
                  - version {version} (type {type(version)})"""))
        self.package = package
        self.application = application
        self.distro = getdistro(distro, version)
        self.image_name = f"img_{self.application}_in_{self.distro.image}_{self.distro.version}"
        self.container_name = self.image_name[4:]
        if Config.kernels.index(self.distro.kernel_version) > Config.kernel_index:
            print(
                "Warning! This application was packaged for kernel version",
                self.distro.kernel_version,
                "but this system uses",
                f'{Config.kernel_version}.',
                "you have 10 seconds to cancel this installation, or you can",
                "continue with the installation. It may work, despite this",
                "issue."
            )
            count=10
            while count>0:
                print(count, "seconds.")
                sleep(1)
        self.init_files()
        self.write_desktop_file()

    def run(self):
        if Config.dc.containers.list(all=True, filters={'name': self.container_name }):
            #an empty list is falsy and will skip this block
            if Config.dc.containers.list(filters={'name': self.container_name }):
                print("Application is already running!")
                return
            for container in docker.containers.list(
                        all=True,
                        filters={'name': self.container_name }
                    ):
                Config.dc.api.remove_container(
                    container
                )
        if not Config.dc.images.list(name=self.image_name):
            self.build()
        Config.dc.containers.run(
            image=self.image_name,
            devices=[
                "/dev/snd:/dev/snd:rw",
                "/dev/dri:/dev/dri:rw",
                "/dev/video0:/dev/video0:rw"
            ],
            mounts=[
                Mount(
                    source="/tmp/.X11-unix",
                    target="/tmp/.X11-unix",
                    type='bind'
                )
            ],
            environment={
                'DISPLAY': local_environment['DISPLAY']
            },
            networks=[Config.application_network],
            remove=True
        )


    def write_run_script(self):
        with open(self.run_script_file, 'w') as run_script_file:
            with open(getpath(
                        self.working_directory, "runscript.pytemplate"
                    )) as run_script_template:
                run_script_file.write(render(
                    text=run_script_template,
                    context={
                        'application_directory': self.application_directory,
                        'image_name': self.image_name,
                        'container_name': self.container_name
                    }
                ))

    def init_files(self):
        self.working_directory = getpath('/', 'usr', 'share', 'docker-gui')
        check_isdir(self.working_directory)
        with open(
                    getpath(
                        self.working_directory,
                        "Dockerfile.pytemplate"
                    ),
                    'r'
                ) as dockerfile:
            self.dockerfile_template = dockerfile.read()
        self.application_directory = getpath(
            self.working_directory,
            self.application
        )
        check_isdir(self.application_directory)
        self.run_script_file = getpath(
                    self.application_directory, f"run_{self.application}"
                )

    def write_desktop_file(self):
        try:
            desktop_file = open(getpath(
                    '/',
                    'usr',
                    'share',
                    'applications',
                    "%s.docker.desktop" % test_input['application']
                ),
                'w'
            )
        except PermissionError:
            runcmd("""sudo su -c 'echo "{0}" > "{1}" && chown {2}:{3} {1}'""".format(
                dedent(f"""
                        [Desktop Entry]
                        Version=From {self.distro.distro}
                        Name={self.application}
                        Exec={self.run_script_file}
                        Terminal=false
                        Type=Application
                        Categories=Containerized
                        """
                ),
                getpath(
                    '/',
                    'usr',
                    'share',
                    'applications',
                    "%s.docker.desktop" % test_input['application']
                ),
                os.getuid(),
                os.getgid()
            ))
        desktop_file.write(dedent(f"""
                [Desktop Entry]
                Version=From {self.distro.distro}
                Name={self.application}
                Exec={self.run_script_file}
                Terminal=false
                Type=Application
                Categories=Containerized
                """
        ))

    def build(self):
        """Builds a docker image for the specified environment."""
        self.render_dockerfile()
        Config.dc.images.build(
            path=self.application_directory,
            tag=self.image_name
        )

    def render_dockerfile(self):
        self.final_dockerfile = render(
            template=self.dockerfile_template,
            context={
                'package': self.package,
                'application': self.application,
                'distro': self.distro,
                'uid': getuid(),
                'gid': getgid()
            }
        )
        with open(getpath(
                    self.application_directory, "Dockerfile"
                ),'w') as dockerfile:
            dockerfile.write(self.final_dockerfile)
