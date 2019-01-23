#Prometheus Config Store Dockerfile
FROM python:2.7-slim 
LABEL maintainer "(xuejipeng@sensetime.com)"


ENV RANCHER_ENV=manager

RUN mkdir -p /etc/prom-conf/
COPY conf/* /etc/prom-conf/
COPY init.sh rewrite.py /

RUN pip install pyyaml

CMD ["/bin/sh" "-c" "sh init.sh ; /bin/sh"]
