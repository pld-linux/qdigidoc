%define		qtver	5.8.0
Summary:	Estonian digital signature application
Name:		qdigidoc
Version:	3.13.6
Release:	0.1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://github.com/open-eid/qdigidoc/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3e8de77f166b56670af489e81c7c46d3
Source1:	https://id.eesti.ee/config.json
# Source1-md5:	63f710daa62f532d9d43d4631e431295
Source2:	https://id.eesti.ee/config.rsa
# Source2-md5:	d3b47de630a20013a8bab464045b5607
Source3:	https://id.eesti.ee/config.pub
# Source3-md5:	b3931bf5a8a2f19cb00e53afd89e440d
Source4:	TSL.qrc
Source5:	config.qrc
Source6:	https://ec.europa.eu/information_society/policy/esignature/trusted-list/tl-mp.xml
# Source6-md5:	45964706ced57279f3ae8d71d9f63831
Source7:	EE.xml
# Source7-md5:	e15d2f875b47365970ced4697843e7c1
Patch0:		desktop.patch
Patch1:		sandbox-compilation.patch
URL:		https://github.com/open-eid/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5PrintSupport-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	libdigidocpp-devel >= 3.12
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	qt5-qmake >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.596
Requires(post,postun):	gtk-update-icon-cache
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QDigiDoc is an application for digitally signing and encrypting
documents in BDoc, DDoc, and CDoc container formats. These file
formats are widespread in Estonia where they are used for storing
legally binding digital signatures.

%package -n nautilus-%{name}
Summary:	Nautilus extension for %{name}
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-python >= 1.0
Requires:	python-pygobject

%description -n nautilus-%{name}
This package contains the qdigidoc extension for the nautilus file
manager.

%package -n kde4-konqueror-plugin-%{name}
Summary:	Konqueror extension for %{name}
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description -n kde4-konqueror-plugin-%{name}
This package contains the qdigidoc extension for Konqueror.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

install -d build/{common,client}
cp %{SOURCE1} build/common
cp %{SOURCE2} build/common
cp %{SOURCE3} build/common
cp %{SOURCE4} build/client
cp %{SOURCE5} build/common
cp %{SOURCE6} build/client
cp %{SOURCE7} build/client

%build
cd build
%cmake \
%ifarch %{arm} %{ix86} %{x8664}
	-DBREAKPAD=OFF \
%endif
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang nautilus-qdigidoc

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/qdigidoc-client.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/qdigidoc-crypto.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/qdig*
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/mime/packages/*.xml
%{_datadir}/appdata/qdigidoc-client.appdata.xml
%{_datadir}/appdata/qdigidoc-cypto.appdata.xml

%files -n nautilus-%{name} -f nautilus-qdigidoc.lang
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/*.py

%files -n kde4-konqueror-plugin-%{name}
%defattr(644,root,root,755)
%{_datadir}/kde4/services/*.desktop
