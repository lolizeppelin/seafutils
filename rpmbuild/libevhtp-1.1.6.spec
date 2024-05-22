Name:		libevhtp
Version:	1.1.6
Release:        0%{?dist}
Summary:	A more flexible replacement for libevent's http API
License:	BSD
Group:		System/Libraries
Url:		https://github.com/ellzey/libevhtp
Source0:	https://github.com/ellzey/libevhtp/archive/%{version}/%{name}-%{version}.tar.gz
Patch1:         %{name}-%{version}-makefile.patch
BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libevent)
BuildRequires:  gcc-c++ 

%description
Libevhtp was created as a replacement API for Libevent's current
HTTP API. The reality of libevent's http interface is that it
was created as a JIT server, meaning the developer never thought
of it being used for creating a full-fledged HTTP service.
Infact I am under the impression that the libevent http API was
designed almost as an example of what you can do with libevent.
It's not Apache in a box, but more and more developers are
attempting to use it as so.

#----------------------------------------------------

%package 	devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	evhtp-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description    devel
The devel  package contains libraries and header files for
developing applications that use %{name}.

#----------------------------------------------------

%prep
%setup -q
%patch 1 -p0


%build
%{__cmake} -DEVHTP_DISABLE_SSL=ON -DCMAKE_INSTALL_PREFIX=/usr
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"

%install
%make_install

%files 
%{_prefix}/lib/libevhtp.so


%files devel
%doc ChangeLog README.markdown
%doc LICENSE
%{_prefix}/lib/libevhtp.a
%{_includedir}/*.h


%changelog
* Sun May 19 2024 Lolizeppelin <lolizeppelin@gmail.com>        Version:	1.1.6
- update sepc and patch file for fedora 40

* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com>        Version:	1.1.6
- update to 1.1.6 for seafile server
