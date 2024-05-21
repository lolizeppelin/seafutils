%global debug_package %{nil}
%define proj_name seafutils
%define _release 1

Name:           %{proj_name}
Version:        2.0.0
Release:        %{_release}%{?dist}
Summary:        manager utils for seafile server
Group:          Development/Libraries
License:        MIT
URL:            http://github.com/Lolizeppelin/%{proj_name}
Source0:        %{proj_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python >= 3.6
BuildRequires:  python-setuptools >= 40
BuildRequires:  python-oslo-config >= 6.0.0
BuildRequires:  python3-psycopg3 >= 3.1.0

# base required
Requires(pre):  shadow-utils
Requires:       python >= 3.6
Requires:       python3-psycopg3 >= 3.1.0
Requires:       python-oslo-config >= 6.0.0
Requires:       python3-stevedore >= 1.20.0
# seafile required
Requires:       seahub >= 7.0.2
Requires:       seafile-server >= 7.0.2
Requires:       seafile-ccnet >= 7.0.2



%description
utils for seafile server

%prep
%setup -q -n %{proj_name}-%{version}
rm -rf %{proj_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# config path
mkdir -p %{buildroot}%{_sysconfdir}/seafile
mkdir -p %{buildroot}%{_sysconfdir}/seafile/central

# systemd service file
%{__install} -D -m 0644 -p seahub.service %{buildroot}%{_unitdir}/seahub.service
%{__install} -D -m 0644 -p ccnet.service %{buildroot}%{_unitdir}/ccnet.service
%{__install} -D -m 0644 -p ccnet.service %{buildroot}%{_unitdir}/ccnet.service

# log files
mkdir -p %{buildroot}/var/log/seafile

# bin files
for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;

for l in sbin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_sbindir}
done;



%preun
systemctl stop seahub.service
systemctl stop seafile.service
systemctl stop ccnet.service


%files
%defattr(-,root,root,-)
%{_bindir}/seafutil-*
%{_sbindir}/seafutil-init-*
%dir %{_sysconfdir}/seafile
%dir %{_sysconfdir}/seafile/central
%config(noreplace) %{_sysconfdir}/seafile.conf
%{_unitdir}/seafile.service
%{_unitdir}/ccnet.service
%{_unitdir}/seahub.service
%{py_sitedir}/%{proj_name}/*
%dir %{py_sitedir}/%{proj_name}-%{version}-*.egg-info/
%{py_sitedir}/%{proj_name}-%{version}-*.egg-info/*
%doc README.md
%doc doc/*
%defattr(-,seafile,seafile,-)
%dir /var/log/seafile


%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package