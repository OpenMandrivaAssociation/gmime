%define	major 0
%define apiver 2.6
%define libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d

%define build_mono 1

%ifarch %mips %arm
%define build_mono 0
%endif

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%define _requires_exceptions libgmime
Summary:		The libGMIME library
Name:			gmime
Version:		2.6.3
Release:		1
License:		LGPLv2+
Group:			System/Libraries
URL:			http://spruce.sourceforge.net/gmime
Source0:		http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.xz
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libz-devel
BuildRequires:	gpgme-devel
%if %{build_mono}
BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2
%endif

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries
Obsoletes:	%mklibname %{name} 2.0
Provides:	%mklibname %{name} 2.0
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{develname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	%{name}-devel
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 2.0 -d
Provides:	%mklibname %{name} 2.0 -d

%description -n %{develname}
This package contains the lib%{name} development library and its header files.

%if %{build_mono}
%package sharp
Summary:	GMIME# bindings for mono
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
rm -rf %{buildroot}
%makeinstall_std

# cleanup
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

# these are provided by sharutils, gotta rename them...
mv %{buildroot}%{_bindir}/uudecode %{buildroot}%{_bindir}/gmime-uudecode
mv %{buildroot}%{_bindir}/uuencode %{buildroot}%{_bindir}/gmime-uuencode

%files -n %{name}-utils
%{_bindir}/gmime-uudecode
%{_bindir}/gmime-uuencode

%files -n %{libname}
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%doc AUTHORS ChangeLog PORTING README TODO
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gmime-%{apiver}.pc
%{_includedir}/*
%doc %{_gtkdocdir}/*

%if %{build_mono}
%files sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/%{name}-sharp
%{_prefix}/lib/mono/%{name}-sharp-%{apiver}
%{_libdir}/pkgconfig/%{name}-sharp-%{apiver}.pc
%endif
