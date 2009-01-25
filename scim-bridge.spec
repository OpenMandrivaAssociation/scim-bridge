%define version      0.4.15.2
%define release      %mkrel 1

%define scim_version 1.4.7

Name:         scim-bridge
Summary:      Yet another IM client of SCIM
Version:      %{version}
Release:      %{release}
Group:        System/Internationalization
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:      GPLv2+
URL:          http://sourceforge.net/projects/scim/
Source0:      http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
Patch0:		scim-bridge-0.4.15.2-use-mandriva-qt-dir.patch
Patch1:		bug-351920-should-return-retval.patch
Patch2:		scim-bridge-0.4.15.2-qt4-focus.patch
Patch3:		scim-bridge-0.4.15.2-linkage.patch
Requires:        scim-common >= %{scim_version}
BuildRequires:   scim-devel >= %{scim_version}
BuildRequires:   automake doxygen gettext-devel intltool
BuildRequires:   qt3-devel
BuildRequires:	 qt4-devel
Provides:        scim-client = %{scim_api}
Suggests:        %name-gtk = %{version}-%{release}

%description
Scim-bridge is yet another IM client of SCIM.
It solves SCIM's C++ ABI problems.

%package gtk
Summary:    Scim-bridge gtk immodule
Group:      System/Internationalization
Obsoletes:   %mklibname scim-bridge 0

%description gtk
scim-bridge gtk immodule.

%package    qt3
Summary:    Scim-bridge for qt3
Group:      System/Internationalization
Requires:   %{name} = %{version}
Obsoletes:  %{name}-qt

%description qt3
scim-bridge for qt3.

%package    qt4
Summary:    Scim-bridge for qt4
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qt4
scim-bridge for qt4.

%prep
%setup -q -n scim-bridge-0.4.15
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
%configure2_5x --enable-agent --enable-gtk2-immodule --enable-qt3-immodule --enable-qt4-immodule
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
rm -f %{buildroot}/%{qt3plugins}/inputmethods/im-scim-bridge.{a,la}
rm -f %{buildroot}/%{qt4plugins}/inputmethods/im-scim-bridge.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk
%if %mdkversion < 200900
/sbin/ldconfig
%endif
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk
%if %mdkversion < 200900
/sbin/ldconfig
%endif
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/scim-bridge

%files gtk
%defattr(-,root,root)
%{_libdir}/gtk-2.0/immodules/*.so

%files qt3
%defattr(-,root,root)
%{qt3plugins}/inputmethods/*.so

%files qt4
%defattr(-,root,root)
%{qt4plugins}/inputmethods/*.so
