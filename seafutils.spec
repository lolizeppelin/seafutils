%global debug_package %{nil}
%define _release 1

Name:           seafutils
Version:        2.0.0
Release:        %{_release}%{?dist}
Summary:        manager utils for seafile server
Group:          Development/Libraries
License:        MIT
URL:            http://github.com/Lolizeppelin/%{name}
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3 >= 3.6
BuildRequires:  python3-setuptools >= 40
BuildRequires:  python3-oslo-config >= 6.0.0
BuildRequires:  python3-psycopg3 >= 3.1.0

# base required
Requires(pre):  shadow-utils
Requires:       python3 >= 3.6
Requires:       python3-setuptools >= 40
Requires:       python3-psycopg3 >= 3.0.0
Requires:       python3-stevedore >= 2.0.0
Requires:       python3-oslo-config >= 6.0.0

# seafile required
Requires:       seahub = 7.0.2
Requires:       seafile-server = 7.0.2
Requires:       ccnet = 7.0.2



%description
utils for seafile server

%prep
%setup -q -n %{name}-%{version}
rm -rf %{name}.egg-info

%build
sed -i '0,/VERSION/s//%{version}/' setup.cfg
sed -i '0,/VERSION/s//%{version}/' PKG-INFO
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
# 配置文件生成
%{__python3} config-generator.py

# systemd service file
%{__install} -D -m 0644 -p seahub.service %{buildroot}%{_unitdir}/seahub.service
%{__install} -D -m 0644 -p seafile.service %{buildroot}%{_unitdir}/seafile.service
%{__install} -D -m 0644 -p ccnet.service %{buildroot}%{_unitdir}/ccnet.service


# config path
%{__mkdir} -p %{buildroot}%{_sysconfdir}/seafile
%{__mkdir} -p %{buildroot}%{_sysconfdir}/seafile/central
# config file
%{__install} -D -m 0644 -p etc/seafile/seafile.conf %{buildroot}%{_sysconfdir}/seafile/seafile.conf

# log files
%{__mkdir} -p %{buildroot}/var/log/seafile

# bin files
for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;



%preun
systemctl stop seahub.service
systemctl stop seafile.service
systemctl stop ccnet.service


%files
%defattr(-,root,root,-)
%{_bindir}/seafile-launch
%{_bindir}/seafutils
%{_unitdir}/seafile.service
%{_unitdir}/ccnet.service
%{_unitdir}/seahub.service
%{python3_sitelib}/%{name}/*
%dir %{python3_sitelib}/%{name}-%{version}-py3.*.egg-info/
%{python3_sitelib}/%{name}-%{version}-py3.*.egg-info/*
%doc README.md
%doc doc/*
%doc etc/initialize.conf
%defattr(-,seafile,seafile,-)
%dir %{_sysconfdir}/seafile
%dir %{_sysconfdir}/seafile/central
%dir /var/log/seafile
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/seafile/seafile.conf


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 2.0.0
- Seafile Update to 7.0.2
- Optimize code structure

* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package