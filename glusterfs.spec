%define name	glusterfs
%define version 1.2.3
%define release %mkrel 3

Release:	%{release}
Version:	%{version}
Summary:	GlusterFS network/cluster filesystem
Name:		%{name}
BuildRoot:	%{_tmppath}/%{name}-root
License:	GPL
Group:          Networking/Other
Source:		http://ftp.zresearch.com/pub/gluster/glusterfs/1.2/%{name}-%{version}.tar.gz
BuildRequires:	%{mklibname fuse -d} >= 2.6.0, flex, bison
URL:		http://www.gluster.org/glusterfs.php

%description
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

%package common
Summary:	The common files needed by GlusterFS for client and server
Group:          Networking/Other
Requires:	fuse >= 2.6.0


%description common
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

The glusterfs-common package contains files needed by both glusterfs
client and server.

%package client
Summary:	GlusterFS client
Group:          Networking/Other
Requires:	%{name}-common = %{version}

%description client
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

This package is the client needed to mount a GlusterFS fs.

%package server
Summary:	GlusterFS server
Group:          Networking/Other
Requires:	%{name}-common = %{version}

%description server
GlusterFS is a powerful network/cluster filesystem. The storage server
(or each in a cluster) runs glusterfsd and the clients use mount
command or glusterfs client to mount the exported filesystem. You can
keep scaling your storage beyond peta bytes as your demand increases.

Please visit http://www.gluster.org/glusterfs.php for more info.

This package is the server.

%prep
%setup -q

%build
CFLAGS='-O3' %configure
make

%install
%{__rm} -Rf %{buildroot}
%makeinstall slashsbindir=${RPM_BUILD_ROOT}/sbin

%clean
%{__rm} -Rf %{buildroot}

%files common
%defattr(-,root,root)
%{_sysconfdir}
%{_libdir}/glusterfs
%{_libdir}/libglusterfs.so
%doc README AUTHORS NEWS COPYING

%files client
%defattr(-,root,root)
/sbin/mount.glusterfs
%{_sbindir}/glusterfs

%files server
%defattr(-,root,root)
%{_sbindir}/glusterfsd
%{_var}
