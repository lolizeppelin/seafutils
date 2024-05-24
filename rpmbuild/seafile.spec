%global _hardened_build 1
%global _exe_prefix seaf
%define _release 1


Name:           seafile
Version:        7.0.2
Release:        %{_release}%{?dist}
Summary:        A simple and easy-to-use C language RPC framework

License:        LGPLv3
URL:            https://github.com/haiwen/%{name}-server
Source0:        %{name}-server-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  openssl-devel
BuildRequires:  libuuid-devel
BuildRequires:  python2-devel
BuildRequires:  sqlite-devel
BuildRequires:  libevent-devel >= 2.0
BuildRequires:  intltool
BuildRequires:  libarchive-devel
BuildRequires:  jansson-devel
BuildRequires:  vala
BuildRequires:  fuse-devel
BuildRequires:  libcurl-devel
BuildRequires:  libzdb-devel

BuildRequires:  libevhtp-devel = 1.1.6
BuildRequires:  libsearpc-devel >= 3.1
BuildRequires:  ccnet-devel = %{version}
BuildRequires:  postgresql15-devel


Requires:       libcurl >= 7.0
Requires:       libevent >= 2.0
Requires:       jansson
Requires:       openssl-libs
Requires:       libuuid
Requires:       python2 >= 2.7
Requires:       glib2 >= 2.5

Requires:       ccnet = %{version}
Requires:       libsearpc >= 3.1
Requires:       postgresql-libs


%description
Seafile is a next-generation open source cloud storage system with
advanced support for file syncing, privacy protection and teamwork.

%package        server
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       fuse-libs
Requires:       libzdb
Requires:       libarchive



%description    server
This is the core component of Seafile server. It provides RPC to
the web front-end (Seahub) to access files, and provides HTTP APIs
to the desktop clients for syncing files.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       jansson-devel >= 2.2.1


%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%prep
%setup -qn %{name}-server-%{version}-server
sed -i -e /\(DESTDIR\)/d lib/lib%{name}.pc.in


%build
./autogen.sh --enable-server --enable-client
export PYTHON=python2
%configure --disable-static  --with-postgresql=/usr/pgsql-11/bin/pg_config --disable-compile-demo
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"


%install
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# default seafile data dir
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}

# shebangs 修正
sed -i '1c\#!/usr/bin/python2' %{buildroot}%{_bindir}/%{name}-admin



%check
# tests are failing on big endian arches
# https://bugzilla.redhat.com/show_bug.cgi?id=1388453
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README.markdown
%doc doc/seafile-tutorial.doc
%{python2_sitearch}/%{name}

%files server
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-controller
%{_bindir}/%{_exe_prefix}-fsck
%{_bindir}/%{_exe_prefix}-fuse
%{_bindir}/%{_exe_prefix}-migrate
%{_bindir}/%{_exe_prefix}-server
%{_bindir}/%{_exe_prefix}-server-init
%{_bindir}/%{_exe_prefix}serv-gc
%{python2_sitearch}/seaserv
%defattr(0750,seafile,seafile,-)
%dir %{_sharedstatedir}/%{name}


%files devel
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/*


%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.2
- Update 7.0.2 For fedora 40


* Tue Mar 26 2019 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.0
- Update to 7.0.0


* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 6.3.4
- Update to 6.3.4

