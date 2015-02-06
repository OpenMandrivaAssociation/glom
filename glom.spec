%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api	1.22
%define major	0
%define libname	%mklibname glom %{api} %{major}
%define devname	%mklibname -d glom
%define postgresql 9.0

Summary:	Easy-to-use database designer and user interface
Name:		glom
Version:	1.22.1
Release:	2
Group:		Development/Databases
License:	GPLv2+
URL:		http://www.glom.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glom/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	python-sphinx
BuildRequires:	xsltproc
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(evince-view-3.0)
BuildRequires:	pkgconfig(giomm-2.4) >= 2.31.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(goocanvasmm-2.0) >= 1.90.3
BuildRequires:	pkgconfig(gtkmm-3.0) >= 2.99.1
BuildRequires:	pkgconfig(gtksourceviewmm-3.0) >= 3.0.0
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libepc-1.0)
BuildRequires:	pkgconfig(libgdamm-4.0)
BuildRequires:	pkgconfig(libgda-4.0)
BuildRequires:	pkgconfig(libgda-postgres-4.0)
BuildRequires:	pkgconfig(libgda-sqlite-4.0)
BuildRequires:	pkgconfig(libxml++-2.6) >= 2.23.1
BuildRequires:	pkgconfig(libxslt) >= 1.1.10
BuildRequires:	pkgconfig(pygobject-3.0) >= 2.29.0
BuildRequires:	postgresql%{postgresql}-devel
BuildRequires:	postgresql%{postgresql}-plpython
BuildRequires:	postgresql%{postgresql}-server
BuildRequires:	postgresql%{postgresql}-plpython
BuildRequires:	postgresql%{postgresql}-plpgsql
BuildRequires:	postgresql%{postgresql}-pl
BuildRequires:	postgresql%{postgresql}-contrib
Requires:	gnome-python-gda
Requires:	libgda4.0-postgres
Requires:	postgresql%{postgresql}
Requires:	postgresql%{postgresql}-plpython
Requires:	postgresql%{postgresql}-server
Requires:	postgresql%{postgresql}-plpython
Requires:	postgresql%{postgresql}-plpgsql
Requires:	postgresql%{postgresql}-pl
Requires:	postgresql%{postgresql}-contrib

%description
Glom lets you design database systems - the database and the user
interface. Glom has high-level features such as relationships,
lookups, related fields, related records, calculated fields, drop-down
choices, searching, reports, users and groups. It has Numeric, Text,
Date, Time, Boolean, and Image field types. Glom systems require
almost no programming, but you may use Python for calculated fields or
buttons. Glom uses the postgresql%{postgresql} database backend.

%package -n %{libname}
Summary:	A support library for accessing Glom data
Group:		System/Libraries
Obsoletes:	%mklibname glom-1_ 0

%description -n %{libname}
A support library for accessing Glom data.

%package -n %{devname}
Summary:        Development files for Glom
Group:          Development/Other
Conflicts:	%{name} < 0.17.1
Requires:	%{libname} = %{version}

%description -n %{devname}
Development files for Glom.

%prep
%setup -q

%build
%configure2_5x \
        --disable-dependency-tracking \
        --disable-static \
        --disable-update-mime-database \
        --disable-scrollkeeper \
	--with-postgres-utils=%{_bindir}

%make

%install
%makeinstall_std
%find_lang %{name}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install \
	--remove-category="Application" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{py_platsitedir}/%{name}_1_18.so
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml

%files -n %{libname}
%{_libdir}/libglom-%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/libglom-%{api}.so
%{_includedir}/%{name}-%{api}
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%doc %{_datadir}/doc/pyglom*
%doc %{_datadir}/doc/libglom-%{api}
%doc %{_datadir}/devhelp/books/*
