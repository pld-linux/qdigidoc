%define		qtver	4.4.0
Summary:	Estonian digital signature application
Name:		qdigidoc
Version:	3.12.6
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://github.com/open-eid/qdigidoc/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b0a989d846f76901bc2951e17622fe12
Patch0:		desktop.patch
URL:		https://github.com/open-eid/
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	libdigidocpp-devel >= 3.9
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.596
Requires(post,postun):	gtk-update-icon-cache
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	libdigidocpp >= 3.9
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

%build
install -d build
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
