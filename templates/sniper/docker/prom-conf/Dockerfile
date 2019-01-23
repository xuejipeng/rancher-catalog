#Prometheus Config Store Dockerfile
FROM python:2.7-slim 
LABEL maintainer "(xuejipeng@sensetime.com)"


ENV RANCHER_ENV=manager

RUN mkdir -p /etc/prom-conf/
COPY conf/* /etc/prom-conf/
COPY init.sh rewrite.py /

RUN pip install pyyaml
ADD ./conf.d /etc/confd/conf.d
ADD ./templates /etc/confd/templates
VOLUME /etc/logstash
VOLUME /opt/logstash/patterns

ENTRYPOINT ["/confd"]
CMD ["--backend", "rancher", "--prefix", "/2015-07-25"]

CMD ["/bin/sh", "-c", "./init.sh ; /bin/sh"]
