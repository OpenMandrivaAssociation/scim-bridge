%define version      0.4.16
%define release      8

%define scim_version 1.4.7

Name:         scim-bridge
Summary:      Yet another IM client of SCIM
Version:      %{version}
Release:      %{release}
Group:        System/Internationalization
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:      GPLv2+
URL:          https://sourceforge.net/projects/scim/
Source0:      http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
Patch0:		scim-bridge-0.4.15.2-use-mandriva-qt-dir.patch
Patch1:		bug-351920-should-return-retval.patch
Patch2:		scim-bridge-0.4.15.2-qt4-focus.patch
Patch3:		scim-bridge-0.4.15.2-linkage.patch
Patch4:		scim-bridge-0.4.16-gcc44.patch
Patch5:		scim-bridge-0.4.15-fix-gdm.patch
Patch6:		scim-bridge-0.4.16-fix-gtk-key-snooper.patch
Patch7:		scim-bridge-0.4.16-fixes-null-imengine.patch
Patch8:		scim-bridge-0.4.16-fixes-unistd-compile.patch
Requires:        scim >= %{scim_version}
BuildRequires:   scim-devel >= %{scim_version}
BuildRequires:   automake doxygen gettext-devel intltool
BuildRequires:	 qt4-devel
BuildRequires:   pkgconfig(gtk+-2.0)
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

%package    qt4
Summary:    Scim-bridge for qt4
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qt4
scim-bridge for qt4.

%prep
%setup -q -n scim-bridge-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1

%build
export LIBS="-lX11"
%configure2_5x --enable-agent --enable-gtk2-immodule --disable-qt3-immodule --enable-qt4-immodule
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
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

%files qt4
%defattr(-,root,root)
%{qt4plugins}/inputmethods/*.so
