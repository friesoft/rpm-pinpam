## Prerequisites
```
$ sudo dnf install mock
$ sudo usermod -a -G mock username
```

## Building
```
$ rpmdev-setuptree 
$ spectool -g -C ~/rpmbuild/SOURCES pinpam.spec
$ cp pinpam-policy.conf ~/rpmbuild/SOURCES/
$ rpmbuild -bs pinpam.spec
$ mock -r fedora-43-x86_64 rebuild ~/rpmbuild/SRPMS/pinpam-0.0.4-1.fc43.src.rpm 
```

