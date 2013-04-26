%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major	0
%define apiver	2.6
%define libname	%mklibname %{name} %{apiver} %{major}
%define devname %mklibname %{name} -d

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%define build_mono 1

%ifarch %mips %arm
%define build_mono 0
%endif

Summary:	The libGMIME library
Name:		gmime
Version:	2.6.13
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://spruce.sourceforge.net/gmime
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	gpgme-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(zlib)
%if %{build_mono}
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
%endif

%description
This library allows you to manipulate MIME messages.

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{devname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	%{name}-devel
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the lib%{name} development library and its header files.

%if %{build_mono}
%package sharp
Summary:	GMIME bindings for mono
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description sharp
This library allows you to manipulate MIME messages.
%endif

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc

#gw parallel build broken in 2.1.15
# (tpg) mono stuff doesn't like parallel build, this solves it
%(echo %make|perl -pe 's/-j\d+/-j1/g')

%check
make check

%install
%makeinstall_std

# cleanup
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

%files -n %{libname}
%{_libdir}/libgmime-%{apiver}.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog PORTING README TODO
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gmime-%{apiver}.pc
%{_includedir}/*
%{_datadir}/gapi-2.0/gmime-api.xml
%doc %{_gtkdocdir}/*

%if %{build_mono}
%files sharp
%{_prefix}/lib/mono/gac/%{name}-sharp
%{_prefix}/lib/mono/%{name}-sharp-%{apiver}
%{_libdir}/pkgconfig/%{name}-sharp-%{apiver}.pc
%endif

