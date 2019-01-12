# TODO
# - cleanup dead links from /etc/openssl/certs after -update uninstall
# - https://bugzilla.mozilla.org/show_bug.cgi?id=549701 and
#   http://groups.google.com/group/mozilla.dev.security.policy/browse_thread/thread/b6493a285ba79998#
# - make amsn use system certs
# - make pidgin use system certs
# - swap %{certsdir}/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt regards file vs symlink
#
# Conditional build:
%bcond_without	tests	# skip duplicates check

Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
%define	ver_date	20180409
Version:	%{ver_date}
Release:	3
License:	GPL v2 (scripts), MPL v2 (mozilla certs), distributable (other certs)
Group:		Base
Source0:	http://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.xz
# Source0-md5:	8425f4b1219e4e528db2de764e4c6586
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
Source14:	http://www.certum.pl/CTNCA.pem
# Source14-md5:	231b5b8bf05c5e93a9b2ebc4186eb6f7
Source15:	http://repository.certum.pl/class1casha2.pem
# Source15-md5:	b52dde6e2618a21965afbe6d6676d09f
Source16:	http://repository.certum.pl/dvcasha2.pem
# Source16-md5:	88ce64a84375c95ab6f7c8515dd2a117
Source17:	http://repository.certum.pl/ovcasha2.pem
# Source17-md5:	3149c923bd23469d6b14caa6334f8b63
Source18:	http://repository.certum.pl/evcasha2.pem
# Source18-md5:	ac54dc6cf3af7e243879b1c8b4aca8a3
#Source19:	http://repository.certum.pl/dvcasha2.pem
## Source19-md5:	88ce64a84375c95ab6f7c8515dd2a117
Source20:	http://repository.certum.pl/gscasha2.pem
# Source20-md5:	a29d37f95dafc08cef36015922e3b0d3
Source21:	http://crt.tcs.terena.org/TERENASSLCA.crt
# Source21-md5:	f62cd1546a8ef14e31ba1ce8eecd234a
Source22:	http://crt.tcs.terena.org/TERENAeScienceSSLCA.crt
# Source22-md5:	5feea35ab01a373f115219706f1f57bd
Source23:	http://crt.tcs.terena.org/TERENAPersonalCA.crt
# Source23-md5:	53eaa497c8fb0b79f14fe9f69693689a
Source24:	http://crt.tcs.terena.org/TERENAeSciencePersonalCA.crt
# Source24-md5:	e25cc655d3ebe920ca9c187e3dde9191
Source25:	http://crt.tcs.terena.org/TERENACodeSigningCA.crt
# Source25-md5:	74c9f511ab03a4e6b7462e310abfa89b
Source26:	http://www.sk.ee/upload/files/JUUR-SK.PEM.cer
# Source26-md5:	805784c06c9eff3771a4b9bd631cd3f5
Source27:	http://www.sk.ee/upload/files/ESTEID-SK.PEM.cer
# Source27-md5:	387beee5b8539ab7d91628f486295899
Source28:	http://www.sk.ee/upload/files/ESTEID-SK%202007.PEM.cer?/ESTEID-SK_2007.PEM.cer
# Source28-md5:	2b1a2a77f565d68fdf5f19f6cc3a5600
Source29:	http://www.sk.ee/upload/files/ESTEID-SK%202011.pem.cer?/ESTEID-SK_2011.pem.cer
# Source29-md5:	cfcc1e592cb0ff305158a7e32730546c
Source30:	http://www.terena.org/activities/tcs/repository/sha2/TERENA_SSL_CA_2.pem
# Source30-md5:	96700974350cecfcfbd904d52c3a3942
Source31:	http://www.terena.org/activities/tcs/repository/sha2/TERENA_Personal_CA_2.pem
# Source31-md5:	d40e5c821f8559faf5bcd55eac5e1371
Source32:	http://www.terena.org/activities/tcs/repository/sha2/TERENA_Code_Signing_CA_2.pem
# Source32-md5:	69ff653e730adf87ff59bf373950b357
Source33:	http://www.terena.org/activities/tcs/repository-g3/TERENA_SSL_CA_3.pem
# Source33-md5:	b22ed904900ed6b3bc129f9a35ba5a66
Source34:	http://www.terena.org/activities/tcs/repository-g3/TERENA_Personal_CA_3.pem
# Source34-md5:	eb5ddefe94750c2f8d4f11cb1f3af911
Source35:	http://www.terena.org/activities/tcs/repository-g3/TERENA_Code_Signing_CA_3.pem
# Source35-md5:	43375a208fba0a5e73f1912faa4db86d
Source36:	http://www.terena.org/activities/tcs/repository-g3/TERENA_SSL_High_Assurance_CA_3.pem
# Source36-md5:	6e00d9ede4460e739eb285ea023299f0
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-more-certs.patch
Patch2:		%{name}-etc-certs.patch

Patch5:		%{name}-DESTDIR.patch
Patch6:		%{name}.d.patch
Patch7:		no-openssl-rehash.patch
URL:		https://packages.debian.org/sid/ca-certificates
BuildRequires:	openssl-tools
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	unzip
BuildRequires:	xz
Obsoletes:	certificates
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certsdir	/etc/certs
%define		openssldir	/etc/openssl/certs

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
Requires:	openssl-tools >= 0.9.7m-6.3
%else
Requires:	openssl-tools >= 0.9.8i-3
%endif

