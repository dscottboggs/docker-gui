FROM ubuntu:16.04
MAINTAINER D. Scott Boggs "scott@tams.tech"

RUN mkdir -p /home/GUIuser && \
    echo "GUIuser:x:1000:1000:GUIuser,,,:/home/GUIuser:/bin/bash" >> /etc/passwd && \
    echo "GUIuser:x:1000:" >> /etc/group && \
    echo "GUIuser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/GUIuser && \
    chmod 0440 /etc/sudoers.d/GUIuser && \
    chown GUIuser:GUIuser -R /home/GUIuser ||\
    echo failed to create user #           ^^ error condition

RUN apt-get install simon

USER GUIuser
ENV HOME /home/GUIuser
WORKDIR /home/GUIuser
CMD simon