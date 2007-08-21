%define major_version 1.4
%define minor_version 4
%define lib_major 0
%define lib_name %mklibname glom-1_ %{lib_major}

Name:           glom
Version:        %{major_version}.%{minor_version}
Release:        %mkrel 1
Summary:        Easy-to-use database designer and user interface.
Group:          Development/Databases
License:        GPL
URL:            http://www.glom.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glom/%{major_version}/%{name}-%{major_version}.%{minor_version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  bakery-devel >= 2.4
BuildRequires:  desktop-file-utils gettext intltool
BuildRequires:  libgdamm-devel >= 1.3.7
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  gnome-python-gda gnome-python-gda-devel
BuildRequires:  libgnomecanvasmm2.6-devel >= 2.10
BuildRequires:  libgnome2-devel >= 2.6.0
BuildRequires:  libxslt-devel >= 1.1.10
BuildRequires:  pygtk2.0-devel >= 2.6
BuildRequires:  gnome-doc-utils
BuildRequires:  scrollkeeper
BuildRequires:  startup-notification-devel
BuildRequires:  iso-codes
BuildRequires: libxslt-proc
BuildRequires: libgtksourceviewmm-devel
BuildRequires: postgresql postgresql-contrib postgresql-devel postgresql-pl postgresql-plpgsql postgresql-plpython postgresql-server
BuildRequires: gettext-devel
BuildRequires: gnome-python-extras

Requires: gda1.2-postgres
Requires: postgresql postgresql-contrib postgresql-devel postgresql-pl postgresql-plpgsql postgresql-plpython postgresql-server

Requires(post):   shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
Requires(post):   scrollkeeper
Requires(postun): scrollkeeper


%description
Glom lets you design database systems - the database and the user
interface. Glom has high-level features such as relationships,
lookups, related fields, related records, calculated fields, drop-down
choices, searching, reports, users and groups. It has Numeric, Text,
Date, Time, Boolean, and Image field types. Glom systems require
almost no programming, but you may use Python for calculated fields or
buttons. Glom uses the PostgreSQL database backend.

%package -n     %{lib_name}
Summary:        %{Summary}
Group:          System/Libraries

%description -n %{lib_name}
A support library for accessing Glom data.

%prep
%setup -q

%build
%configure \
        --disable-dependency-tracking \
        --disable-static \
        --disable-update-mime-database \
        --disable-scrollkeeper \
        --disable-rpath \
	--with-postgres-utils=/usr/bin
%make


%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall_std
#make install DESTDIR=${RPM_BUILD_ROOT}
%find_lang %{name}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Databases" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#rm -f ${RPM_BUILD_ROOT}%{_libdir}/libglom.so

%post
%update_scrollkeeper
%{update_desktop_database}
%update_mime_database
%update_icon_cache hicolor

%postun
%clean_scrollkeeper
%{clean_desktop_database}
%clean_mime_database
%clean_icon_cache hicolor

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/%{name}
%{_libdir}/libglom.so
%{_libdir}/python2.5/site-packages/%{name}.so
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mime-info/*
%{_datadir}/omf/%{name}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*
