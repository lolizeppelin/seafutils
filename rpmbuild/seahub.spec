%global debug_package %{nil}
%define _release 1


Name:           seahub
Version:        7.0.2
Release:        %{_release}%{?dist}
Summary:        Seahub is the web frontend for Seafile.

License:        LGPLv3
URL:            https://github.com/haiwen/%{name}
Source0:        %{name}-%{version}-server.tar.gz
# 打包好的三方库
Source1:        %{name}-3rd.tar.gz
# sql初始化文件
Source2:        seahub.postgres.sql

Requires:       python2 >= 2.7
Requires:       libsearpc >= 3.1
Requires:       python2-psycopg2 >= 2.0
# 禁止自动依赖生成
AutoReqProv:    no


%description
Seafile is a next-generation open source cloud storage system with
advanced support for file syncing, privacy protection and teamwork.


%prep

%build

%install
%{__mkdir} -p 0755 %{buildroot}%{_datadir}
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}

# 拷贝程序文件
tar -xf %{SOURCE0} -C %{buildroot}%{_datadir}/
mv %{buildroot}%{_datadir}/%{name}-%{version}-server %{buildroot}%{_datadir}/%{name}
# third part复制
tar -xf %{SOURCE1} -C %{buildroot}%{_datadir}/%{name}/thirdpart
# sql 文件复制
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/sql/postgres.sql


# 头像
cp -ap %{buildroot}%{_datadir}/%{name}/media/avatars %{buildroot}%{_sharedstatedir}/%{name}/avatars
rm -rf %{buildroot}%{_datadir}/%{name}/media/avatars
# 缩略图
%{__mkdir} %{buildroot}%{_sharedstatedir}/%{name}/thumb

# shebangs 修正
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/avatar_migration.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/batch-delete.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/gen-tarball.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/seahub-admin.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/secret_key_generator.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/tools/update-seahub-db_0.9.4_to_0.9.5.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/manage.py
# third part shebangs
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/thirdpart/bin/chardetect
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/thirdpart/gunicorn
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/thirdpart/gunicorn_paster
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/thirdpart/django/bin/django-admin.py
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_datadir}/%{name}/thirdpart/django/conf/project_template/manage.py-tpl


%post
# 创建软连接
ln -s -f %{_sharedstatedir}/%{name}/avatars %{_datadir}/%{name}/media/avatars
ln -s -f %{_sharedstatedir}/%{name}/thumb %{_datadir}/%{name}/seahub/thumbnail/thumb


%preun
# 删除软连接
if [ "$1" = "0" ] ; then
    %{__rm} -f %{_datadir}/%{name}/media/avatars
    %{__rm} -f %{_datadir}/%{name}/seahub/thumbnail/thumb
fi

%files
%{_datadir}/%{name}
%defattr(-,seafile,seafile,-)
%{_sharedstatedir}/%{name}

%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.2
- 7.0.2 For fedora 40