%description update
Script and data for updating CA Certificates database.

%description update -l pl.UTF-8
Skrypt i dane do odświeżania bazy certyfikatów CA.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%patch5 -p1
%patch6 -p1
%patch7 -p1

%{__sed} -i -e 's,@openssldir@,%{openssldir},' sbin/update-ca-certificates*

install -d certum
cp -pi %{SOURCE2} certum
cp -pi %{SOURCE3} certum
cp -pi %{SOURCE4} certum
cp -pi %{SOURCE5} certum
cp -pi %{SOURCE6} certum
cp -pi %{SOURCE7} certum
cp -pi %{SOURCE8} certum
cp -pi %{SOURCE9} certum
cp -pi %{SOURCE10} certum
cp -pi %{SOURCE11} certum
cp -pi %{SOURCE12} certum
cp -pi %{SOURCE13} certum
cp -pi %{SOURCE14} certum
cp -pi %{SOURCE15} certum
cp -pi %{SOURCE16} certum
cp -pi %{SOURCE17} certum
cp -pi %{SOURCE18} certum
#cp -pi %{SOURCE19} certum
cp -pi %{SOURCE20} certum
for a in certum/*.pem; do
	mv -i "$a" "${a%.pem}.crt"
done

# http://www.sk.ee/en/Repository/certs/rootcertificates
# JUUR-SK, ESTEID-SK and ESTEID-SK 2007, ESTEID-SK 2011
install -d esteid
cp -pi %{SOURCE26} esteid
cp -pi %{SOURCE27} esteid
cp -pi %{SOURCE28} esteid/ESTEID-SK_2007.crt
cp -pi %{SOURCE29} esteid/ESTEID-SK_2011.crt
for a in esteid/*.PEM.cer; do
	mv -i "$a" "${a%.PEM.cer}.crt"
done

%build
install -d terena
openssl x509 -inform DER -in %{SOURCE21} -outform PEM -out terena/$(basename %{SOURCE21})
openssl x509 -inform DER -in %{SOURCE22} -outform PEM -out terena/$(basename %{SOURCE22})
openssl x509 -inform DER -in %{SOURCE23} -outform PEM -out terena/$(basename %{SOURCE23})
openssl x509 -inform DER -in %{SOURCE24} -outform PEM -out terena/$(basename %{SOURCE24})
openssl x509 -inform DER -in %{SOURCE25} -outform PEM -out terena/$(basename %{SOURCE25})
cp %{SOURCE30} terena/$(basename %{SOURCE30} .pem).crt
cp %{SOURCE31} terena/$(basename %{SOURCE31} .pem).crt
cp %{SOURCE32} terena/$(basename %{SOURCE32} .pem).crt
sed 's/\r//' %{SOURCE33} > terena/$(basename %{SOURCE33} .pem).crt
sed 's/\r//' %{SOURCE34} > terena/$(basename %{SOURCE34} .pem).crt
sed 's/\r//' %{SOURCE35} > terena/$(basename %{SOURCE35} .pem).crt
sed 's/\r//' %{SOURCE36} > terena/$(basename %{SOURCE36} .pem).crt

%{__make}

# We have those and more in specific dirs
%{__rm} mozilla/{Certum,Deutsche_Telekom_Root_CA_2}*.crt

# See TODO
# %{__rm} mozilla/RSA_Security_1024_v3.crt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},%{certsdir},/etc/pki/tls/certs,%{_sysconfdir}/ca-certificates.d}
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

ln -s %{certsdir}/ca-certificates.crt $RPM_BUILD_ROOT/etc/pki/tls/certs/ca-bundle.crt

%if %{with tests}
install -d pld-tests
cd pld-tests

# check for duplicates (to avoid X509_STORE_add_cert "cert already in hash table" problem)
cat $RPM_BUILD_ROOT%{certsdir}/ca-certificates.crt | awk '/BEGIN/ { i++; } /BEGIN/, /END/ { print > i ".extracted.crt" }'
for cert in *.extracted.crt; do
	openssl x509 -in "$cert" -noout -sha1 -fingerprint > "$cert.fingerprint"
done
DUPLICATES=$(sort *.fingerprint | uniq -c | sort -nr | awk ' { if ($1 != 1) { print $0; } } ')
if [ -n "$DUPLICATES" ]; then
	echo -e "\n\nFound duplicates for certificates (count, type, fingerprint):\n\n$DUPLICATES\n\nFailing..."
	exit 1
fi
cd ..
%endif

# The Debian path might be hard-coded in some binaries we cannot fix
# like the Steam client
install -d $RPM_BUILD_ROOT/etc/ssl
ln -s %{certsdir} $RPM_BUILD_ROOT/etc/ssl/certs

%clean
rm -rf $RPM_BUILD_ROOT

%post update
%{_sbindir}/update-ca-certificates --fresh || :

%files
%defattr(644,root,root,755)
%doc debian/README.Debian debian/changelog
%dir /etc/pki/tls
%dir /etc/pki/tls/certs
%dir /etc/ssl
/etc/ssl/certs
%config(noreplace) %verify(not md5 mtime size) /etc/pki/tls/certs/ca-bundle.crt
%config(noreplace) %verify(not md5 mtime size) %{certsdir}/ca-certificates.crt

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%dir %{_sysconfdir}/ca-certificates.d
%{_datadir}/ca-certificates
