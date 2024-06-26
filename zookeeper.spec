%global __jar_repack 0
%global zk_prefix  %{_javadir}/zookeeper
%global zk_confdir %{_sysconfdir}/zookeeper
%global zk_logdir  %{_var}/log/zookeeper
%global zk_datadir %{_sharedstatedir}/zookeeper

%{!?zk_version:%global zk_version 3.8.4}
%{!?zk_release:%global zk_release 1}

Summary: High-performance coordination service for distributed applications
Name: zookeeper
Version: %{zk_version}
Release: %{zk_release}%{?dist}
License: ASL 2.0 and BSD
Group: Applications/Databases
URL: https://zookeeper.apache.org/
Source0: https://archive.apache.org/dist/zookeeper/zookeeper-%{version}/apache-zookeeper-%{version}-bin.tar.gz
Source1: zookeeper.service
Source2: zkcli
Source3: zookeeper.logrotate
Source4: zookeeper.sysconfig
Source5: zoo.cfg
Source6: logback.xml
%{?systemd_requires}
BuildRequires: systemd
BuildArch: noarch
%if 0%{?rhel} > 8
Requires: jre-17-headless
%else
Requires: jre-11-headless
%endif

%description
ZooKeeper is a high-performance coordination service for distributed
applications. It exposes common services - such as naming, configuration
management, synchronization, and group services - in a simple interface so
you don't have to write them from scratch. You can use it off-the-shelf to
implement consensus, group management, leader election, and presence
protocols. And you can build on it for your own, specific needs.


%package -n nagios-plugins-zookeeper
Group:             Applications/System
Summary:           Provides check_zookeeper support for Nagios
BuildArch:         noarch
Requires:          nagios-plugins

%description -n nagios-plugins-zookeeper
Provides check_zookeeper support for Nagios.


%prep
%setup -q -n apache-%{name}-%{version}-bin

%build

%install
# bin
mkdir -p $RPM_BUILD_ROOT/usr/bin/
install -p -m 0755 bin/*.sh $RPM_BUILD_ROOT/usr/bin/

# JARs
mkdir -p $RPM_BUILD_ROOT%{zk_prefix}
install -p -m 0644 lib/*.jar $RPM_BUILD_ROOT%{zk_prefix}/

# Service, systemd fails to expand file paths in runtime
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
CLASSPATH=
for i in $RPM_BUILD_ROOT%{zk_prefix}/*.jar; do
  CLASSPATH="%{zk_prefix}/$(basename ${i}):${CLASSPATH}"
done
sed -e "s|@CLASSPATH@|${CLASSPATH}|" %{S:1} > \
  $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service
# CLI
install -p -D -m 0755 %{S:2} $RPM_BUILD_ROOT%{_bindir}/zkcli
# Configuration
install -p -D -m 0644 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 0644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zookeeper
mkdir -p $RPM_BUILD_ROOT%{zk_confdir}/
install -p -m 0644 %{S:5} %{S:6} conf/configuration.xsl \
  $RPM_BUILD_ROOT%{zk_confdir}/
# Empty directories
mkdir -p $RPM_BUILD_ROOT%{zk_logdir}
mkdir -p $RPM_BUILD_ROOT%{zk_datadir}

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null; then
  /usr/sbin/useradd -r -g zookeeper -M -N -d %{zk_prefix} -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service

%files
%license LICENSE.txt
%{zk_prefix}/
%{_unitdir}/zookeeper.service
%{_bindir}/zkcli
%{_bindir}/*.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper
%attr(0755,zookeeper,zookeeper) %dir %{zk_confdir}/
%attr(0644,zookeeper,zookeeper) %config(noreplace) %{zk_confdir}/*
%attr(0755,zookeeper,zookeeper) %dir %{zk_logdir}/
%attr(0700,zookeeper,zookeeper) %dir %{zk_datadir}/

%changelog
* Tue Nov 22 2016 Michał Lisowski <michal@exads.com> - 3.4.9-3
- Add nagios-plugins-zookeeper subpackage

* Wed Oct 26 2016 Matthias Saou <matthias@saou.eu> 3.4.9-2
- Add java-headless requirement.

* Tue Oct 11 2016 Matthias Saou <matthias@saou.eu> 3.4.9-1
- Simplify, fix and clean up the spec file and related files.

