%global debug_package %{nil}
%define _release 1


Name:           aria2d
Version:        1.3.7
Release:        %{_release}%{?dist}
Summary:        aria2 domain utils
Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/Lolizeppelin/%{name}
Source0:        AriaNg-%{version}.zip
BuildArch:      noarch

Requires:       aria2 >= 1.7
Requires:       jellyfin >= 10.8


%description
Aria2 rpc daemon service, use AriaNg as web

%prep
%setup -q -n %{name}-%{version}


%install
mkdir -p %{buildroot}%{_sharedstatedir}/aria2d
mkdir -p %{buildroot}%{_datarootdir}/aria2d
%{__install} -D -m 0755 %{buildroot}%{_datarootdir}/aria2d/html
cp * %{buildroot}%{_datarootdir}/aria2d/html/


%{__install} -D -m 0644 -p aria2d.service %{buildroot}%{_unitdir}/aria2d.service
%{__install} -D -m 0640 -p etc/aria2d/aria2d.conf -t %{buildroot}%{_sysconfdir}/aria2d


%preun
systemctl stop aria2d.service


%files
%defattr(-,root,root,-)
%{_unitdir}/aria2d.service
%{_datarootdir}/aria2d
%doc README.md
%doc etc/nginx/aria2d-nginx.conf
%defattr(-,jellyfin,jellyfin,-)
%dir %{_sharedstatedir}/aria2d
%config(noreplace) %{_sysconfdir}/aria2d/aria2d.conf


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 1.3.7
- Update AriaNg to 1.3.7