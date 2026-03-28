Name:           pinpam
Version:        0.0.4
Release:        2%{?dist}
Summary:        TPM2 backed PAM module and utility for pin-based authentication

License:        GPL-3.0-or-later
URL:            https://github.com/RazeLighter777/pinpam
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        pinpam-policy.conf

BuildRequires:  cargo
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tss-devel
BuildRequires:  pam-devel
# For udev rules and tss group management
BuildRequires:  systemd-devel

# Ensure TPM2 TSS libraries are available at runtime
Requires:       tpm2-tss
# PAM is required
Requires:       pam

%description
TPM2 backed PAM module and utility for pin-based authentication.
It uses TPM2 to store and verify PINs, providing a secure way
to authenticate users.

%prep
%autosetup -n %{name}-%{version}

%build
export CARGO_HOME=$(pwd)/.cargo
cargo build --release --locked

%install
# Install the utility
install -Dpm 0755 target/release/pinutil %{buildroot}%{_bindir}/pinutil

# Install the PAM module
install -Dpm 0755 target/release/libpinpam.so %{buildroot}%{_libdir}/security/libpinpam.so

# Install the policy configuration (NOTE: filename must be 'policy' not 'policy.conf')
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pinpam/policy

# Install udev rules for TPM access (Setgid method support)
mkdir -p %{buildroot}%{_udevrulesdir}
cat > %{buildroot}%{_udevrulesdir}/70-pinpam-tpm.rules <<EOF
# TPM device access for tss group (required for pinpam)
KERNEL=="tpm[0-9]*", TAG+="systemd", MODE="0660", GROUP="tss"
KERNEL=="tpmrm[0-9]*", TAG+="systemd", MODE="0660", GROUP="tss"
EOF

%check
export CARGO_HOME=$(pwd)/.cargo
cargo test --release --locked

%files
%license LICENSE.txt
%doc README.md
# Setuid root allows regular users to interact with the TPM via pinutil
%attr(4755, root, root) %{_bindir}/pinutil
%{_libdir}/security/libpinpam.so
%dir %{_sysconfdir}/pinpam
%config(noreplace) %{_sysconfdir}/pinpam/policy
%{_udevrulesdir}/70-pinpam-tpm.rules

%changelog
* Sat Mar 28 2026 Bernhard Friedreich <friesoft@gmail.com> - 0.0.4-1
- Fix policy filename to match code expectations
- Add setuid bit to pinutil for TPM access

