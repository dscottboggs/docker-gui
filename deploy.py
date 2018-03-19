from string import Template
PACKAGE_NAME = "simon"
dockerfile = open("Dockerfile.pytemplate", 'r')
before_substitutions = Template(dockerfile.read())
dockerfile.close()
final_dockerfile = before_substitutions.substitute(
    {
        "application": PACKAGE_NAME,
        "package": PACKAGE_NAME
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
dockerfile = open("Dockerfile", 'w')
dockerfile.write(final_dockerfile)
composition = {
    version: '2.0',
    services: {

    }
}
