from distros import getdistro
test_input = {
    "package": "x11-apps",
    "application": "xeyes",
    "distro": getdistro("ubuntu", "16.04"),
}

from yaml import dump
from os.path import dirname, realpath, isdir
from os.path import join as getpath
from os import environ
from os import makedirs as mkdir
from pystache import render

class Application():
    """An application to deploy"""
    def __init__(self, package: str, application: str, distro: str, version: str=''):
        self.package = package
        self.application = application
        self.distro = getdistro(distro, version)

    def init_files(self):
        self.working_directory = getpath('usr', 'share', 'docker-gui')
        if not isdir(working_directory):
            if access(working_directory, F_OK):
                raise RuntimeError("Directory to work in exists as a file.")
            else:
                mkdir(working_directory, mode=0o755)
        with open(getpath(working_directory, "Dockerfile.pytemplate"), 'r') as dockerfile:
            self.before_substitutions = dockerfile.read()
        self.application_directory = getpath(
            self.working_directory,
            self.application
        )

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



composition = {
    'version': '2.0',
    'services': {
        'application': {
            'build': working_directory,
            'command': PACKAGE_NAME,
            'volumes': [
                "/tmp/.X11-unix:/tmp/.X11-unix",
                "/dev/dri:/dev/dri",
                "/dev/snd:/dev/snd",
                "/dev/video0:/dev/video0"
            ],
            'networks': ['application'],
            'environment': {'DISPLAY': environ['DISPLAY']}
        }
    },
    'networks': {'application': None}
}
compose_file_path = getpath(
    application_directory,
    "docker-compose.yml"
)
with open(
            compose_file_path,
            'w'
        ) as compose_file:
    compose_file.write(dump(composition))
