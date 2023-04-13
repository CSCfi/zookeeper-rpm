zookeeper-redhat7-rpm
---------
This is a set of scripts to make zookepeer rpm package for CentOS/RedHat 7.

Setup
-----
    sudo yum install make rpmdevtools wget

Building
--------
    make rpm

Resulting RPM will be avaliable at $(shell pwd)/noarch/

Installing and operating
------------------------
    sudo yum install zookeeper*.rpm
    sudo systemctl enable zookeeper
    sudo systemctl start zookeeper

Zookeeper shell is available via zkcli.

Default locations
-----------------
archives: /usr/share/java/zookeeper
data:     /var/lib/zookeeper
logs:     /var/log/zookeeper
configs:  /etc/zookeeper, /etc/sysconfig/zookeeper
