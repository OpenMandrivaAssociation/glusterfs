%define	major 0
%define libname	%mklibname glusterfs %{major}
%define develname %mklibname -d glusterfs

Summary:	GlusterFS network/cluster filesystem
Name:		glusterfs
Version:	3.2.6
Release:	1
License:	GPLv3+
Group:		Networking/Other
URL:		http://www.gluster.org/docs/index.php/GlusterFS
Source0:	ftp://ftp.gluster.com/pub/gluster/glusterfs/3.0/%{version}/%{name}-%{version}.tar.gz
Source1:	glusterfsd.init
Source2:	glusterfsd.sysconfig
Source3:	glusterfsd.logrotate
Source4:	glusterfs.logrotate
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fuse-devel >= 2.6.0
BuildRequires:	libibverbs-devel
BuildRequires:	libtool

%description
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

%package -n	%{libname}
Summary:	GlusterFS network/cluster filesystem library
Group:		System/Libraries
Provides: 	glusterfs-libs = %{EVRD}
Provides:	libglusterfs = %{EVRD}

%description -n	%{libname}
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

This package includes the libglusterfs and glusterfs translator modules common
to both GlusterFS server and client framework.

%package -n	%{develname}
Summary:	Static library and header files for the GlusterFS library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{version}

%description -n	%{develname}
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

This package contains the static GlusterFS library and its header files.

%package	common
Summary:	The common files needed by GlusterFS for client and server
Group:		Networking/Other
Requires:	fuse >= 2.6.0

%description	common
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

This package includes the glusterfs binaries and documentation. These are needed by both glusterfs
client and server.

%package	client
Summary:	GlusterFS client
Group:		Networking/Other
Requires:	%{name}-common = %{version}
Requires(post): rpm-helper

%description	client
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package is the client needed to mount a GlusterFS fs.

%package	server
Summary:	GlusterFS server
Group:		Networking/Other
Requires:	%{name}-common = %{version}
Requires:	%{name}-client = %{version}
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(post): sed

%description	server
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package is the server.

%prep
%setup -q %{name}-%{version}
cp %{SOURCE1} glusterfsd.init
cp %{SOURCE2} glusterfsd.sysconfig
cp %{SOURCE3} glusterfsd.logrotate
cp %{SOURCE4} glusterfs.logrotate

%build
%configure2_5x --disable-static --enable-shared
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
%{__rm} -rf %{buildroot} 
%{__make} install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}%{_includedir}/glusterfs
%{__mkdir_p} %{buildroot}/var/log/glusterfs
%{__install} -p -m 0644 libglusterfs/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir} -name '*.la' | xargs rm -f

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/run/glusterfsd

install -m0755 glusterfsd.init %{buildroot}%{_initrddir}/glusterd
install -m0644 glusterfsd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
install -m0644 glusterfsd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-server
install -m0644 glusterfs.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-client

touch %{buildroot}/var/log/glusterfs/glusterfs.log
touch %{buildroot}/var/log/glusterfs/glusterfsd.log

# remove default startup script
%{__rm} %{buildroot}/etc/init.d/glusterd

# fix docs
#rm -rf installed_docs
#mv %{buildroot}%{_docdir}/glusterfs installed_docs

%post client
%create_ghostfile /var/log/glusterfs/glusterfs.log root root 0644

%post server
%create_ghostfile /var/log/glusterfs/glusterfsd.log root root 0644
%_post_service glusterd
if [ -e /etc/glusterfs/glusterfs-server.vol ]; then 
echo "Updating /etc/sysconfig/glusterfsd to point to old /etc/glusterfs/glusterfs-server.vol file"
sed -i 's|GLUSTERFSD_CONFIG_FILE="/etc/glusterfs/glusterfsd.vol"|GLUSTERFSD_CONFIG_FILE="/etc/glusterfs/glusterfs-server.vol"|g' /etc/sysconfig/glusterfsd
#   mv -n /etc/glusterfs/glusterfs-server.vol /etc/glusterfs/glusterfsd.vol
fi

%preun server
%_preun_service glusterfsd

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/glusterfs

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/glusterfs
#%{_includedir}/libglusterfsclient.h
#%{_datadir}/glusterfs/*.py
#%{_libdir}/*.a
#%{_libdir}/*.la
%{_libdir}/*.so

%files common
%defattr(-,root,root)
# %doc AUTHORS ChangeLog COPYING INSTALL NEWS README
# %doc installed_docs/*
%docdir %{_docdir}/glusterfs
%doc %{_docdir}/glusterfs/*
%{_sysconfdir}/glusterfs/gluster*
#%{_bindir}/glusterfs-volgen
%{_mandir}/man8/glusterfs.8*
%{_mandir}/man8/gluster.8*
%{_mandir}/man8/glusterd.8*
%{_mandir}/man8/glusterfsd.8*
%dir /var/log/glusterfs/
%{_sbindir}/glusterfs
%{_sbindir}/gluster
%{_sbindir}/glusterfsd
%{_sbindir}/glusterd

%files client
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfs-client
/sbin/mount.glusterfs
%{_mandir}/man8/mount.glusterfs.8.*
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfs.log

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/glusterd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/glusterfsd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfs-server
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfsd.log
%dir /var/run/glusterfsd


%changelog
* Mon Apr 16 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.6-1
+ Revision: 791326
- manually remove .la files for backporting

* Mon Apr 16 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.2.6-1
+ Revision: 791281
- update to 3.2.6

* Mon Dec 06 2010 Funda Wang <fwang@mandriva.org> 3.0.0-2mdv2011.0
+ Revision: 611833
- update file list

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sat Jan 30 2010 Funda Wang <fwang@mandriva.org> 3.0.0-1mdv2010.1
+ Revision: 498597
- db storage not there any more
- New version 3.0.0

* Sun Sep 20 2009 Michael Scherer <misc@mandriva.org> 2.0.6-1mdv2010.0
+ Revision: 444885
- try to compile without -j, as this may help for weird errors

  + Funda Wang <fwang@mandriva.org>
    - use configure2_5x

  + Glen Ogilvie <nelg@mandriva.org>
    - This is a large upgrade, from 1.3.12 to 2.0.6. This includes updated configuration samples and init script.
      New features:
      * Distribute (DHT) translator
      * Replicate atomic write support
      * High Availability (HA) translator
      * Non-blocking I/O
      * Binary Protocol
      * NUFA translator
      * APIs via 'libglusterfsclient' library
      * Apache/Lighttpd embeddable 'mod_glusterfs'
      * Booster
      * Multiple OS support
        * OS X - Server and Client works.
        * Solaris 10 and above - Server part works file, Client part will be ported in future when FUSE is provided by Solaris.
        * FreeBSD 7.0 and above - Server and Client works.
      * Log message improvements
      * Stripe over tmpfs
      * Filter translator
      * Quota translator
      Full list of upgrade features at:
      http://www.gluster.com/community/documentation/index.php/Whats_New_v2.0

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.3.12-4mdv2010.0
+ Revision: 429217
- rebuild

* Tue Sep 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-3mdv2009.0
+ Revision: 285247
- fix deps
- rework the initscript and config

* Tue Sep 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-2mdv2009.0
+ Revision: 285163
- fix typo
- added fixes requested by Jos?\195?\169 Antonio Becerra Permuy

* Fri Sep 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-1mdv2009.0
+ Revision: 284140
- 1.3.12

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Apr 23 2007 Nicolas Vigier <nvigier@mandriva.com> 1.2.3-1mdv2008.0
+ Revision: 17508
- Import glusterfs




* Mon Apr 23 2007 Nicolas Vigier <nvigier@mandriva.com>
- first version
