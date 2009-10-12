%define api 1.12
%define lib_major 0
%define lib_name %mklibname glom %api %{lib_major}
%define develname %mklibname -d glom

Summary:	Easy-to-use database designer and user interface
Name:		glom
Version:	1.12.2
Release:	%mkrel 1
Group:		Development/Databases
License:	GPLv2+
URL:		http://www.glom.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glom/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libbakery2.6-devel
BuildRequires:	desktop-file-utils gettext intltool
BuildRequires:	libgdamm4-devel >= 3.99.15
BuildRequires:	gda4.0-devel >= 4.0.4
%py_requires -d
BuildRequires:	gnome-python-gda gnome-python-gda-devel >= 2.25.2
BuildRequires:	libgnomecanvasmm2.6-devel >= 2.10
BuildRequires:	libgnome2-devel >= 2.6.0
BuildRequires:	libxslt-devel >= 1.1.10
BuildRequires:	pygtk2.0-devel >= 2.6
BuildRequires:	gnome-doc-utils
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel
BuildRequires:	iso-codes
BuildRequires:	libxslt-proc
BuildRequires:	postgresql-devel postgresql-plpython postgresql-server postgresql-plpython postgresql-plpgsql postgresql-pl postgresql-contrib-virtual
BuildRequires:	gettext-devel
BuildRequires:	gnome-python-extras
BuildRequires:	libepc-devel
BuildRequires:	goocanvasmm-devel >= 0.13.0
BuildRequires:	libgtksourceviewmm-2.0-devel
BuildRequires:	avahi-ui-devel
Requires:	gnome-python-gda
Requires:	libgda4.0-postgres
Requires:	postgresql-virtual postgresql-plpython postgresql-server postgresql-plpython postgresql-plpgsql postgresql-pl postgresql-contrib-virtual

%description
Glom lets you design database systems - the database and the user
interface. Glom has high-level features such as relationships,
lookups, related fields, related records, calculated fields, drop-down
choices, searching, reports, users and groups. It has Numeric, Text,
Date, Time, Boolean, and Image field types. Glom systems require
almost no programming, but you may use Python for calculated fields or
buttons. Glom uses the postgresql8.2 database backend.

%package -n %{lib_name}
Summary:	A support library for accessing Glom data
Group:		System/Libraries
Obsoletes:	%mklibname glom-1_ 0

%description -n %{lib_name}
A support library for accessing Glom data.

%package -n %{develname}
Summary:        Development files for Glom
Group:          Development/Other
Conflicts:	%name < 0.17.1
Requires:	%{lib_name} = %version

%description -n %{develname}
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
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

#rm -f ${RPM_BUILD_ROOT}%{_libdir}/libglom.so

%if %mdkversion < 200900
%post
%update_scrollkeeper
%{update_desktop_database}
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%{clean_desktop_database}
%clean_mime_database
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{py_platsitedir}/%{name}_1_12.so
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/omf/%{name}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libglom-%api.so.%{lib_major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libglom-%api.so
%_includedir/%name-%api
%_libdir/pkgconfig/%name-%api.pc
