#!/usr/bin/env python3
"""Functionality to perform a deployment of an application."""
from os.path import join as getpath
from os import environ as local_environment
from os import getuid, getgid, chmod, remove
from stat import S_IRWXU, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH

from textwrap import dedent
from jinja2 import Template as JinjaTemplate

from docker.types import Mount

from container_gui.config import Config
from container_gui.distros import getdistro
from time import sleep
from container_gui.misc_functions import *


class Application():
    """An application to deploy."""

    local_share = getpath(local_environment['HOME'], '.local', 'share')

    def __init__(self, package: str, application: str):
        """Initialize and provide methods for acting on a given application."""
        if False in [isinstance(val, str) for val in (package, application)]:
            raise TypeError(dedent(f"""
                One of the following attributes was not a string:
                  - package {package} (type {type(package)})
                  - application {application} (type {type(application)})"""))
        self.package = package
        self.application = application
        self.image_name = "img_%s_from_aur" % (self.application)
        self.container_name = self.image_name[4:]
        self.init_files()

    def uninstall(self, check=False):
        """Uninstall the package."""
        if check:
            if ask("%s is already installed. Would you like to remove it?",
                   self.application,
                   default='No'):
                return self.uninstall()
            else:
                return False    # not uninstalled at the request of the user.
        Config.dc.containers.remove(self.container_name)
        Config.dc.images.remove(self.image_name)
        remove(self.desktop_file)
        remove(self.run_script_file)
        return True

    def run(self):
        """Check that the application isn't already running and start it."""
        if Config.dc.containers.list(all=True,
                                     filters={'name': self.container_name}):
            # an empty list is falsy and will skip this block
            if Config.dc.containers.list(
                filters={'name': self.container_name}
            ):
                if not uninstall(check=True):
                    print("%s is already running!" % self.application)
                    return
            for container in Config.dc.containers.list(
                        all=True,
                        filters={'name': self.container_name}
                    ):
                if not uninstall(check=True):
                    print(self.application, "is already installed.")
                    exit(0)
        if not Config.dc.images.list(name=self.image_name):
            self.build()
        Config.dc.containers.run(
            image=self.image_name,
            devices=["/dev/snd:/dev/snd:rw",
                     "/dev/dri:/dev/dri:rw"],
            mounts=[Mount(source="/tmp/.X11-unix",
                          target="/tmp/.X11-unix",
                          type='bind')],
            environment={'DISPLAY': local_environment['DISPLAY']},
            network=Config.application_network.id,
            remove=False
        )

    def init_files(self):
        """Write all the files to use this Application at a later time."""
        self.working_directory = getpath(self.local_share, 'dock-aur')
        check_isdir(self.working_directory)
        with open(getpath(self.working_directory,
                          "Dockerfile.pytemplate"), 'r') as dockerfile:
            self.dockerfile_template = dockerfile.read()
        self.application_directory = getpath(self.working_directory,
                                             self.application_directory)
        check_isdir(self.application_directory)
        self.run_script_file = getpath(self.application_directory,
                                       f"run_{self.application}")
        self.render_dockerfile()
        self.write_run_script()
        self.write_desktop_file()

    def write_run_script(self):
        """Write a script to run this application to a file."""
        with open(Config.runscript_template) as templatefile:
            template = JinjaTemplate(templatefile.read())
        try:
            with open(self.run_script_file, 'w') as run_script_file:
                run_script_file.write(
                    template.render(
                        application_directory=self.application_directory,
                        image_name=self.image_name,
                        container_name=self.container_name
                    ) + '\n'         # a hack because apparently rendering the
                )                    #      template eats the trailing newline
        chmod(self.run_script_file,
              S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH)
        # these ^^ bitwise-or'd values ^^  basically equate to rwxr-xr-x

    def write_desktop_file(self):
        """Create the .desktop file for this Applicationself.

        Creating and storing this file in /usr/share/applications allows the
        user to run the application from their app menu or launcher.
        """
        self.desktop_file = getpath(self.local_share,
                                    'applications',
                                    "%s.dock-aur.desktop" % self.application)
        try:
            desktop_file = open(self.desktop_file)
            desktop_file.write(dedent(f"""
                [Desktop Entry]
                Version=From {self.distro.distro}
                Name={self.application}
                Exec={self.run_script_file}
                Terminal=false
                Type=Application
                Categories=Containerized
                """))
        except PermissionError:
            runcmd("""sudo su -c 'touch {0} && chown {1}:{2} {0}'""".format(
                self.desktop_file, getuid(), getgid()
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
        """Render a dockerfile for building this application."""
        with open(config.dockerfile_template, 'r') as templatefile:
            template = jinjatemplate(templatefile.read())
        with open(getpath(
                    self.application_directory, "Dockerfile"
                ), 'w') as dockerfile:
            dockerfile.write(
                template.render(
                    package=self.package,
                    application=self.application,
                    uid=getuid(),
                    gid=getgid()
                ) + '\n'            # a hack because apparently rendering the
            )                       # template eats the trailing newline
