#!/usr/bin/env python2

import boto3
import os
import platform
import requests
import shutil
import subprocess
import sys
from pymongo import MongoClient
from time import sleep


class Crawler:

    def get_region(self):
        doc_url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
        res = requests.get(doc_url)
        reg = res.json()["region"]
        return reg


    def get_instances(self, cluster_name):
        ec2 = boto3.client('ec2', region_name=self.get_region())
        instances = ec2.describe_instances( Filters = [
            {'Name': 'tag:cluster',
            'Values': [cluster_name]},
            {'Name': 'instance-state-name',
            'Values': ['running']}
            ])
        return instances


class Config:

    def __init__(self):
        self.conffile = "/etc/mongod.conf"

    def get_conf(self):
        with open(self.conffile, "r") as mconf:
            cont = mconf.read()
            return cont

    def write_conf(self, cluster_name):
        rconf = """
replication:
    replSetName: {0}
""".format(cluster_name)
        cont = self.get_conf()
        with open(self.conffile, "w") as mconf:
            if not rconf in cont:
                cont = cont + rconf
            mconf.seek(0)
            mconf.write(cont)
            mconf.truncate()

class MongoConf:

    def __init__(self):
        self.uri = 'mongodb://localhost:27017/'
        self.client = MongoClient(self.uri)

    def create_rsconfig(self, replica_set, instances):
        lmembers = list()
        diconfig = dict()

        diconfig = {'_id' : replica_set}

        for i in range(len(instances)):
            d = dict()
            d = {'_id' : i, 'host' : instances[i]}
            lmembers.append(d)

        diconfig.update({'members' : lmembers})
        return diconfig


    def initiate_rs(self, config):
        self.client.admin.command("replSetInitiate", config)

def runcmd(cmd):
    proc = subprocess.Popen(cmd, shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            close_fds=False)
    out, err = proc.communicate()
    return out


if __name__ == "__main__":

    cluster_name = sys.argv[1]

    crawler = Crawler()
    instances = crawler.get_instances(cluster_name)

    conf = Config()
    conf.write_conf(cluster_name)

    cmd = "systemctl enable mongod"
    runcmd(cmd)
    cmd = "systemctl restart mongod"
    runcmd(cmd)

    # get only the hostname part, not fqdn
    # e.g: 'cluster_name-index'
    hostname = platform.node().split('.')[0]

    if hostname == cluster_name + "-0":

        # Wait other instances configure replica set
        sleep(180)

        # Means that is the PRIMARY
        # Only this instance will add the other nodes
        listinst = list()

        reservations = instances["Reservations"]
        for r in range(len(reservations)):
            tags = reservations[r]["Instances"][0]["Tags"]
            for t in range(len(tags)):
                if tags[t]["Key"] == "Internal":
                    listinst.append(tags[t]["Value"])

        # Initiate Replica Set
        mongoc = MongoConf()
        config = mongoc.create_rsconfig(cluster_name, listinst)
        mongoc.initiate_rs(config)
