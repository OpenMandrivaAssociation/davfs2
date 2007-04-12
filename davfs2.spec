Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version: 	0.2.8
Release: 	%mkrel 2
License:	GPL
Group:		System/Kernel and hardware		

Source:		http://prdownloads.sourceforge.net/dav/%{name}-%{version}.tar.bz2
Url:		http://sourceforge.net/projects/dav
BuildRoot:	%_tmppath/%name-%version-root
BuildRequires:	neon-devel = 0.24.7

%description

Davfs is a Linux file system driver that allows you to mount a WebDAV 
server as a disk drive. WebDAV is an extension to HTTP/1.1 that allows 
remote collaborative authoring of Web resources, defined in RFC 2518.

%prep
%setup -q

# (sb) name clash with davfs packag, fstype is davfs2
sed -i 's|mount.davfs|mount.davfs2|g' mount.davfs.8 Makefile.in src/util.c
sed -i 's|-t davfs|-t davfs2|g' mount.davfs.8 src/util.c
sed -i 's|DAV_VFS_TYPE "davfs"|DAV_VFS_TYPE "davfs2"|g' src/util.h
mv mount.davfs.8 mount.davfs2.8

%build
# (sb) use system headers rather than kernel-source
%configure --with-ssl --with-kernel-src=%{_prefix}
%make

%install
rm -fr %buildroot
%makeinstall_std

install -d %{buildroot}/sbin
ln -sf ..%{_sbindir}/mount.%{name} %{buildroot}/sbin/mount.%{name}
install -d %{buildroot}/var/run/mount.%{name}

# (sb) handled by %%doc
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc README COPYING NEWS FAQ TODO THANKS ChangeLog secrets.template %{name}.conf.template
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/secrets
%{_sbindir}/mount.%{name}
/sbin/mount.%{name}
%{_mandir}/man8/*
%attr(1775,root,users) %dir /var/run/mount.%{name}

