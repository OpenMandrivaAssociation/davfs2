%define dav_user %{name}
%define dav_group %{name}
%define dav_localstatedir /var/run
%define dav_syscachedir /var/cache

Summary:	File system driver that allows you to mount a WebDAV server
Name:		davfs2
Version: 	1.4.7
Release: 	%mkrel 1
License:	GPLv2+
Group:		System/Kernel and hardware		
URL:		http://savannah.nongnu.org/projects/davfs2
Source0:	http://ftp.twaren.net/Unix/NonGNU/%{name}/%{name}-%{version}.tar.gz
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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-2mdv2011.0
+ Revision: 663752
- mass rebuild

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 1.4.6-1mdv2011.0
+ Revision: 568047
- new version 1.4.6

* Fri Dec 11 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.4.5-1mdv2010.1
+ Revision: 476391
- New version 1.4.5.

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.3-1mdv2010.1
+ Revision: 462730
- Update to new version 1.4.3

* Tue Jun 16 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-1mdv2010.0
+ Revision: 386466
- Update to new version 1.4.1
- Obsolete old davfs package
- Don't rename mount.davfs to mount.davfs2 anymore, but provide
  symlinks for users for users upgrading from previous davfs2 packages
- Remove glibc 2.7 patch: not needed anymore
- Update string format patch

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.3-2mdv2009.1
+ Revision: 316532
- more correct fix in P1
- fix build with -Werror=format-security (P2)

* Wed Aug 06 2008 Funda Wang <fwang@mandriva.org> 1.3.3-1mdv2009.0
+ Revision: 264760
- New version 1.3.3

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.3.2-5mdv2009.0
+ Revision: 264385
- rebuild early 2009.0 package (before pixel changes)

* Thu May 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-4mdv2009.0
+ Revision: 210057
- fix correct permissions (0600) in the glibc27 patch (thanks meuh)

* Thu May 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-3mdv2009.0
+ Revision: 210055
- fix correct permissions in the glibc27 patch (thanks meuh)
- fix the glibc27 patch (thanks meuh)

* Thu May 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-1mdv2009.0
+ Revision: 210035
- reworked the package some more
- added a glibc27 patch
- 1.3.2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill extra spacing at top of description


* Wed Apr 12 2006 Stew Benedict <sbenedict@mandriva.com> 0.2.8-2mdk
- buildrequires neon-devel = 0.24.7

* Thu Mar 23 2006 Lenny Cartier <lenny@mandriva.com> 0.2.8-1mdk
- 0.2.8

* Wed Feb 15 2006 Stew Benedict <sbenedict@mandriva.com> 0.2.7-1mdk
- 0.2.7, redo P0

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.2.5-4mdk
- rebuilt against openssl-0.9.8a

* Wed Sep 28 2005 Stew Benedict <sbenedict@mandriva.com> 0.2.5-3mdk
- drop modprobe.conf mod (#18906)

* Wed Sep 28 2005 Stew Benedict <sbenedict@mandriva.com> 0.2.5-2mdk
- check for DAV_VFS_TYPE = davfs2, rather than davfs (#18906)
- fix perms on pid file directory

* Mon Sep 26 2005 Stew Benedict <sbenedict@mandriva.com> 0.2.5-1mdk
- New release 0.2.5, redo P0

* Thu Jun 09 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.2.3-3mdk
- Rebuild for libkrb53-devel 1.4.1

* Tue May 10 2005 Stew Benedict <sbenedict@mandriva.com>  0.2.3-2mdk
- renumber patches, fix compile on x86_64 (P1)

* Wed Nov 03 2004 Stew Benedict <sbenedict@mandrakesoft.com>  0.2.3-1mdk
- 0.2.3, patch0 merged upstream

* Tue Oct 26 2004 Stew Benedict <sbenedict@mandrakesoft.com>  0.2.2-2mdk
- link mount.davfs2 in /sbin so mount finds it

* Wed Oct 20 2004 Stew Benedict <sbenedict@mandrakesoft.com>  0.2.2-1mdk
- First mandrakelinux release
- rename binary to mount.davfs2 to coexist with davfs

