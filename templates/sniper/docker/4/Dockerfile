#FROM rancher/confd-base:0.11.0-dev-rancher
FROM debian

ADD ./conf.d /etc/confd/conf.d
ADD ./templates /etc/confd/templates
ADD ./confd /
VOLUME /etc/prom-app-conf

ENTRYPOINT ["/confd"]
CMD ["--backend", "rancher", "--prefix", "/2015-07-25"]