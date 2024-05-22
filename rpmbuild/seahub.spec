%global _hardened_build 1
%define _release 1


Name:           ccnet
Version:        7.0.2
Release:        %{_release}%{?dist}
Summary:        Seahub is the web frontend for Seafile.

License:        LGPLv3
URL:            https://github.com/haiwen/%{name}
Source0:        %{name}-%{version}.tar.gz
# 打包好的三方库
Source1:        %{name}-3rd.tar.gz
# sql初始化文件
Source2:        seahub.postgres.sql

Requires:       python2 >= 2.7
Requires:       libsearpc >= 3.1
Requires:       python2-psycopg2 >= 2.0


%description
Seafile is a next-generation open source cloud storage system with
advanced support for file syncing, privacy protection and teamwork.


%prep
%setup -qn %{name}-%{version}.tar.gz

%build
# overwrite third part
tar -xf %{SOURCE1} -C .
cp -p %{SOURCE2} .

%install
# 头像
install -d %{name}-%{version}/media/avatars %{buildroot}%{_datadir}/%{name}/avatars
# 缩略图
install -d %{name}-%{version}/%{name}/thumb %{buildroot}%{_datadir}/%{name}/thumb
# 初始化sql
install -D -m 644 seahub.postgres.sql %{buildroot}%{_datadir}/%{name}/sql/postgres.sql

# 删除头像与缩略图文件夹
rm -rf %{name}-%{version}/media/avatars
rm -rf %{name}-%{version}/%{name}/thumb

# 拷贝程序文件
%{__install} -D -m 0755 %{name}-%{version} %{buildroot}%{_datadir}/%{name}



%post
# 创建软连接
ln -s -f %{_datadir}/%{name}/media/avatars %{_datadir}/%{name}/avatars
ln -s -f %{_datadir}/%{name}/%{name}/thumb %{_datadir}/%{name}/thumb


%preun
# 删除软连接
if [ "$1" = "0" ] ; then
    %{__rm} -f %{_datadir}/%{name}/media/avatars
    %{__rm} -f %{_datadir}/%{name}/%{name}/thumb
fi

%files
%{_datadir}/%{name}
%dir %{_sharedstatedir}/%{name}/avatars
%dir %attr(0755, seafile, seafile) %{_sharedstatedir}/%{name}
%dir %attr(0750, seafile, seafile) %{_sharedstatedir}/%{name}/thumb
%dir %attr(0755, seafile, seafile) %{_sharedstatedir}/%{name}/avatars/groups
%attr(0644, root, root) %{_sharedstatedir}/%{name}/avatars/groups/default.png


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.2
- 7.0.2 For fedora 40
