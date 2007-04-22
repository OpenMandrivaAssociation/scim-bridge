%define version      0.4.10
%define release      %mkrel 2

%define scim_version 1.4.5

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Name:         scim-bridge
Summary:      Scim-bridge is yet another IM client of SCIM
Version:      %{version}
Release:      %{release}
Group:        System/Internationalization
License:      GPL
URL:          http://sourceforge.jp/projects/scim-imengine/
Source0:      %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:        %{libname} = %{version}
Requires:        scim >= %{scim_version}
BuildRequires:   scim-devel >= %{scim_version}
BuildRequires:   automake1.8 doxygen
BuildRequires:   qt3-devel

%description
Scim-bridge is yet another IM client of SCIM.
It solves SCIM's C++ ABI problems.


%package -n %{libname}
Summary:    Scim-bridge library
Group:      System/Internationalization
Provides:   %{libname_orig} = %{version}-%{release}

%description -n %{libname}
scim-bridge library.

%package    qt
Summary:    Scim-bridge for qt
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qt
scim-bridge for qt.


%prep
%setup -q
cp /usr/share/automake-1.9/mkinstalldirs .

%build
[[ ! -x configure ]] && ./bootstrap
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
rm -f %{buildroot}/%_prefix/lib/qt3/plugins/inputmethods/im-scim-bridge.{a,la}

mkdir -p %{buildroot}%{qt3plugins}/inputmethods/
mv %{buildroot}%{qt3dir}/plugins/inputmethods/*.so %{buildroot}%{qt3plugins}/inputmethods/

%clean
rm -rf $RPM_BUILD_ROOT


%post -n %{libname}
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun -n %{libname}
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/scim-bridge

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/gtk-2.0/immodules/*.so

%files qt
%defattr(-,root,root)
%doc COPYING
%{qt3plugins}/inputmethods/*.so


