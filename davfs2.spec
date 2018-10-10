%define dav_user %{name}
%define dav_group %{name}
%define dav_localstatedir %{_rundir}
%define dav_syscachedir %{_var}/cache

Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version:	1.5.4
Release:	3
License:	GPLv2+
Group:		System/Kernel and hardware		
Url:		http://savannah.nongnu.org/projects/davfs2
Source0:	http://ftp.twaren.net/Unix/NonGNU/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(neon)
BuildRequires:	rpm-helper
Requires(pre,postun):	rpm-helper
Provides:	davfs = %{version}-%{release}

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

%build
export dav_user=%{dav_user}
export dav_group=%{dav_group}
export dav_localstatedir=%{dav_localstatedir}
export dav_syscachedir=%{dav_syscachedir}

%configure

%make

%install
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

%files -f %{name}.lang
%doc AUTHORS COPYING FAQ NEWS README THANKS
%doc %{_docdir}/%{name}/BUGS
%doc %{_docdir}/%{name}/ChangeLog
%doc %{_docdir}/%{name}/INSTALL
%doc %{_docdir}/%{name}/README.translators
%doc %{_docdir}/%{name}/TODO
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/certs
%dir %{_sysconfdir}/%{name}/certs/private
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/secrets
%{_sbindir}/mount.davfs*
%{_sbindir}/umount.davfs*
/sbin/mount.davfs*
/sbin/umount.davfs*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man5/*
%lang(de) %{_mandir}/de/man8/*
%lang(es) %{_mandir}/es/man5/*
%attr(1775,root,%{dav_group}) %dir %{dav_localstatedir}/mount.%{name}
%attr(1775,root,%{dav_group}) %dir %{dav_syscachedir}/%{name}

