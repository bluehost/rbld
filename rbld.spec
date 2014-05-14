Name:           rbld
Summary:        Daemon that reads lists of IP based blacklists or whitelists
Group:          System Environment/Daemons
Version:        1.3
Release:        1%{?dist}
License:        GPLv2+
Source:         %{name}-%{version}.tar.gz
URL:            https://github.com/bluehost/rbld
Packager:       %{packager}
Vendor:         %{vendor}
BuildArch:      noarch
Requires:       perl >= 5.8, perl-Proc-PID-File, perl-Proc-Daemon, perl-Data-Dump, perl-Time-HiRes, perl-YAML-Syck, perl-libwww-perl, perl-Getopt-Long
BuildRoot:      %{_tmppath}/%{name}-%{version}-build


%description
RBLD is a daemon that reads arbitrary lists of IP addresses as either 
blacklists or whitelists.  Clients can connect via Unix Domain Socket 
and query for an IP address.

RBLD is most useful for applications that require realtime low-latency 
lookups such as webservers, MTAs, and POP3/IMAP servers.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rbld.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rbld.d/lists
mkdir -p $RPM_BUILD_ROOT/%{_initddir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/rbld

install -D -m 0755 $RPM_BUILD_DIR/%{name}-%{version}/rbld.init $RPM_BUILD_ROOT/%{_initddir}/rbld
install -D -m 0644 rbld.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/rbld
install -D -m 0755 rbld $RPM_BUILD_ROOT/%{_sbindir}/rbld
install -D -m 0755 rbldstats $RPM_BUILD_ROOT/%{_sbindir}/rbldstats
install -D -m 0755 pullrbllists $RPM_BUILD_ROOT/%{_bindir}/pullrbllists

install -D -m 0644 rbld.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rbld.conf
install -D -m 0644 lists.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rbld.d/lists.conf
install -D -m 0644 pullrbllists.yml $RPM_BUILD_ROOT/%{_sysconfdir}/rbld.d/pullrbllists.yml

install -D -m 0644 rbld.conf.example $RPM_BUILD_ROOT/%{_datadir}/rbld/rbld.conf.example
install -D -m 0644 lists.conf.example $RPM_BUILD_ROOT/%{_datadir}/rbld/lists.conf.example
install -D -m 0644 pullrbllists.yml.example $RPM_BUILD_ROOT/%{_datadir}/rbld/pullrbllists.yml.example
install -D -m 0644 COPYING $RPM_BUILD_ROOT/%{_datadir}/rbld/COPYING

%post
# Register the rbld service
/sbin/chkconfig --add rbld

%preun
if [ $1 = 0 ]; then
        /sbin/service rbld stop > /dev/null 2>&1
        /sbin/chkconfig --del rbld
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/pullrbllists
%{_sbindir}/rbld
%{_sbindir}/rbldstats
%{_initddir}/rbld
%dir %{_sysconfdir}/rbld.d
%dir %{_sysconfdir}/rbld.d/lists
%config(noreplace) %{_sysconfdir}/sysconfig/rbld
%config(noreplace) %{_sysconfdir}/rbld.conf
%config(noreplace) %{_sysconfdir}/rbld.d/lists.conf
%{_datadir}/rbld/rbld.conf.example
%{_datadir}/rbld/lists.conf.example
%{_datadir}/rbld/pullrbllists.yml.example
%{_datadir}/rbld/COPYING

%attr(0600, root, root) %config(noreplace) %{_sysconfdir}/rbld.d/pullrbllists.yml

%changelog
* Mon Jan 20 2014 Erick Cantwell <ecantwell@bluehost.com> 1.3-1
- Added Licensing information to all scripts
- Include COPYING file containing the GPLv2 license

* Mon Jan 20 2014 Erick Cantwell <ecantwell@bluehost.com> 1.2-2
- Added example configuration files

* Fri Jan 17 2014 Erick Cantwell <ecantwell@bluehost.com> 1.2-1
- Made pullrbllists compatible with perl 5.10
- Updated pullrbllists so that it can do basic authentication
- Since pullrbllists can contain passwords, make permissions 0600
- by default

* Fri Jan 17 2014 Erick Cantwell <ecantwell@bluehost.com> 1.1-2
- Changed rbld lists file so that it doesn't have Bluehost specific
- configuration files as examples

* Fri Jan 17 2014 Erick Cantwell <ecantwell@bluehos.tcom> 1.1-1
- Fixed syntax error in init script so that it can actually be added and used
- Made defaults for pullrbllists sane
- Changed default socket group in rbld.conf from apache to root
- Fixed bug in rbldstats which caused it to non-gracefully error when it
- couldn't connect to rbld

* Wed Jan 15 2014 Erick Cantwell <ecantwell@bluehost.com> 1.0-2
- Include rbldstats script

* Tue Jan 14 2014 Erick Cantwell <ecantwell@bluehost.com> 1.0-1
- Initial build of rbld as RPM
