%define PROGRAM_NAME mount.%{name}
%define dav_user %{name}
%define dav_group %{name}
%define dav_localstatedir /var/run
%define dav_syscachedir /var/cache

Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version: 	1.3.2
Release: 	%mkrel 4
License:	GPL
Group:		System/Kernel and hardware		
URL:		http://sourceforge.net/projects/dav
Source0:	http://prdownloads.sourceforge.net/dav/%{name}-%{version}.tar.gz
Patch0:		davfs2-PROGRAM_NAME.diff
Patch1:		davfs2-glibc27.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	neon-devel >= 0.27
BuildRequires:	gettext-devel >= 0.14.4
BuildRequires:	libtool
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
%patch0 -p1
%patch1 -p0

%build
libtoolize --copy --force; aclocal -I config; autoheader; automake --add-missing --force-missing; autoheader; autoconf

export PROGRAM_NAME=%{PROGRAM_NAME}
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
mv %{buildroot}%{_sbindir}/mount.davfs %{buildroot}%{_sbindir}/mount.%{name}
mv %{buildroot}%{_sbindir}/umount.davfs %{buildroot}%{_sbindir}/umount.%{name}

rm -f %{buildroot}/sbin/*
ln -snf ..%{_sbindir}/mount.%{name} %{buildroot}/sbin/mount.%{name}
ln -snf ..%{_sbindir}/umount.%{name} %{buildroot}/sbin/umount.%{name}

# rename the manpages
find %{buildroot}%{_mandir} -name "*.gz" | xargs gunzip
mv %{buildroot}%{_mandir}/man8/mount.davfs.8 %{buildroot}%{_mandir}/man8/mount.%{name}.8
mv %{buildroot}%{_mandir}/man8/umount.davfs.8 %{buildroot}%{_mandir}/man8/umount.%{name}.8
mv %{buildroot}%{_mandir}/de/man8/mount.davfs.8 %{buildroot}%{_mandir}/de/man8/mount.%{name}.8
mv %{buildroot}%{_mandir}/de/man8/umount.davfs.8 %{buildroot}%{_mandir}/de/man8/umount.%{name}.8

%find_lang %{name} --all-name

%pre
%_pre_useradd %{dav_user} %{dav_localstatedir}/mount.%{name} /bin/false

%postun
%_postun_userdel %{dav_user}

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING FAQ INSTALL.davfs2 NEWS README THANKS
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/certs
%dir %{_sysconfdir}/%{name}/certs/private
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/secrets
%{_sbindir}/mount.%{name}
%{_sbindir}/umount.%{name}
/sbin/mount.%{name}
/sbin/umount.%{name}
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man5/*
%lang(de) %{_mandir}/de/man8/*
%lang(es) %{_mandir}/es/man5/*
%attr(1775,root,%{dav_group}) %dir %{dav_localstatedir}/mount.%{name}
%attr(1775,root,%{dav_group}) %dir %{dav_syscachedir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
