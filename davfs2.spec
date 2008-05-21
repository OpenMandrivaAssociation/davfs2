Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version: 	1.3.2
Release: 	%mkrel 1
License:	GPL
Group:		System/Kernel and hardware		
URL:		http://sourceforge.net/projects/dav
Source0:	http://prdownloads.sourceforge.net/dav/%{name}-%{version}.tar.gz
Patch0:		davfs2-PROGRAM_NAME.diff
BuildRequires:	neon-devel >= 0.27
BuildRequires:	gettext-devel >= 0.14.4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Davfs is a Linux file system driver that allows you to mount a WebDAV 
server as a disk drive. WebDAV is an extension to HTTP/1.1 that allows 
remote collaborative authoring of Web resources, defined in RFC 2518.

%prep

%setup -q
%patch0 -p1

%build
export PROGRAM_NAME="mount.davfs2"

%configure2_5x \
    --disable-rpath \

%make

%install
rm -fr %{buildroot}

install -d %{buildroot}/sbin
install -d %{buildroot}/var/run/mount.davfs2

%makeinstall_std

# rename the binaries
mv %{buildroot}%{_sbindir}/mount.davfs %{buildroot}%{_sbindir}/mount.davfs2
mv %{buildroot}%{_sbindir}/umount.davfs %{buildroot}%{_sbindir}/umount.davfs2

rm -f %{buildroot}/sbin/*
ln -snf ..%{_sbindir}/mount.davfs2 %{buildroot}/sbin/mount.davfs2
ln -snf ..%{_sbindir}/umount.davfs2 %{buildroot}/sbin/umount.davfs2

# rename the manpages
find %{buildroot}%{_mandir} -name "*.gz" | xargs gunzip
mv %{buildroot}%{_mandir}/man8/mount.davfs.8 %{buildroot}%{_mandir}/man8/mount.davfs2.8
mv %{buildroot}%{_mandir}/man8/umount.davfs.8 %{buildroot}%{_mandir}/man8/umount.davfs2.8
mv %{buildroot}%{_mandir}/de/man8/mount.davfs.8 %{buildroot}%{_mandir}/de/man8/mount.davfs2.8
mv %{buildroot}%{_mandir}/de/man8/umount.davfs.8 %{buildroot}%{_mandir}/de/man8/umount.davfs2.8

# (sb) handled by %%doc
rm -fr %{buildroot}%{_datadir}/%{name}

%find_lang %{name} --all-name

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING NEWS FAQ TODO THANKS ChangeLog
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/certs
%dir %{_sysconfdir}/%{name}/certs/private
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/secrets
%{_sbindir}/mount.davfs2
%{_sbindir}/umount.davfs2
/sbin/mount.davfs2
/sbin/umount.davfs2
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man5/*
%lang(de) %{_mandir}/de/man8/*
%lang(es) %{_mandir}/es/man5/*
%attr(1775,root,users) %dir /var/run/mount.%{name}
