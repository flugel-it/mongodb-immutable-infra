#!/bin/bash -ex

echo ${HOSTNAME} > /etc/hostname
hostname -F /etc/hostname

chmod +x /usr/local/sbin/join-mongo-cluster.py
nohup python /usr/local/sbin/join-mongo-cluster.py ${CLUSTER_NAME} &
