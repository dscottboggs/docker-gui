from distros import getdistro
test_input = {
    "package": "x11-apps",
    "application": "xeyes",
    "distro": getdistro("ubuntu", "16.04"),
}

from yaml import dump
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import environ as local_environment
from os import makedirs as mkdir
from pystache import render
from docker import DockerClient
from docker.types import Mount

class Config{
    dc = DockerClient('unix://run/docker.sock', version='1.30')
    network_name = "docker_application_network"
    try:
        application_network = dc.networks.list(names=[network_name])[0]
    except IndexError:
        application_network = dc.networks.create(network_name)
    log=print
}

def check_isdir(filepath):
    if not isdir(filepath):
        if access(filepath, F_OK):
            raise FileExistsError("Goal directory {filepath} exists as a file.")
        else:
            mkdir(filepath, mode=0o755)


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
        self.image_name = f"img_{self.application}_in_{self.distro.name}_{self.distro.version}"
        self.container_name = image_name[4:]
        self.init_files()
        self.write_desktop_file()

    def run(self):
        if dc.containers.list(all=True, filters={'name':self.container_name}):
            #an empty list is falsy and will skip this block
            if dc.containers.list(filters={'name':self.container_name}):
                Config.log("Application is already running!")
                return
            for container in docker.containers.list(
                        all=True
                        filters={'name':self.container_name}
                    ):
                dc.api.remove_container(
                    container
                )
        if not dc.images.list(name=self.image_name):
            self.build()
        dc.containers.run(
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
        self.working_directory = getpath('/', 'usr', 'share', 'docker-gui')
        check_isdir(self.working_directory)
        with open(getpath(working_directory, "Dockerfile.pytemplate"), 'r') as dockerfile:
            self.before_substitutions = dockerfile.read()
        self.application_directory = getpath(
            self.working_directory,
            self.application
        )
        check_isdir(self.application_directory)

    def write_desktop_file(self):
        with open(
                    getpath(
                        'usr',
                        'share',
                        'applications',
                        "%s.docker.desktop" % test_input['application']
                    )
                ) as desktop_file:
            desktop_file.write(render(
                text=dedent("""
                    [Desktop Entry]
                    Version=From {{ distro }}
                    Name={{ application }}
                    Exec={{ command }}
                    Terminal=false
                    Type=Application
                    Categories=Containerized
                    """
                ),
                context={
                    'commmand': f"docker run {self.image_name}"
                    'application': self.application,
                    'distro': self.distro.distro
                }
            ))

    def build(self):
        """Builds a docker image for the specified environment."""
        self.render_dockerfile()
        dc.images.build(
            path=self.application_directory,
            tag=self.image_name
        )

    def render_dockerfile(self):
        self.final_dockerfile = render(
            template=self.before_substitutions,
            context={
                'package': self.package,
                'application': self.application,
                'distro': self.distro,
                'uid': environ['UID'],
                'gid': environ['GID']
            }
        )
        with open(getpath(
                    self.application_directory, "Dockerfile"
                ),'w') as dockerfile:
            dockerfile.write(final_dockerfile)
