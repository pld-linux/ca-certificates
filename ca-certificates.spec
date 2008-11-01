# TODO
# - keep one: certificates.spec vs ca-certificates.spec
Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
Version:	20080809
Release:	0.2
# is it license name or should be unified? ("distributable"?)
License:	freedist
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.gz
# Source0-md5:	c155f5059006b94ad0aea7018161ab37
Patch0:		%{name}-undebianize.patch
URL:		http://www.cacert.org/
# for temp files
Requires:	mktemp
# for c_rehash
Requires:	openssl-tools-perl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common CA Certificates PEM files.

%description -l pl.UTF-8
Pliki PEM popularnych certyfikatów CA.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},/etc/certs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

touch $RPM_BUILD_ROOT/etc/certs/ca-certificates.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-ca-certificates || :

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/certs/ca-certificates.crt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%{_datadir}/ca-certificates
