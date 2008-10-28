# TODO
# - get rid (or update our rc-scripts) debianized run-parts
# - use global certs dir or sth
Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
Version:	20080809
Release:	0.1
# is it license name or should be unified? ("distributable"?)
License:	freedist
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.gz
# Source0-md5:	c155f5059006b94ad0aea7018161ab37
URL:		http://www.cacert.org/
# for temp files
Requires:	mktemp
# for c_rehash
Requires:	openssl-tools-perl
# for /bin/run-parts
Requires:	rc-scripts >= 0.4.1.25
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
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},/etc/ssl/certs,%{_sysconfdir}/ca-certificates/update.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

touch $RPM_BUILD_ROOT/etc/ssl/certs/ca-certificates.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-ca-certificates || :

%files
%defattr(644,root,root,755)
%dir /etc/ssl/certs
%config(noreplace) %verify(not md5 mtime size) /etc/ssl/certs/ca-certificates.crt
# remove noreplace?
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%dir %{_sysconfdir}/ca-certificates/update.d
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%{_datadir}/ca-certificates
