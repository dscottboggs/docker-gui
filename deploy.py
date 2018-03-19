from yaml import dump
from os.path import dirname, realpath
from os.path import join as getpath
from os import environ
from pystache import render
working_directory = dirname(realpath(__file__))
PACKAGE_NAME = "geany"
with open(getpath(working_directory, "Dockerfile.pytemplate"), 'r') as dockerfile:
    before_substitutions = dockerfile.read()
final_dockerfile = render(
    template=before_substitutions,
    context={
        'package': PACKAGE_NAME,
        'application': PACKAGE_NAME,
        'distro': {
            'name': "ubuntu",
            'version': 16.04,
            'pkg_mngr_cmd': 'apt-get update && apt-get install -y'
        }
    }
)
with open(getpath(working_directory, "Dockerfile"), 'w') as dockerfile:
    dockerfile.write(final_dockerfile)

composition = {
    'version': '2.0',
    'services': {
        'application': {
            'build': working_directory,
            'command': PACKAGE_NAME,
            'volumes': [
                "/tmp/.X11-unix:/tmp/.X11-unix"
            ],
            'networks': ['application'],
            'environment': {'DISPLAY': environ['DISPLAY']}
        }
    },
    'networks': {'application': None}
}
with open(getpath(working_directory, "docker-compose.yml"), 'w') as compose_file:
    compose_file.write(dump(composition))
