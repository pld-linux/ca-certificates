# TODO
# - cleanup dead links from /etc/openssl/certs after -update uninstall
Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
Version:	20081127
Release:	1
License:	distributable
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.gz
# Source0-md5:	4a4b07e755e1506cab753eec9a2e7157
Source1:	https://www.verisign.com/support/thawte-roots.zip
# Source1-md5:	a3709cc0279ef3fca4f86ea775066b18
Source2:	http://www.certum.pl/keys/CA.pem
# Source2-md5:	35610177afc9c64e70f1ce62c1885496
Source3:	http://www.certum.pl/keys/level1.pem
# Source3-md5:	ba2d2e234ef9cfd2e6e5f810c964862e
Source4:	http://www.certum.pl/keys/level2.pem
# Source4-md5:	d06578a04e8cb23071f3870430ea0cf0
Source5:	http://www.certum.pl/keys/level3.pem
# Source5-md5:	47b67c63a52236576fc0d1150327c962
Source6:	http://www.certum.pl/keys/level4.pem
# Source6-md5:	f1f8a65d177745311a1e99f029ae5d71
Source7:	http://www.certum.pl/keys/vs.pem
# Source7-md5:	8da19ffc48c5dcc2868b1aa55f1d5983
Source8:	http://www.certum.pl/keys/na.pem
# Source8-md5:	ba571cb35e7672ff7ae95132ac1bfec4
Source9:	http://www.certum.pl/keys/tsa.pem
# Source9-md5:	1a7b3faf8ed00f4d80297de74862e102
Source10:	http://www.certum.pl/keys/class1.pem
# Source10-md5:	058436b132ea2df6972821f546104a16
Source11:	http://www.certum.pl/keys/class2.pem
# Source11-md5:	5caf7fe99b1fc6e63c40b3d081711d1b
Source12:	http://www.certum.pl/keys/class3.pem
# Source12-md5:	07bc97e21da092ba53535c7379e1b58b
Source13:	http://www.certum.pl/keys/class4.pem
# Source13-md5:	99ef61d509539af89f1c025b67245965
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-more-certs.patch
Patch2:		%{name}-etc-certs.patch
Patch3:		%{name}-c_rehash.sh.patch
URL:		http://www.cacert.org/
BuildRequires:	ruby
BuildRequires:	unzip
Obsoletes:	certificates
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certsdir	/etc/certs

%description
Common CA Certificates PEM files.

%description -l pl.UTF-8
Pliki PEM popularnych certyfikatów CA.

%package update
Summary:	Script for updating CA Certificates database
Summary(pl.UTF-8):	Skrypt do odświeżania bazy certyfikatów CA
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mktemp
Requires:	openssl-tools >= 0.9.8i-3

%description update
Script and data for updating CA Certificates database.

%description update -l pl.UTF-8
Skrypt i dane do odświeżania bazy certyfikatów CA.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__unzip} -qq %{SOURCE1} '*_b64.txt' -d thawte
for a in thawte/{,*/}*.txt; do
	mv "$a" "${a%_b64.txt}.crt"
done

install -d certum
install %{SOURCE2} certum
install %{SOURCE3} certum
install %{SOURCE4} certum
install %{SOURCE5} certum
install %{SOURCE6} certum
install %{SOURCE7} certum
install %{SOURCE8} certum
install %{SOURCE9} certum
install %{SOURCE10} certum
install %{SOURCE11} certum
install %{SOURCE12} certum
install %{SOURCE13} certum
for a in certum/*.pem; do
	mv "$a" "${a%.pem}.crt"
done

%build
%{__make}

# We have those and more in specific dirs
rm mozilla/{Thawte,thawte,Certum}*.crt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},%{certsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' -print0 | xargs -0 cat
) > $RPM_BUILD_ROOT%{certsdir}/ca-certificates.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post update
%{_sbindir}/update-ca-certificates || :

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{certsdir}/ca-certificates.crt

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%{_datadir}/ca-certificates
