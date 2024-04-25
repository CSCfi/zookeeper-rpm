.PHONY:	rpm clean

VERSION ?= 3.8.4
RELEASE ?= 1
SOURCE = apache-zookeeper-$(VERSION)-bin.tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)
URL = https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/$(SOURCE)
rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "zk_version $(VERSION)" \
			--define "zk_release $(RELEASE)" \
			zookeeper.spec

source: $(SOURCE)

$(SOURCE): KEYS $(SOURCE).asc
	@wget -q $(URL)
	gpg --verify $(SOURCE).asc $(SOURCE)

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(SOURCE)

$(SOURCE).asc:
	@wget https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/$(SOURCE).asc

KEYS:
	@wget https://dist.apache.org/repos/dist/release/zookeeper/KEYS
	gpg --import KEYS

