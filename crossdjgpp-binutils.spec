Summary:	Cross DJGPP GNU binary utility development utilities - binutils
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - DJGPP binutils
Summary(fr):	Utilitaires de développement binaire de GNU - DJGPP binutils
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla DJGPP - binutils
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - DJGPP binutils
Summary(tr):	GNU geliþtirme araçlarý - DJGPP binutils
Name:		crossdjgpp-binutils
Version:	2.15.90.0.3
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	1c1af0064ebd3d7bd99905874656a21e
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
%ifarch sparc sparc32
BuildRequires:	sparc32
%endif
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

Ten pakiet zawiera binutils generuj±ce skro¶nie binaria dla DOS.

%prep
%setup -q -n binutils-%{version}

%build
cp /usr/share/automake/config.sub .

# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
# [the same applies to binutils 2.10.1.0.4]

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
%ifarch sparc
sparc32 \
%endif
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib/*
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*

%clean
rm -rf $RPM_BUILD_ROOT
