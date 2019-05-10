FROM python:3.7.3-alpine

RUN set -ex \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache/pip /var/cache/apt

WORKDIR /usr/src/app
COPY ./pycloudflare.py .

ENTRYPOINT [ "python", "./pycloudflare.py" ]