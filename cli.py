#!/usr/bin/env python3
from deploy import Application
from sys import argv
from textwrap import dedent


def show_usage():
    print(dedent("""
        Run a GUI program in a docker container.

        Usage: docker-gui (run|build) PACKAGE_NAME from DISTRO [ version DISTRO_VERSION ] launched-with APPLICATION_NAME"""
    ))
    exit(1)

def check_args(args: list):
    argvals = {}
    argvals['package_name'] = args[0]
    try:
        if args[1]=='from':
            argvals['distro']=args[2]
        else:
            print(args[1], "should have been 'from'")
            show_usage()
        if args[3]=='version':
            argvals['version']=args[4]
            if args[5]=='launched-with':
                argvals['application_name']=args[6]
            else:
                print(f'"{args[5]}"', "should have been 'launched-with'")
                show_usage()
        else:
            version=''
            if args[3]=='launched-with':
                argvals['application_name']=args[4]
            else:
                print(f'"{args[3]}"', "should have been 'launched-with'")
                show_usage()
    except IndexError:
        show_usage()
    return argvals


def build(args: list):
    argvals = check_args(args)
    return Application(
        package_name=argvals['package_name'],
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
