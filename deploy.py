from string import Template
PACKAGE_NAME = "simon"
dockerfile = open("Dockerfile.pytemplate", 'r')
before_substitutions = Template(dockerfile.read())
dockerfile.close()
final_dockerfile = before_substitutions.substitute(
    {
        "application": PACKAGE_NAME,
        "package": PACKAGE_NAME
    }
)
dockerfile = open("Dockerfile", 'w')
dockerfile.write(final_dockerfile)
composition = {
    version: '2.0',
    services: {

    }
}
