%global _hardened_build 1
%define _release 1

Name:           ccnet
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
BuildRequires:  libsearpc-devel >= 3.1
BuildRequires:  libevent-devel >= 2.0
BuildRequires:  intltool
BuildRequires:  libarchive-devel
BuildRequires:  jansson-devel
BuildRequires:  vala
#BuildRequires: vala-devel
BuildRequires:  fuse-devel
BuildRequires:  libcurl-devel
BuildRequires:  libzdb-devel
BuildRequires:  postgresql15-devel


Requires:       libcurl >= 7.0
Requires:       libevent >= 2.0
Requires:       jansson
Requires:       openssl-libs
Requires:       libuuid
Requires:       python2 >= 2.7
Requires:       glib2 >= 2.5
Requires:       fuse-libs
Requires:       libzdb
Requires:       libarchive


Requires:       libsearpc >= 3.1
Requires:       postgresql-libs


%description
Seafile is a next-generation open source cloud storage system with
advanced support for file syncing, privacy protection and teamwork.


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
sed -i -e /\(DESTDIR\)/d lib%{name}.pc.in


%build
./autogen.sh --enable-server --enable-client
export PYTHON=python2
%configure --disable-static --with-postgresql=/usr/pgsql-11/bin/pg_config --disable-compile-demo
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"


%install
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# default ccnet data dir
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}


%check
# tests are failing on big endian arches
# https://bugzilla.redhat.com/show_bug.cgi?id=1388453
%{__make} check


%post -p /sbin/ldconfig


%files
%doc README.markdown
%{_libdir}/lib%{name}.so.*
%{python2_sitearch}/%{name}
%{_bindir}/%{name}-init
%{_bindir}/%{name}-server
%dir %attr(0755,seafile,seafile) %{_sharedstatedir}/%{name}


%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/*



%changelog
* Wed May 22 2024 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.2
- Update 7.0.2 For fedora 40

* Tue Mar 26 2019 Lolizeppelin <lolizeppelin@gmail.com> - 7.0.0
- Update to 7.0.0

* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 6.3.4
- Update to 6.3.4

