%define dav_user %{name}
%define dav_group %{name}
%define dav_localstatedir /var/run
%define dav_syscachedir /var/cache

Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version: 	1.4.6
Release: 	%mkrel 1
License:	GPLv2+
Group:		System/Kernel and hardware		
URL:		http://savannah.nongnu.org/projects/davfs2
Source0:	http://ftp.twaren.net/Unix/NonGNU/%{name}/%{name}-%{version}.tar.gz
Patch2:		davfs2-1.4.0-format_not_a_string_literal_and_no_format_arguments.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	neon-devel >= 0.27
BuildRequires:	gettext-devel >= 0.14.4
BuildRequires:	libtool
Provides:	davfs = %{version}-%{release}
Obsoletes:	davfs < 0.2.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
davfs2 is a Linux file system driver that allows you to mount a WebDAV server
as a local file system, like a disk drive. This way applications can access
resources on a Web server without knowing anything about HTTP or WebDAV. davfs2
runs as a daemon in userspace. It uses the kernel file system coda or fuse.
Most propably your Linux kernel includes at least one of this file systems. To
connect to the WebDAV server it makes use of the neon library. Neon supports
TLS/SSL (using OpenSSL or GnuTLS) and access via proxy server.

davfs2 allows you to e.g.

 * use a WebDAV server as workspace for a geographically distributed work
   group.
 * save documents on a WebDAV server and access and edit them via internet from
   wherever you want.
 * edit a web site in place, using your preferred development tools.


%prep
%setup -q
%patch2 -p1 -b .fmt

%build
export dav_user=%{dav_user}
export dav_group=%{dav_group}
export dav_localstatedir=%{dav_localstatedir}
export dav_syscachedir=%{dav_syscachedir}

%configure2_5x \
    --disable-rpath \

%make

%install
rm -fr %{buildroot}

install -d %{buildroot}/sbin
install -d %{buildroot}%{dav_localstatedir}/mount.%{name}
install -d %{buildroot}%{dav_syscachedir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}

%makeinstall_std

# rename the binaries
ln -s %{_sbindir}/mount.davfs %{buildroot}%{_sbindir}/mount.%{name}
ln -s %{_sbindir}/umount.davfs %{buildroot}%{_sbindir}/umount.%{name}

rm -f %{buildroot}/sbin/*
ln -snf ..%{_sbindir}/mount.%{name} %{buildroot}/sbin/mount.%{name}
ln -snf ..%{_sbindir}/umount.%{name} %{buildroot}/sbin/umount.%{name}

# rename the manpages
find %{buildroot}%{_mandir} -name "*.gz" | xargs gunzip

%find_lang %{name} --all-name

%pre
%_pre_useradd %{dav_user} %{dav_localstatedir}/mount.%{name} /bin/false

%postun
%_postun_userdel %{dav_user}

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING FAQ NEWS README THANKS
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/certs
%dir %{_sysconfdir}/%{name}/certs/private
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/secrets
%{_sbindir}/mount.davfs*
%{_sbindir}/umount.davfs*
/sbin/mount.davfs*
/sbin/umount.davfs*
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man5/*
%lang(de) %{_mandir}/de/man8/*
%lang(es) %{_mandir}/es/man5/*
%attr(1775,root,%{dav_group}) %dir %{dav_localstatedir}/mount.%{name}
%attr(1775,root,%{dav_group}) %dir %{dav_syscachedir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
