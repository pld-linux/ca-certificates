# TODO
# - make amsn use system certs
# - make pidgin use system certs
# - swap %{certsdir}/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt regards file vs symlink
#
# Conditional build:
%bcond_without	tests	# certificate duplicate and expiry checks

Summary:	Common CA Certificates PEM files
Summary(pl.UTF-8):	Pliki PEM popularnych certyfikatów CA
Name:		ca-certificates
%define	ver_date	20260601
Version:	%{ver_date}
Release:	6
License:	GPL v2 (scripts), MPL v2 (mozilla certs), distributable (other certs)
Group:		Base
Source0:	https://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.xz
# Source0-md5:	987199e8918ed427ec494a1a716241b0
# https://www.certum.pl/pl/cert_wiedza_zaswiadczenia_klucze_certum/
Source15:	https://repository.certum.pl/class1casha2.pem
# Source15-md5:	b52dde6e2618a21965afbe6d6676d09f
Source16:	https://repository.certum.pl/dvcasha2.pem
# Source16-md5:	88ce64a84375c95ab6f7c8515dd2a117
Source17:	https://repository.certum.pl/ovcasha2.pem
# Source17-md5:	3149c923bd23469d6b14caa6334f8b63
Source18:	https://repository.certum.pl/evcasha2.pem
# Source18-md5:	ac54dc6cf3af7e243879b1c8b4aca8a3
Source19:	https://repository.certum.pl/ctnca-ctrca.pem
# Source19-md5:	ea746f231a0f20ae4a5bd98aa6062900
Source20:	https://repository.certum.pl/gscasha2.pem
# Source20-md5:	a29d37f95dafc08cef36015922e3b0d3
Source21:	https://files.certum.eu/documents/klucze_ca/CertumTrustedNetworkCA/CROSS-CTNCA-CTNCA2.crt
# Source21-md5:	c03631774d30bdc4f2ce283959334dbf
Source22:	https://repository.certum.pl/ctnca-cec384ca.pem
# Source22-md5:	8b8273bcb8390ae473183985cafe079c
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-more-certs.patch
Patch2:		%{name}-etc-certs.patch
Patch3:		%{name}-DESTDIR.patch
Patch4:		%{name}.d.patch
Patch5:		%{name}-p11-kit.patch
URL:		https://packages.debian.org/sid/ca-certificates
%if %{with tests}
BuildRequires:	openssl-tools
%endif
BuildRequires:	python3
BuildRequires:	python3-cryptography
BuildRequires:	python3-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post):	coreutils
Requires(post):	findutils
Requires(post):	grep
Requires(post):	p11-kit
Requires(post):	sed
Requires(postun):	coreutils
Requires:	coreutils
Requires:	findutils
Requires:	grep
Requires:	p11-kit
Requires:	sed
Provides:	ca-certificates-update = %{version}-%{release}
Obsoletes:	ca-certificates-update < 20260601-2
Obsoletes:	certificates < 1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certsdir	/etc/certs
%define		openssldir	/etc/openssl/certs

%description
Common CA Certificates PEM files.

%description -l pl.UTF-8
Pliki PEM popularnych certyfikatów CA.

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
cp -pi %{SOURCE15} certum
cp -pi %{SOURCE16} certum
cp -pi %{SOURCE17} certum
cp -pi %{SOURCE18} certum
cp -pi %{SOURCE19} certum
cp -pi %{SOURCE20} certum
cp -pi %{SOURCE21} certum
cp -pi %{SOURCE22} certum
for a in certum/*.pem; do
	mv -i "$a" "${a%.pem}.crt"
done

%build
cd ca-certificates
%{__make}

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
./sbin/update-ca-certificates --destdir $RPM_BUILD_ROOT

ln -s %{certsdir}/ca-certificates.crt $RPM_BUILD_ROOT/etc/pki/tls/certs/ca-bundle.crt

%if %{with tests}
install -d pld-tests
cd pld-tests

# regex for subjects of allowed expired certs; empty allows none
ALLOW_EXPIRED=""
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
		SUBJECT=$(openssl x509 -in "$cert" -noout -subject | sed 's/^subject= *//')
		if [ -n "$ALLOW_EXPIRED" ] && echo "$SUBJECT" | grep -E "$ALLOW_EXPIRED"; then
			echo "EXPIRED CERT IN WHITELIST"
		else
			exit 1
		fi
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

%post
%{_sbindir}/update-ca-certificates --fresh || :

%postun
# remove only what update-ca-certificates installed; local admin files stay
if [ "$1" = "0" ] && [ -f %{openssldir}/.manifest ]; then
	while IFS= read -r f; do
		case "$f" in ''|*/*) continue ;; esac
		rm -f "%{openssldir}/$f"
	done < %{openssldir}/.manifest
	rm -f %{openssldir}/.manifest
fi

%pretrans -p <lua>
local mode = posix.stat("/etc/ssl/certs")
if mode and mode["type"] == "link" then
	posix.unlink("/etc/ssl/certs")
end

%files
%defattr(644,root,root,755)
%doc ca-certificates/debian/{README.Debian,changelog}
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%dir /etc/pki/tls
%dir /etc/pki/tls/certs
%dir /etc/ssl
%dir /etc/ssl/certs
/etc/ssl/certs/ca-certificates.crt
%config(noreplace) %verify(not md5 mtime size) /etc/pki/tls/certs/ca-bundle.crt
%verify(not md5 mtime size) %{certsdir}/ca-certificates.crt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%dir %{_sysconfdir}/ca-certificates.d
%{_datadir}/ca-certificates
