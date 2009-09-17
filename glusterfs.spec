%define	major 0
%define libname	%mklibname glusterfs %{major}
%define develname %mklibname -d glusterfs

Summary:	GlusterFS network/cluster filesystem
Name:		glusterfs
Version:	2.0.6
Release:	%mkrel 1
License:	GPLv3+
Group:		Networking/Other
URL: 		http://www.gluster.org/docs/index.php/GlusterFS
Source0:	ftp://ftp.gluster.com/pub/gluster/glusterfs/2.0/%{version}/%{name}-%{version}.tar.gz
Source1:	glusterfsd.init
Source2:	glusterfsd.sysconfig
Source3:	glusterfsd.logrotate
Source4:	glusterfs.logrotate
Patch0:	glusterfs-sprint.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	db4-devel
BuildRequires:	gcc
BuildRequires:	make
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
Provides: 	glusterfs-libs, libglusterfs

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
Provides:	%{name}-devel = %{version}
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
Requires:	libglusterfs

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
%patch0 -p1
cp %{SOURCE1} glusterfsd.init
cp %{SOURCE2} glusterfsd.sysconfig
cp %{SOURCE3} glusterfsd.logrotate
cp %{SOURCE4} glusterfs.logrotate

%build
%configure
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot} 
%{__make} install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}%{_includedir}/glusterfs
%{__mkdir_p} %{buildroot}/var/log/glusterfs
%{__install} -p -m 0644 libglusterfs/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir}/glusterfs -name '*.la' | xargs rm -f

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/run/glusterfsd

install -m0755 glusterfsd.init %{buildroot}%{_initrddir}/glusterfsd
install -m0644 glusterfsd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
install -m0644 glusterfsd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfsd
install -m0644 glusterfs.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs

touch %{buildroot}/var/log/glusterfs/glusterfs.log
touch %{buildroot}/var/log/glusterfs/glusterfsd.log

# remove default startup script
%{__rm} %{buildroot}/etc/init.d/glusterfsd

# fix docs
#rm -rf installed_docs
#mv %{buildroot}%{_docdir}/glusterfs installed_docs

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post client
%create_ghostfile /var/log/glusterfs/glusterfs.log root root 0644

%post server
%create_ghostfile /var/log/glusterfs/glusterfsd.log root root 0644
%_post_service glusterfsd
if [ -e /etc/glusterfs/glusterfs-server.vol ]; then 
echo "Updating /etc/sysconfig/glusterfsd to point to old /etc/glusterfs/glusterfs-server.vol file"
sed -i 's|GLUSTERFSD_CONFIG_FILE="/etc/glusterfs/glusterfsd.vol"|GLUSTERFSD_CONFIG_FILE="/etc/glusterfs/glusterfs-server.vol"|g' /etc/sysconfig/glusterfsd
#   mv -n /etc/glusterfs/glusterfs-server.vol /etc/glusterfs/glusterfsd.vol
fi

%preun server
%_preun_service glusterfsd

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
# %doc README AUTHORS NEWS
%{_libdir}/*.so.%{major}*
%{_libdir}/glusterfs

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/glusterfs
%{_includedir}/libglusterfsclient.h
%exclude %{_includedir}/glusterfs/y.tab.h
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so

%files common
%defattr(-,root,root)
# %doc AUTHORS ChangeLog COPYING INSTALL NEWS README
# %doc installed_docs/*
%docdir %{_docdir}/glusterfs
%doc %{_docdir}/glusterfs/*
%{_sysconfdir}/glusterfs/glusterfs*
%{_mandir}/man8/glusterfs.8*
%dir /var/log/glusterfs
%{_sbindir}/glusterfs
%{_sbindir}/glusterfsd

%files client
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfs
/sbin/mount.glusterfs
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfs.log

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/glusterfsd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/glusterfsd
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/glusterfsd
%attr(0644,root,root) %ghost %config(noreplace) /var/log/glusterfs/glusterfsd.log
%dir /var/run/glusterfsd
