Summary:	Common CA Certificates PEM files
Name:		ca-certificates
Version:	20070303
Release:	0.12
Group:		Libraries
URL:		http://www.cacert.org/
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.gz
# Source0-md5:	e356066a02d257d23f8e0f4d48d08b1b
License:	freedist
Requires:	mktemp
Requires:	openssl-tools-perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common CA Certificates PEM files

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},%{_sysconfdir}/ssl/certs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/ca-certificates.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-ca-certificates || :

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/ssl/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ssl/certs/ca-certificates.crt
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%{_datadir}/ca-certificates
