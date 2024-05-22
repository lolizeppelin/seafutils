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
Source1:        aria2d.conf
Source2:        aria2d.service
Source3:        aria2d-nginx.conf
BuildArch:      noarch

Requires:       aria2 >= 1.7
Requires:       jellyfin >= 10.8


%description
Aria2 rpc daemon service, use AriaNg as web

%prep
cp %{SOURCE3} .


%install
mkdir -p %{buildroot}%{_sharedstatedir}/aria2d
mkdir -p %{buildroot}%{_datarootdir}/aria2d

%{__install} -D -m 0755 %{buildroot}%{_datarootdir}/aria2d/html
unzip -d %{buildroot}%{_datarootdir}/aria2d/html/  %{SOURCE0}

%{__install} -D -m 0640 -p %{SOURCE1} -t %{buildroot}%{_sysconfdir}/aria2d
%{__install} -D -m 0644 -p %{SOURCE2} %{buildroot}%{_unitdir}/aria2d.service


%preun
systemctl stop aria2d.service


%files
%defattr(-,root,root,-)
%{_unitdir}/aria2d.service
%{_datarootdir}/aria2d
%config(noreplace) %{_sysconfdir}/aria2d/aria2d.conf
%doc aria2d-nginx.conf
%defattr(-,jellyfin,jellyfin,-)
%dir %{_sharedstatedir}/aria2d


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 1.3.7
- Update AriaNg to 1.3.7