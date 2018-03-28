#!/usr/bin/env python3
from deploy import Application
from sys import argv
from textwrap import dedent


def show_usage():
    print(dedent("""
        Run a GUI program in a docker container.

        Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO version DISTRO_VERSION launched with APPLICATION_NAME"""
    ))
    exit(1)

def check_args(args: list):
    argvals = {}
    try:
        if args[1]=='from':
            argvals['distro']=args[2]
        else:
            print(args[1], "should have been 'from'")
            show_usage()
        if args[3]=='version':
            argvals['version']=args[4]
            if args[5:6]==['launched', 'with']:
                argvals['application_name']=args[7]
            else:
                print(args[5], args[6], "should have been 'launched with'")
                show_usage()
        else:
            version=args[3]
            if args[4:5]==['launched', 'with']:
                argvals['application_name']=args[6]
            else:
                print(args[4], args[5], "should have been 'launched with'")
                show_usage()
    except IndexError:
        show_usage()
    return argvals


def build(args: list):
    pkg_name = args[0].lower()
    argvals = check_args(args)
    return Application(
        package_name=pkg_name,
        application_name=argvals['application_name'],
        distro=argvals['distro'],
        version=argvals['version']
    )

def run(args: list):
    build(args).run()

if argv[1].lower()=='build':
    build([arg.lower() for arg in argv[2:]])
elif argv[1].lower()=='run':
    run([arg.lower() for arg in argv[2:]])
else:
    show_usage()
