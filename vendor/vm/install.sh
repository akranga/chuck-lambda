#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

add-apt-repository -y ppa:openjdk-r/ppa
apt-get update -y
apt-get install openjdk-8-jdk
update-alternatives --config java
apt-get -yqq install python-pip python-dev build-essential wget curl unzip
pip install awscli --ignore-installed six
pip install --upgrade virtualenv 

curl -O https://releases.hashicorp.com/terraform/0.7.5/terraform_0.7.5_linux_amd64.zip
unzip terraform_0.7.5_linux_amd64.zip
