#!/usr/bin/env python3
"""A simple command line interface for installing the applications."""
from container_gui.deploy import Application
from sys import argv
from textwrap import dedent


def show_usage():
    """Show the usage/help text."""
    print(dedent("""
        Run a GUI program in a docker container.

        Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO [ version DISTRO_VERSION ] launched-with APPLICATION_NAME"""
    ))
    exit(1)


def check_args(args: list) -> dict:
    """Store various information from the command line args in a usable way."""
    argvals = {}
    argvals['package_name'] = args[0]
    print()
    try:
        if args[1] == 'from':
            print()
            argvals['distro'] = args[2]
        else:
            print(args[1], "should have been 'from'")
            show_usage()
        if args[3] == 'version':
            print()
            argvals['version'] = args[4]
            if args[5] == 'launched-with':
                print()
                argvals['application_name'] = args[6]
            else:
                print(f'"{args[5]}"', "should have been 'launched-with'")
                show_usage()
        else:
            argvals['version'] = ''
            if args[3] == 'launched-with':
                print()
                argvals['application_name'] = args[4]
            else:
                print(f'"{args[3]}"', "should have been 'launched-with'")
                show_usage()
    except IndexError:
        print("Too many args:", len(argv))
        show_usage()
    return argvals


def build(args: list):
    """Build the appropriate Application object."""
    argvals = check_args(args)
    app = Application(
        package=argvals['package_name'],
        application=argvals['application_name'],
        distro=argvals['distro'],
        version=argvals['version']
    )
    app.build()
    return app


def run(args: list):
    """Build the appropriate Application object, then run it."""
    build(args).run()


if argv[1].lower() == 'build':
    print("Commencing build")
    build([arg.lower() for arg in argv[2:]])
elif argv[1].lower() == 'run':
    print("Commencing build for run")
    run([arg.lower() for arg in argv[2:]])
else:
    show_usage()
