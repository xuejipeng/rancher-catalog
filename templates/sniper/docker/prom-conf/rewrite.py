import yaml
import os

config = yaml.load(open('/etc/prom-conf/prometheus.yml'))
#config = yaml.load(open('prometheus.yml'))


config['global']['external_labels'] = {}
config['global']['external_labels']['env'] = os.environ['RANCHER_ENV']
#config['global']['external_labels']['env'] = os.environ['HOME']

for i in range(0, len(config['scrape_configs'])-1):
    if config['scrape_configs'][i]['job_name'] == 'Prometheus':
        config['scrape_configs'][i]['metrics_path'] = os.environ['BASIC_PATH'] + "/metrics"
        #config['scrape_configs'][i]['metrics_path'] = os.environ['HOME'] + "/metrics"

if "true" == os.environ['ES_EXIST']:
    config['rule_files'].append("elasticsearch.yml")
    es_rule = yaml.load(open('/etc/prom-conf/elasticsearch.yml'))

    for i in range(0, len(es_rule['groups'][0]['rules']) -1):
        if es_rule['groups'][0]['rules'][i]["alert"] == "elasticsearch_too_few_nodes_running":
            es_rule['groups'][0]['rules'][i]["expr"] = ("elasticsearch_cluster_health_number_of_nodes < " + str(os.environ['ES_NODE_COUNT']))
            es_rule['groups'][0]['rules'][i]["annotations"]['summary'] += ("ElasticSearch running on less than " + str(os.environ['ES_NODE_COUNT']))
    es_rule_file = open('/etc/prom-conf/elasticsearch.yml', 'w')
    yaml.dump(es_rule, es_rule_file, default_flow_style=False)
    es_rule_file.close

else:
    if "elasticsearch.yml" in config['rule_files']:
        config['rule_files'].remove("elasticsearch.yml")

if "true" == os.environ['MYSQL_EXIST']:
    config['rule_files'].append("mysql.yml")
else:
    if "mysql.yml" in config['rule_files']:
        config['rule_files'].remove("mysql.yml")



if "true" == os.environ['MONGODB_EXIST']:
    config['rule_files'].append("mongodb.yml")
else:
    if "mongodb.yml" in config['rule_files']:
        config['rule_files'].remove("mongodb.yml")



url_yml = yaml.load(open('/etc/prom-conf/url.yml'))
url_yml_file = open('/etc/prom-conf/url.yml','w')

tcp_yml = yaml.load(open('/etc/prom-conf/tcp.yml'))
tcp_yml_file = open('/etc/prom-conf/tcp.yml','w')

env = os.environ

url_yml[0]["targets"] == None
if "blackbox.yml" in config['rule_files']:
    config['rule_files'].remove("blackbox.yml")

for (k,v) in  env.items():
    if k[0:3] == "URL":
        if url_yml[0]["targets"] == None:
            url_yml[0]["targets"] = []
            url_yml[0]["targets"].append(v)
            config['rule_files'].append("blackbox.yml")
        else:
            url_yml[0]["targets"].append(v)
    if k[0:3] == "POR":
        if tcp_yml[0]["targets"] == None:
            tcp_yml[0]["targets"] = []
            tcp_yml[0]["targets"].append(v)
            if "blackbox.yml" in config['rule_files']:
                print "blockbox.yml alredy exist"
            else:
                config['rule_files'].append("blackbox.yml")
        else:
            tcp_yml[0]["targets"].append(v)

yaml.dump(url_yml, url_yml_file, default_flow_style=False)
url_yml_file.close

yaml.dump(tcp_yml, tcp_yml_file, default_flow_style=False)
tcp_yml_file.close



print config['global']['external_labels']

config_file = open('/etc/prom-conf/prometheus.yml', 'w')
#config_file = open('prometheus.yml', 'w')

yaml.dump(config, config_file, default_flow_style=False)

config_file.close
