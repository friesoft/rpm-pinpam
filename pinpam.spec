Name:           pinpam
Version:        0.0.4
Release:        1%{?dist}
Summary:        TPM2 backed PAM module and utility for pin-based authentication

License:        GPL-3.0-or-later
URL:            https://github.com/RazeLighter777/pinpam
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        pinpam-policy.conf

BuildRequires:  cargo
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tss-devel
BuildRequires:  pam-devel

%description
TPM2 backed PAM module and utility for pin-based authentication.
It uses TPM2 to store and verify PINs, providing a secure way
to authenticate users.

%prep
%autosetup -n %{name}-%{version}
# No cargo_prep here to allow network access for dependencies

%build
export CARGO_HOME=$(pwd)/.cargo
cargo build --release --locked

%install
# Custom install since we aren't using %cargo_install
install -Dpm 0755 target/release/pinutil %{buildroot}%{_bindir}/pinutil
chmod 4755 %{buildroot}%{_bindir}/pinutil

# Install the PAM module
install -Dpm 0755 target/release/libpinpam.so %{buildroot}%{_libdir}/security/libpinpam.so

# Install the policy configuration
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pinpam/policy.conf

%check
export CARGO_HOME=$(pwd)/.cargo
cargo test --release --locked

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
