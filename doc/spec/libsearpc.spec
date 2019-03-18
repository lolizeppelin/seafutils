%global _hardened_build 1

Name:           libsearpc
Version:        3.1
Release:        11%{?dist}
Summary:        A simple and easy-to-use C language RPC framework

License:        LGPLv3
URL:            https://github.com/haiwen/%{name}
#Source0:        https://github.com/haiwen/%{name}/archive/v%{version}-latest.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  jansson-devel
BuildRequires:  pygobject2
BuildRequires:  python2-simplejson
BuildRequires:  python2-devel


%description
Searpc is a simple C language RPC framework based on GObject system. Searpc
handles the serialization/deserialization part of RPC, the transport part is
left to users.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       jansson-devel >= 2.2.1


%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%prep
%setup -qn %{name}-%{version}-latest
sed -i -e /\(DESTDIR\)/d %{name}.pc.in


%build
./autogen.sh
%configure --disable-static --disable-compile-demo
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"


%install
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%check
# tests are failing on big endian arches
# https://bugzilla.redhat.com/show_bug.cgi?id=1388453
%ifnarch ppc ppc64 s390 s390x
%{__make} check
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS README.markdown
%license COPYING
%{_libdir}/%{name}.so.*
%{_bindir}/searpc-codegen.py
%{python2_sitearch}/pysearpc/

%files devel
%license COPYING
%{_includedir}/searpc*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Aug 14 2017 Iryna Shcherbina <ishcherb@redhat.com> - 3.1-7
- Add a build-time dependency on python2-devel

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Dan Horák <dan[at]danny.cz> - 3.1-3
- Skip the tests in a better way

* Tue Nov 08 2016 Julien Enselme <jujens@jujens.eu> - 3.1-2
- Skip failing tests on ppc64 and s390

* Sun Oct 23 2016 Julien Enselme <jujens@jujens.eu> - 3.1-1
- Update to 3.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Feb 02 2016 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Fri Dec 04 2015 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-6
- Add optflags

* Fri Sep 11 2015 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-5
- Fix license

* Fri Sep 11 2015 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-4
- Fix license
- Fix build requiremets
- Add check

* Sat Apr 11 2015 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-3
- Use release tag instead of commit

* Wed Nov 05 2014 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-2
- Update to latest tag
- Remove merged patch

* Tue Aug 12 2014 Nikos Roussos <comzeradd@fedoraproject.org> - 3.0-1
- Initial version of the package
