FROM registry.access.redhat.com/ubi8:latest
COPY requirements.txt /tmp/requirements.txt
COPY app.py /usr/bin/

RUN dnf install -y python3.8 && pip-3.8 install -r /tmp/requirements.txt

ENTRYPOINT ["/usr/bin/python3.8", "-u", "/usr/bin/app.py"]
