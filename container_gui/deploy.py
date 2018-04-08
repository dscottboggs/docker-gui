#!/usr/bin/env python3
"""Functionality to perform a deployment of an application."""
from os.path import join as getpath
from os import environ as local_environment
from os import getuid, getgid

from textwrap import dedent
from pystache import render

from docker.types import Mount
from docker.containers import list as list_containers

from config import Config
from distros import getdistro
from time import sleep
from misc_functions import *


class Application():
    """An application to deploy."""
    def __init__(
                self,
                package: str,
                application: str,
                distro: str,
                version: str=''
            ):
        """Initialize and provide methods for acting on a given application."""
        if not type('') == type(package) == type(application) == type(distro) \
                == type(version):
            raise TypeError(dedent(f"""
                One of the following attributes was not a string:
                  - package {package} (type {type(package)})
                  - application {application} (type {type(application)})
                  - distro {distro} (type {type(distro)})
                  - version {version} (type {type(version)})"""))
        self.package = package
        self.application = application
        self.distro = getdistro(distro, version)
        self.image_name = "img_%s_in_%s_%s" % (
            self.application, self.distro.image, self.distro.version
        )
        self.container_name = self.image_name[4:]
        if Config.kernels.index(self.distro.kernel_version) \
                > Config.kernel_index:
            print(
                "Warning! This application was packaged for kernel version",
                self.distro.kernel_version,
                "but this system uses",
                f'{Config.kernel_version}.',
                "you have 10 seconds to cancel this installation, or you can",
                "continue with the installation. It may work, despite this",
                "issue."
            )
            count = 10
            while count > 0:
                print(count, "seconds.")
                sleep(1)
        self.init_files()

    def run(self):
        """Check that the application isn't already running and start it."""
        if Config.dc.containers.list(
                    all=True, filters={'name': self.container_name}
                ):
            # an empty list is falsy and will skip this block
            if Config.dc.containers.list(
                        filters={'name': self.container_name}
                    ):
                print("Application is already running!")
                return
            for container in list_containers(
                        all=True,
                        filters={'name': self.container_name}
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

    def init_files(self):
        """Write all the files to use this Application at a later time."""
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
        self.render_dockerfile()
        self.write_run_script()
        self.write_desktop_file()

    def write_run_script(self):
        """Write a script to run this application to a file."""
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

    def write_desktop_file(self):
        """Create the .desktop file for this Applicationself.

        Creating and storing this file in /usr/share/applications allows the
        user to run the application from their app menu or launcher.
        """
        try:
            desktop_file = open(getpath(
                    '/',
                    'usr',
                    'share',
                    'applications',
                    "%s.docker.desktop" % self.application_name
                ),
                'w'
            )
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
        except PermissionError:
            runcmd(dedent("""
                sudo su -c 'echo "{0}" > "{1}" && chown {2}:{3} {1}'
                """).format(
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
                        "%s.docker.desktop" % self.application_name
                    ),
                    getuid(),
                    getgid()
                )
            )
            self.write_desktop_file()

    def build(self):
        """Build a docker image for the specified environment."""
        self.render_dockerfile()
        Config.dc.images.build(
            path=self.application_directory,
            tag=self.image_name
        )

    def render_dockerfile(self):
        """Render a Dockerfile for building this application."""
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
                ), 'w') as dockerfile:
            dockerfile.write(self.final_dockerfile)
