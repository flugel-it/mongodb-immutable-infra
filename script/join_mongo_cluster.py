#!/usr/bin/env python2
import platform
import sys
from time import sleep

import boto3
import requests
from pymongo import MongoClient

from utils import run_cmd


def get_region():
	"""
	Works only if the current computer is aws ec2 instance
	
	:return: region of the current aws ec2 instance (example: "eu-central-1")
	"""
	doc_url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
	res = requests.get(doc_url)
	reg = res.json()["region"]
	return reg


def get_instances(cluster_name, region_name=None):
	"""
	Gets all instances from the cluster in the same region as current instance
	
	:param region_name: the name of a region in which to search
	:param cluster_name: the name of cluster to get data from
	:return: list with instance data
	"""
	if region_name is None:
		region_name = get_region()
	ec2 = boto3.client('ec2', region_name=region_name)
	instances = ec2.describe_instances(Filters=[
		{
			'Name': 'tag:cluster',
			'Values': [cluster_name]
		},
		{
			'Name': 'instance-state-name',
			'Values': ['running']
		}
	]).get("Reservations")
	return instances


class Config:
	def __init__(self):
		self.config_file = "/etc/mongod.conf"
	
	def get_conf(self):
		with open(self.config_file, "r") as mongo_conf:
			cont = mongo_conf.read()
			return cont
	
	def write_conf(self, cluster_name):
		replica_conf = "replication:\n    replSetName: {0}\n".format(cluster_name)
		old_mongo_conf = self.get_conf()
		if replica_conf not in old_mongo_conf:
			old_mongo_conf = old_mongo_conf + replica_conf
		with open(self.config_file, "w+") as mongo_conf:
			mongo_conf.seek(0)
			mongo_conf.write(old_mongo_conf)
			mongo_conf.truncate()


class MongoConf:
	
	def __init__(self):
		self.uri = 'mongodb://localhost:27017/'
		self.client = MongoClient(self.uri)
	
	@staticmethod
	def create_rsconfig(replica_set, instances):
		instance_with_id = [{'_id': pos, 'host': instance} for pos, instance in enumerate(instances)]
		
		return {
			'_id': replica_set,
			'members': instance_with_id,
		}
	
	def initiate_rs(self, config):
		self.client.admin.command("replSetInitiate", config)


def main():
	if len(sys.argv) == 0:
		return
	cluster_name = sys.argv[1]
	
	instances = get_instances(cluster_name)
	
	conf = Config()
	conf.write_conf(cluster_name)
	
	run_cmd("systemctl enable mongod")
	run_cmd("systemctl restart mongod")
	
	# get only the hostname part, not fqdn
	# e.g: 'cluster_name-index'
	hostname = platform.node().split('.')[0]
	
	if hostname == cluster_name + "-0":
		
		# Wait other instances configure replica set
		sleep(180)
		
		# Means that is the PRIMARY
		# Only this instance will add the other nodes
		listinst = []
		reservations = instances
		for r in reservations:
			tags = r["Instances"][0]["Tags"]
			for t in tags:
				if t["Key"] == "Internal":
					listinst.append(tags[t]["Value"])
		
		# Initiate Replica Set
		mongo_config = MongoConf()
		config = mongo_config.create_rsconfig(cluster_name, listinst)
		mongo_config.initiate_rs(config)


if __name__ == "__main__":
	main()
