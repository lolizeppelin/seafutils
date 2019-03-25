%global _hardened_build 1
%global sname seaf

Name:           seafile
Version:        6.3.4
Release:        2%{?dist}
Summary:        A simple and easy-to-use C language RPC framework

License:        LGPLv3
URL:            https://github.com/haiwen/%{name}
Source0:        %{name}-server-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  openssl-devel
BuildRequires:  libuuid-devel
BuildRequires:  python2-devel
BuildRequires:  postgresql-devel
BuildRequires:  mysql-devel
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

#Requires:       libevhtp = 1.1.6
Requires:       mariadb-connector-c
Requires:       postgresql-libs
Requires:       libcurl >= 7.0
Requires:       libevent >= 2.0
Requires:       jansson
Requires:       openssl-libs
Requires:       libuuid
Requires:       python2 >= 2.7
Requires:       glib2 >= 2.5

Requires:       ccnet = %{version} 
Requires:       libsearpc >= 3.1



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
%configure --disable-static --disable-compile-demo \
    --with-mysql=/usr/bin/mysql_config  \
    --with-postgresql=/usr/bin/pg_config


%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"


%install
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
#sed -i -e 's|%{buildroot}||g' %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc


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
%{_bindir}/%{sname}-fsck
%{_bindir}/%{sname}-fuse
%{_bindir}/%{sname}-migrate
%{_bindir}/%{sname}-server
%{_bindir}/%{sname}-server-init
%{_bindir}/%{sname}serv-gc
%{python2_sitearch}/seaserv

%files devel
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/*


%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 6.3.4
- Update to 6.3.4
