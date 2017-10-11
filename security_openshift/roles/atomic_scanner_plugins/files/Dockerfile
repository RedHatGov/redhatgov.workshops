FROM registry.access.redhat.com/rhel7:latest
LABEL INSTALL='docker run -it --rm --privileged -v /etc/atomic.d/:/host/etc/atomic.d/ $IMAGE sh /install.sh'
ADD example_plugin /
ADD list_rpms.py /
ADD install.sh /
