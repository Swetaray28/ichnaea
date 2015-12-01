FROM mozilla-ichnaea/python:latest
MAINTAINER Mozilla Geolocation <dev-geolocation@lists.mozilla.org>
ENV PYTHONUNBUFFERED 1

WORKDIR /data/ichnaea
COPY ./requirements/*.txt requirements/
RUN bin/pip install --no-cache-dir --no-deps --disable-pip-version-check \
    -r requirements/prod.txt
RUN bin/pip install --no-cache-dir --no-deps --disable-pip-version-check \
    -r requirements/dev.txt
COPY . /data/ichnaea
RUN bin/python setup.py install
RUN bin/python compile.py

CMD ["bash"]