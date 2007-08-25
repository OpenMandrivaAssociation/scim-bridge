%define version      0.4.13
%define release      %mkrel 3

%define scim_version 1.4.7

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Name:         scim-bridge
Summary:      Scim-bridge is yet another IM client of SCIM
Version:      %{version}
Release:      %{release}
Group:        System/Internationalization
License:      GPL
URL:          http://sourceforge.net/projects/scim/
Source0:      http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
# fwang: patch0 from fedora, fix rhbug#242864
Patch0:		scim-bridge-0.4.13-setlocale.patch
# fwang: patch1 from CVS, fix status change notification crash
Patch1:		scim-bridge-0.4.13-fix-status-notification.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:        %{libname} = %{version}-%{release}
Requires:        scim >= %{scim_version}
BuildRequires:   scim-devel >= %{scim_version}
BuildRequires:   automake doxygen
BuildRequires:   qt3-devel
BuildRequires:	 qt4-devel

%description
Scim-bridge is yet another IM client of SCIM.
It solves SCIM's C++ ABI problems.

%package -n %{libname}
Summary:    Scim-bridge library
Group:      System/Internationalization
Provides:   %{libname_orig} = %{version}-%{release}

%description -n %{libname}
scim-bridge library.

%package    qt3
Summary:    Scim-bridge for qt3
Group:      System/Internationalization
Requires:   %{name} = %{version}
Obsoletes:  %{name}-qt
Provides:   %{name}-qt

%description qt3
scim-bridge for qt3.

%package    qt4
Summary:    Scim-bridge for qt4
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qt4
scim-bridge for qt4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp /usr/share/automake-1.10/mkinstalldirs .
[[ ! -x configure ]] && ./bootstrap
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
rm -f %{buildroot}/%{qt3dir}/plugins/inputmethods/im-scim-bridge.{a,la}
rm -f %{buildroot}/%{qt4dir}/plugins/inputmethods/im-scim-bridge.{a,la}

mkdir -p %{buildroot}%{qt3plugins}/inputmethods/
mv %{buildroot}%{qt3dir}/plugins/inputmethods/* %{buildroot}%{qt3plugins}/inputmethods/

mkdir -p %{buildroot}%{qt4plugins}/inputmethods/
mv %{buildroot}%{qt4dir}/plugins/inputmethods/* %{buildroot}%{qt4plugins}/inputmethods/

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

%files qt3
%defattr(-,root,root)
%doc COPYING
%{qt3plugins}/inputmethods/*.so

%files qt4
%defattr(-,root,root)
%doc COPYING
%{qt4plugins}/inputmethods/*.so
