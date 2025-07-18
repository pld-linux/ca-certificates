# TODO
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
%define	ver_date	20250419
Version:	%{ver_date}
Release:	1
License:	GPL v2 (scripts), MPL v2 (mozilla certs), distributable (other certs)
Group:		Base
Source0:	https://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.xz
# Source0-md5:	d3b07ed9bd2d2f966419aa0b1c3fad23
Source2:	https://www.certum.pl/keys/CA.pem
# Source2-md5:	35610177afc9c64e70f1ce62c1885496
Source14:	https://www.certum.pl/CTNCA.pem
# Source14-md5:	231b5b8bf05c5e93a9b2ebc4186eb6f7
Source15:	https://repository.certum.pl/class1casha2.pem
# Source15-md5:	b52dde6e2618a21965afbe6d6676d09f
Source16:	https://repository.certum.pl/dvcasha2.pem
# Source16-md5:	88ce64a84375c95ab6f7c8515dd2a117
Source17:	https://repository.certum.pl/ovcasha2.pem
# Source17-md5:	3149c923bd23469d6b14caa6334f8b63
Source18:	https://repository.certum.pl/evcasha2.pem
# Source18-md5:	ac54dc6cf3af7e243879b1c8b4aca8a3
#Source19:	http://repository.certum.pl/dvcasha2.pem
## Source19-md5:	88ce64a84375c95ab6f7c8515dd2a117
Source20:	https://repository.certum.pl/gscasha2.pem
# Source20-md5:	a29d37f95dafc08cef36015922e3b0d3
Source23:	https://crt.tcs.terena.org/TERENAPersonalCA.crt
# Source23-md5:	53eaa497c8fb0b79f14fe9f69693689a
Source24:	https://crt.tcs.terena.org/TERENAeSciencePersonalCA.crt
# Source24-md5:	e25cc655d3ebe920ca9c187e3dde9191
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-more-certs.patch
Patch2:		%{name}-etc-certs.patch
Patch3:		%{name}-DESTDIR.patch
Patch4:		%{name}.d.patch
Patch5:		no-openssl-rehash.patch
URL:		https://packages.debian.org/sid/ca-certificates
BuildRequires:	openssl-tools
BuildRequires:	python3
BuildRequires:	python3-cryptography
BuildRequires:	python3-packaging
BuildRequires:	python3-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	unzip
BuildRequires:	xz
Obsoletes:	certificates < 1.2
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
Requires:	openssl-tools >= 0.9.8i-3

%description update
Script and data for updating CA Certificates database.

%description update -l pl.UTF-8
Skrypt i dane do odświeżania bazy certyfikatów CA.

%prep
%setup -qc
cd ca-certificates
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%{__sed} -i -e 's,@openssldir@,%{openssldir},' sbin/update-ca-certificates*

install -d certum
cp -pi %{SOURCE2} certum
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

%build
cd ca-certificates
install -d terena
openssl x509 -inform DER -in %{SOURCE23} -outform PEM -out terena/$(basename %{SOURCE23})
openssl x509 -inform DER -in %{SOURCE24} -outform PEM -out terena/$(basename %{SOURCE24})

%{__make}

# We have those and more in specific dirs
%{__rm} mozilla/Certum*.crt

make_sure_expired_and_rm() {
	cert="$1"
	rm -rf pld-tests
	install -d pld-tests
	cat "$cert" |  awk '/^-+BEGIN/ { i++; } /^-+BEGIN/, /^-+END/ { print > "pld-tests/" i ".extracted.crt" }'
	for tmpcert in pld-tests/*.extracted.crt; do
		# check expiration date
		EXPDATE=$(openssl x509 -enddate -noout -in "$tmpcert")
		EXPDATE=${EXPDATE#notAfter=}
		EXPDATETIMESTAMP=$(date +"%s" -d "$EXPDATE")
		NOWTIMESTAMP=$(date +"%s")
		# mksh is 32bit only
		if /usr/bin/test "$EXPDATETIMESTAMP" -ge "$NOWTIMESTAMP"; then
			echo "$cert ($tmpcert): not expired! ${EXPDATE}"
			return 1
		fi
	done
	rm "$cert"
	return 0
}

# See TODO
# %{__rm} mozilla/RSA_Security_1024_v3.crt

%install
rm -rf $RPM_BUILD_ROOT
cd ca-certificates
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
cat $RPM_BUILD_ROOT%{certsdir}/ca-certificates.crt | awk '/^-+BEGIN/ { i++; } /^-+BEGIN/, /^-+END/ { print > i ".extracted.crt" }'
for cert in *.extracted.crt; do
	openssl x509 -in "$cert" -noout -sha1 -fingerprint > "$cert.fingerprint"


	# check expiration date
	EXPDATE=$(openssl x509 -enddate -noout -in "$cert")
	EXPDATE=${EXPDATE#notAfter=}
	EXPDATETIMESTAMP=$(date +"%s" -d "$EXPDATE")
	NOWTIMESTAMP=$(date +"%s")
	# mksh is 32bit only
	if /usr/bin/test "$EXPDATETIMESTAMP" -lt "$NOWTIMESTAMP"; then
		echo "!!! Expired certificate: $cert"
		openssl x509 -subject -issuer -startdate -enddate -email -alias -noout -in "$cert"
		echo "Fingerprint: $(cat "$cert.fingerprint")"
		echo "\n\n"
		exit 1
	fi
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
install -d $RPM_BUILD_ROOT/etc/ssl/certs
ln -s %{certsdir}/ca-certificates.crt $RPM_BUILD_ROOT/etc/ssl/certs

%clean
rm -rf $RPM_BUILD_ROOT

%post update
%{_sbindir}/update-ca-certificates --fresh || :

%postun update
/usr/bin/find "%{openssldir}" -xtype l -delete || :

%pretrans -p <lua>
local mode = posix.stat("/etc/ssl/certs")
if mode and mode["type"] == "link" then
	posix.unlink("/etc/ssl/certs")
end

%files
%defattr(644,root,root,755)
%doc ca-certificates/debian/{README.Debian,changelog}
%dir /etc/pki/tls
%dir /etc/pki/tls/certs
%dir /etc/ssl
%dir /etc/ssl/certs
/etc/ssl/certs/ca-certificates.crt
%config(noreplace) %verify(not md5 mtime size) /etc/pki/tls/certs/ca-bundle.crt
%verify(not md5 mtime size) %{certsdir}/ca-certificates.crt

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%dir %{_sysconfdir}/ca-certificates.d
%{_datadir}/ca-certificates
