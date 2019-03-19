%include %{_rpmconfigdir}/macros.python

%global debug_package %{nil}
%define proj_name seafutil
%define _release 12

Name:           python2-%{proj_name}
Version:        1.0.0
Release:        %{_release}%{?dist}
Summary:        manager utils for seafile server
Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/Lolizeppelin/%{proj_name}
Source0:        %{proj_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2 >= 2.7
BuildRequires:  python2-oslocfg >= 1.0.0
BuildRequires:  python2-setuptools >= 40

Requires(pre):  shadow-utils
Requires:       python2 >= 2.7
Requires:       seafile-server >= 6.3.4
Requires:       python2-mysql >= 1.3
Requires:       python2-sqlalchemy >= 1.2
Requires:       python2-pg8000 >= 1.12


%description
utils for seafile server

%prep
%setup -q -n %{proj_name}-%{version}
rm -rf %{proj_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%{__install} -D -m 0640 -p etc/seafile.conf -t %{buildroot}%{_sysconfdir}
%{__install} -D -m 0644 -p etc/sysconfig/seafile -t %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -D -m 0644 -p seafile.service %{buildroot}%{_unitdir}/seafile.service


mkdir -p %{buildroot}%{_sysconfdir}/seafile
mkdir -p %{buildroot}/var/log/seafile


for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;

for l in sbin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_sbindir}
done;


%pre
if [ "$1" = "1" ] ; then
    getent group seafile >/dev/null || groupadd -f -g 873 -r seafile
    if ! getent passwd seafile >/dev/null ; then
        if ! getent passwd 873 >/dev/null ; then
          useradd -r -u 873 -g seafile -M -s /sbin/nologin -c "Seafile server" seafile
        else
          useradd -r -g seafile -M -s /sbin/nologin -c "Seafile server" seafile
        fi
    fi
fi


%preun
systemctl stop seafile.service


%postun
if [ "$1" = "0" ] ; then
    /usr/sbin/userdel seafile > /dev/null
fi


%files
%defattr(-,root,root,-)
%{_bindir}/seafutil-*
%{_sbindir}/seafutil-init-*
%dir %{_sysconfdir}/seafile
%config(noreplace) %{_sysconfdir}/seafile.conf
%config(noreplace) %{_sysconfdir}/sysconfig/seafile
%{_unitdir}/seafile.service
%{py_sitedir}/%{proj_name}/*
%dir %{py_sitedir}/%{proj_name}-%{version}-*.egg-info/
%{py_sitedir}/%{proj_name}-%{version}-*.egg-info/*
%doc README.md
%doc doc/*
%doc etc/nginx/conf.d/seahub.conf
%doc etc/uwsgi.d/seahub.ini
%defattr(-,seafile,seafile,-)
%dir /var/log/seafile

%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package