Name:           pinpam
Version:        0.0.4
Release:        1%{?dist}
Summary:        TPM2 backed PAM module and utility for pin-based authentication

License:        GPL-3.0-or-later
URL:            https://github.com/RazeLighter777/pinpam
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        pinpam-policy.conf

BuildRequires:  rust-packaging >= 21
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tss-devel
BuildRequires:  pam-devel

%description
TPM2 backed PAM module and utility for pin-based authentication.
It uses TPM2 to store and verify PINs, providing a secure way
to authenticate users.

%prep
%autosetup -n %{name}-%{version}
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
# Setuid for pinutil so it can access the TPM device
chmod 4755 %{buildroot}%{_bindir}/pinutil

# Install the PAM module (cargo install doesn't handle cdylibs)
install -Dpm 0755 target/release/libpinpam.so %{buildroot}%{_libdir}/security/libpinpam.so

# Install the policy configuration
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pinpam/policy.conf

%check
%cargo_test

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/pinutil
%{_libdir}/security/libpinpam.so
%dir %{_sysconfdir}/pinpam
%config(noreplace) %{_sysconfdir}/pinpam/policy.conf

%changelog
* Sat Mar 28 2026 Bernhard Friedreich <friesoft@gmail.com> - 0.0.4-1
- Initial package for Fedora
