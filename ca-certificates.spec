# TODO
# - cleanup dead links from /etc/openssl/certs after -update uninstall
#
# - https://bugzilla.mozilla.org/show_bug.cgi?id=549701 and
#   http://groups.google.com/group/mozilla.dev.security.policy/browse_thread/thread/b6493a285ba79998#
#
Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
Version:	20090814
Release:	13
License:	distributable
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}+nmu3.tar.gz
# Source0-md5:	578be1c5a459cea3b243777c08610727
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
Source14:	http://crt.tcs.terena.org/TERENASSLCA.crt
# Source14-md5:	f62cd1546a8ef14e31ba1ce8eecd234a
Source15:	http://crt.tcs.terena.org/TERENAeScienceSSLCA.crt
# Source15-md5:	5feea35ab01a373f115219706f1f57bd
Source16:	http://crt.tcs.terena.org/TERENAPersonalCA.crt
# Source16-md5:	53eaa497c8fb0b79f14fe9f69693689a
Source17:	http://crt.tcs.terena.org/TERENAeSciencePersonalCA.crt
# Source17-md5:	e25cc655d3ebe920ca9c187e3dde9191
Source18:	http://crt.tcs.terena.org/TERENACodeSigningCA.crt
# Source18-md5:	74c9f511ab03a4e6b7462e310abfa89b
Source19:	http://www.sk.ee/upload/files/JUUR-SK.PEM.cer
# Source19-md5:	805784c06c9eff3771a4b9bd631cd3f5
Source20:	http://www.sk.ee/upload/files/ESTEID-SK.PEM.cer
# Source20-md5:	387beee5b8539ab7d91628f486295899
Source21:	http://www.sk.ee/upload/files/ESTEID-SK%202007.PEM.cer
# Source21-md5:	2b1a2a77f565d68fdf5f19f6cc3a5600
Source22:	http://www.sk.ee/upload/files/ESTEID-SK%202011.pem.cer
# Source22-md5:	cfcc1e592cb0ff305158a7e32730546c
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-more-certs.patch
Patch2:		%{name}-etc-certs.patch
Patch3:		%{name}-c_rehash.sh.patch
Patch4:		%{name}-endline.patch
Patch5:		%{name}-mozilla.patch
Patch6:		%{name}-DESTDIR.patch
URL:		http://www.cacert.org/
BuildRequires:	openssl-tools
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Obsoletes:	certificates
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certsdir	/etc/certs
%if "%{pld_release}" == "th"
%define		openssldir	/etc/openssl/certs
%else
%define		openssldir	/var/lib/openssl/certs
%endif

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
%if "%{pld_release}" == "ac"
Requires:	openssl-tools >= 0.9.7m-2
%else
Requires:	openssl-tools >= 0.9.8i-3
%endif

%description update
Script and data for updating CA Certificates database.

%description update -l pl.UTF-8
Skrypt i dane do odświeżania bazy certyfikatów CA.

%prep
%setup -q -n %{name}-%{version}+nmu3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -i -e 's,@openssldir@,%{openssldir},' sbin/update-ca-certificates*

%{__unzip} -qq %{SOURCE1} -d thawte

find thawte/ -name *.pem -o -name *.txt| while read f ; do
	if (file "$f" | grep -q "PEM"); then
		ff=$(echo $f | sed -e 's|[ ,]|_|g' -e 's|[()]|=|g')
		nname=$(basename "$ff" .pem)
		nname=$(basename "$nname" .txt)
		nname=$(basename "$nname" _b64)
		cp -i "$f" "thawte/${nname}.crt"
	else
		echo "Skipping $f, doesn't look like PEM CERT"
	fi
done

install -d certum
cp -ai %{SOURCE2} certum
cp -ai %{SOURCE3} certum
cp -ai %{SOURCE4} certum
cp -ai %{SOURCE5} certum
cp -ai %{SOURCE6} certum
cp -ai %{SOURCE7} certum
cp -ai %{SOURCE8} certum
cp -ai %{SOURCE9} certum
cp -ai %{SOURCE10} certum
cp -ai %{SOURCE11} certum
cp -ai %{SOURCE12} certum
cp -ai %{SOURCE13} certum
for a in certum/*.pem; do
	mv -i "$a" "${a%.pem}.crt"
done

install -d terena
openssl x509 -inform DER -in %{SOURCE14} -outform PEM -out terena/$(basename %{SOURCE14})
openssl x509 -inform DER -in %{SOURCE15} -outform PEM -out terena/$(basename %{SOURCE15})
openssl x509 -inform DER -in %{SOURCE16} -outform PEM -out terena/$(basename %{SOURCE16})
openssl x509 -inform DER -in %{SOURCE17} -outform PEM -out terena/$(basename %{SOURCE17})
openssl x509 -inform DER -in %{SOURCE18} -outform PEM -out terena/$(basename %{SOURCE18})

# http://www.sk.ee/pages.php/0203040502#Root_certificates
# JUUR-SK, ESTEID-SK and ESTEID-SK 2007
install -d esteid
cp -ai %{SOURCE19} esteid
cp -ai %{SOURCE20} esteid
cp -ai %{SOURCE21} esteid/ESTEID-SK_2007.crt
cp -ai %{SOURCE22} esteid/ESTEID-SK_2011.crt
for a in esteid/*.PEM.cer; do
	mv -i "$a" "${a%.PEM.cer}.crt"
done

%build
%{__make}

# We have those and more in specific dirs
rm mozilla/{Thawte,thawte,Certum,IGC_A,Deutsche_Telekom_Root_CA_2}*.crt

# See TODO
# rm mozilla/RSA_Security_1024_v3.crt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},%{certsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_datadir}/ca-certificates -name '*.crt' -exec sed -i -e 's/\r$//' {} \;

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

# build %{certsdir}/ca-certificates.crt
install -d $RPM_BUILD_ROOT%{openssldir}
./sbin/update-ca-certificates --destdir $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{openssldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post update
%{_sbindir}/update-ca-certificates --fresh || :

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{certsdir}/ca-certificates.crt

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%{_datadir}/ca-certificates
