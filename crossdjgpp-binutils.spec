Summary:	DJGPP GNU Binary Utility Development Utilities - binutils
Summary(pl):	Narzêdzia programistyczne GNU DJGPP - binutils
Name:		crossdjgpp-binutils
Version:	2.11.90.0.19
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	/bin/bash
Requires:	crossdjgpp-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		i386-pc-msdosdjgpp
%define		arch		%{_prefix}/%{target}

%description
DJGPP is a port of GNU GCC to the DOS environment. (It stands for DJ's
Gnu Programming Platform, if it has to stand for something, but it's
best left ambiguous.)

This package contains cross targeted binutils.

%description -l pl
DJGPP to port GNU GCC dla ¶rodowiska DOS (skrót oznacza DJ's Gnu
Programming Platform, je¶li ju¿ koniecznie ma co¶ oznaczaæ).

Ten pakiet zawiera binutils skompilowane do kroskompilacji.

%prep
%setup -q -n binutils-%{version}

%build
rm -rf $RPM_BUILD_ROOT

# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
# [the same applies to binutils 2.10.1.0.4]

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} tooldir=%{_prefix} EXEEXT="" all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib/*
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*

%clean
rm -rf $RPM_BUILD_ROOT
