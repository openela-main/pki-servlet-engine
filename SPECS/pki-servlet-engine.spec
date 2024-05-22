# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:          pki-servlet-engine
Epoch:         1
Version:       9.0.62
Release:       1%{?dist}
Summary:       Servlet Engine for PKI
Group:         System Environment/Daemons
License:       ASL 2.0
URL:           http://tomcat.apache.org
BuildArch:     noarch

Requires:      tomcat

Obsoletes:     pki-servlet-container < %{epoch}:%{version}-%{release}

Obsoletes:     pki-servlet-4.0-api < %{epoch}:%{version}-%{release}
Provides:      pki-servlet-4.0-api = %{epoch}:%{version}-%{release}

%description
The pki-servlet-engine package has been replaced by the tomcat package.
This package is provided for backward compatibility only, so it contains
no files and will be removed in the future. Please use the tomcat package
directly instead.

%files

%changelog
* Mon Feb 05 2024 Red Hat PKI Team <rhcs-maint@redhat.com> - 1:9.0.62-1
- Bump version number to avoid conflicts with tomcat

* Wed Jan 31 2024 Red Hat PKI Team <rhcs-maint@redhat.com> - 1:9.0.30-4
- Convert pki-servlet-engine into an alias for tomcat

* Fri Jun 11 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.30-3
- Reverts: rhbz#1969366 as it causes other issues

* Tue Jun 08 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.30-2
- Resolves: rhbz#1969366 CA instance installation fails with error message

* Thu Apr 23 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.30-1
- Resolves: rhbz#1721684 Rebase pki-servlet-engine to 9.0.30
- Update to JWS 5.3.0 distribution
- Remove new dependencies that PKI doesn't need (and are not provided by RHEL 8)

* Fri May 31 2019 Endi S. Dewata <edewata@redhat.com> - 1:9.0.7-16
- Obsoleted pki-servlet-container

* Tue Apr 23 2019 Endi S. Dewata <edewata@redhat.com> - 1:9.0.7-15
- Rename pki-servlet-container into pki-servlet-engine

* Mon Mar 04 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.7-14
- Update to JWS 5.0.2 distribution
- Resolves: rhbz#1658846 CVE-2018-8034 pki-servlet-container: tomcat: host name verification missing in WebSocket client
- Resolves: rhbz#1579614 CVE-2018-8014 pki-servlet-container: tomcat: Insecure defaults in CORS filter enable 'supportsCredentials' for all origins
- Resolves: rhbz#1619232 - CVE-2018-8037 pki-servlet-container: tomcat: Due to a mishandling of close in NIO/NIO2 connectors user sessions can get mixed up
- Resolves: rhbz#1641874 - CVE-2018-11784 pki-servlet-container: tomcat: Open redirect in default servlet

* Fri Aug 03 2018 Fraser Tweedale <ftweedal@redhat.com> - 1:9.0.7-13
- Reinstate Maven artifacts and fix maven-metadata JAR path

* Fri Jul 20 2018 Jean-Frederic Clere <jclere@redhat.com> - 1:9.0.7-12
- Add missing BuildRequires: systemd-units

* Fri Jun 22 2018 Coty Sutherland <csutherl@redhat.com> - 1:9.0.7-11
- Resolves: rhbz#1594139 Cleanup Provides and Requires

* Thu Jun 07 2018 Coty Sutherland <csutherl@redhat.com> - 1:9.0.7-10
- Create packages for FreeIPA that wrap the JWS distribution of Tomcat
