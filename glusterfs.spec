%define major 0
%define libname %mklibname glusterfs %{major}
%define devname %mklibname -d glusterfs
%define _disable_ld_no_undefined 1

Summary:	GlusterFS network/cluster filesystem
Name:		glusterfs
Version:	3.7.8
Release:	2
License:	GPLv3+
Group:		Networking/Other
URL:		https://www.gluster.org/docs/index.php/GlusterFS
Source0:	http://download.gluster.org/pub/gluster/glusterfs/%(echo %{version} |cut -d. -f1-2)/%{version}/%{name}-%{version}.tar.gz
Source1:	glusterfsd.service
Source2:	glusterfsd.sysconfig
Source3:	glusterfsd.logrotate
Source4:	glusterfs.logrotate
Source5:	glusterd.sysconfig

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(liburcu-bp)
BuildRequires:	libibverbs-devel
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	acl-devel
BuildRequires:	python2

%description
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

#----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	GlusterFS network/cluster filesystem library
Group:		System/Libraries
Provides:	glusterfs-libs = %{EVRD}
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

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/glusterfs

#----------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Static library and header files for the GlusterFS library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

Please visit http://www.gluster.org/docs/index.php/GlusterFS for more info.

This package contains the static GlusterFS library and its header files.

%files -n %{devname}
%{_includedir}/glusterfs/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

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

This package includes the glusterfs binaries and documentation.
These are needed by both glusterfs client and server.

%files common
%docdir %{_docdir}/glusterfs
%doc %{_docdir}/glusterfs/*
%{_sysconfdir}/glusterfs/gluster*
%{_mandir}/man8/glusterfs.8*
%{_mandir}/man8/gluster.8*
%{_mandir}/man8/glusterd.8*
%{_mandir}/man8/glusterfsd.8*
%dir /var/log/glusterfs/
%{_sbindir}/glusterfs
%{_sbindir}/gluster
%{_sbindir}/glusterfsd
%{_sbindir}/glusterd

# Ganesha stuff... Is this needed for both client and server?
%dir %{_sysconfdir}/ganesha
%{_sysconfdir}/ganesha/ganesha-ha.conf.sample
%{_libexecdir}/ganesha
%dir %{_prefix}/lib/ocf
%dir %{_prefix}/lib/ocf/resource.d
%dir %{_prefix}/lib/ocf/resource.d/heartbeat
%{_prefix}/lib/ocf/resource.d/heartbeat/ganesha_grace
%{_prefix}/lib/ocf/resource.d/heartbeat/ganesha_mon
%{_prefix}/lib/ocf/resource.d/heartbeat/ganesha_nfsd


%dir %{_sysconfdir}/glusterfs
%{_sysconfdir}/glusterfs/group-virt.example
%{_sysconfdir}/glusterfs/logger.conf.example
%{_bindir}/glusterfind
%dir %{_libexecdir}/glusterfs
%{_libexecdir}/glusterfs/gverify.sh
%{_libexecdir}/glusterfs/peer_add_secret_pub
%{_libexecdir}/glusterfs/peer_gsec_create
%{_libexecdir}/glusterfs/peer_mountbroker
%{_libexecdir}/glusterfs/gfind_missing_files
%{_libexecdir}/glusterfs/glusterfind

%{_sbindir}/gcron.py
%{_sbindir}/gfind_missing_files
%{_sbindir}/glfsheal
%{_sbindir}/snap_scheduler.py
%dir %{_datadir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
%{_datadir}/glusterfs/scripts/*

#----------------------------------------------------------------------------

%package	client
Summary:	GlusterFS client
Group:		Networking/Other
Requires:	%{name}-common = %{EVRD}
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

%files client
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfs-client
/sbin/mount.glusterfs
%{_mandir}/man8/mount.glusterfs.8.*
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfs.log
%{_bindir}/fusermount-glusterfs

%post client
%create_ghostfile /var/log/glusterfs/glusterfs.log root root 0644

#----------------------------------------------------------------------------

%package	server
Summary:	GlusterFS server
Group:		Networking/Other
Requires:	%{name}-common = %{EVRD}
Requires:	%{name}-client = %{EVRD}
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

%files server
%attr(0755,root,root) %{_initrddir}/glusterd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/glusterfsd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfs-server
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfsd.log
%dir /var/run/glusterfsd
%{_prefix}/lib/ocf/resource.d/glusterfs
%dir %{_localstatedir}/lib/glusterd
%dir %{_localstatedir}/lib/glusterd/groups
%{_localstatedir}/lib/glusterd/groups/virt
%dir %{_localstatedir}/lib/glusterd/hooks
%{_localstatedir}/lib/glusterd/hooks/1

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

#----------------------------------------------------------------------------
%package geo-replication
Summary:	GlusterFS Geo-replication
Group:		Networking/Other
Requires:	%{name}-common = %{version}
Requires:	%{name}-client = %{version}

%description geo-replication
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides support to geo-replication.

%files geo-replication
%{_libexecdir}/glusterfs/gsyncd
%{_libexecdir}/glusterfs/python/syncdaemon/*
%{_libexecdir}/glusterfs/set_geo_rep_pem_keys.sh

%prep
%setup -q
cp %{SOURCE1} glusterfsd.service
cp %{SOURCE2} glusterfsd.sysconfig
cp %{SOURCE3} glusterfsd.logrotate
cp %{SOURCE4} glusterfs.logrotate
cp %{SOURCE4} glusterd.sysconfig

%build
export PYTHON=python2
%configure \
	--disable-static \
	--enable-shared LIBS=-ltirpc CC=gcc CFLAGS="%{optflags} -fno-lto -fuse-ld=bfd" LDFLAGS="%{optflags} -fno-lto -fuse-ld=bfd"

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make 

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_includedir}/glusterfs
mkdir -p %{buildroot}/var/log/glusterfs
install -p -m 0644 libglusterfs/src/*.h %{buildroot}%{_includedir}/glusterfs/

install -d %{buildroot}%{_unitdir}/
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/run/glusterfsd

install -m0755 glusterfsd.service %{buildroot}%{_initrddir}/glusterd
install -m0644 glusterfsd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
install -m0644 glusterfsd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-server
install -m0644 glusterfs.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-client

touch %{buildroot}/var/log/glusterfs/glusterfs.log
touch %{buildroot}/var/log/glusterfs/glusterfsd.log

# remove default startup script
rm %{buildroot}/etc/init.d/glusterd
