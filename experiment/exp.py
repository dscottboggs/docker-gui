"""fuck your docstring, it's just an experiment."""
import docker
dc = docker.DockerClient('unix://var/run/docker.sock', version='1.30')
thispath = "/home/scott/Documents/code/docker-gui/experiment"
dc.images.build(path=thispath, tag='experiment')
