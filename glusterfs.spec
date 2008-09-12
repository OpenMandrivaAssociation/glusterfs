%define	major 0
%define libname	%mklibname glusterfs %{major}
%define develname %mklibname -d glusterfs

Summary:	GlusterFS network/cluster filesystem
Name:		glusterfs
Version:	1.3.12
Release:	%mkrel 1
License:	GPL
Group:		Networking/Other
URL:		http://www.gluster.org/glusterfs.php
Source0:	http://ftp.zresearch.com/pub/gluster/glusterfs/1.3/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fuse-devel >= 2.6.0
BuildRequires:	libibverbs-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

%package -n	%{libname}
Summary:	GlusterFS network/cluster filesystem library
Group:          System/Libraries

%description -n	%{libname}
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

This package contains the shared GlusterFS library.

%package -n	%{develname}
Summary:	Static library and header files for the GlusterFS library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{develname}
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

This package contains the static GlusterFS library and its header files.

%package	common
Summary:	The common files needed by GlusterFS for client and server
Group:		Networking/Other
Requires:	fuse >= 2.6.0

%description	common
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

The glusterfs-common package contains files needed by both glusterfs
client and server.

%package	client
Summary:	GlusterFS client
Group:		Networking/Other
Requires:	%{name}-common = %{version}

%description	client
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

This package is the client needed to mount a GlusterFS fs.

%package	server
Summary:	GlusterFS server
Group:		Networking/Other
Requires:	%{name}-common = %{version}

%description	server
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

This package is the server.

%prep

%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall slashsbindir=%{buildroot}/sbin

# fix docs
rm -rf installed_docs
mv %{buildroot}%{_docdir}/glusterfs installed_docs

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README AUTHORS NEWS
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.*a

%files common
%defattr(-,root,root)
%doc installed_docs/*
%{_sysconfdir}/glusterfs/glusterfs-client.vol.sample
%{_sysconfdir}/glusterfs/glusterfs-server.vol.sample
%{_libdir}/glusterfs
%{_mandir}/man8/glusterfs.8*

%files client
%defattr(-,root,root)
/sbin/mount.glusterfs
%{_sbindir}/glusterfs

%files server
%defattr(-,root,root)
%{_sbindir}/glusterfsd
%dir /var/log/glusterfs
