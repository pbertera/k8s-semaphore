FROM registry.access.redhat.com/ubi8:latest
RUN dnf install -y python3.8 && pip-3.8 install web.py

COPY app.py /usr/bin/

ENTRYPOINT ["/usr/bin/python3.8", "-u", "/usr/bin/app.py"]
