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

%global major_version 9
%global minor_version 0
%global micro_version 50
%global redhat_version 00006
%global packdname apache-tomcat-%{version}.redhat-%{redhat_version}-src

# Specification versions
%global servletspec 4.0
%global jspspec 2.3
%global elspec 3.0

%global tcuid 91

# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_var}/lib/tomcat
%global appdir %{basedir}/webapps
%global homedir %{_datadir}/tomcat
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/tomcat
%global libdir %{_javadir}/tomcat
%global logdir %{_var}/log/tomcat
%global cachedir %{_var}/cache/tomcat
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _initrddir %{_sysconfdir}/init.d
%global _systemddir /lib/systemd/system

Name:          pki-servlet-engine
Epoch:         1
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       1%{?dist}
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API
Group:         System Environment/Daemons
License:       ASL 2.0
URL:           http://tomcat.apache.org/

#Source0:       http://www.apache.org/dist/tomcat/tomcat-%%{major_version}/v%%{version}/src/%%{packdname}.tar.gz
Source0:       tomcat-%{version}.redhat-%{redhat_version}-src.zip
Source1:       tomcat-%{major_version}.%{minor_version}.conf
Source3:       tomcat-%{major_version}.%{minor_version}.sysconfig
Source4:       tomcat-%{major_version}.%{minor_version}.wrapper
Source6:       tomcat-%{major_version}.%{minor_version}-digest.script
Source7:       tomcat-%{major_version}.%{minor_version}-tool-wrapper.script
Source8:       tomcat-%{major_version}.%{minor_version}.service
Source21:      tomcat-functions
Source30:      tomcat-preamble
Source31:      tomcat-server
Source32:      tomcat-named.service

Patch0:        tomcat-%{major_version}.%{minor_version}-bootstrap-MANIFEST.MF.patch
Patch1:        tomcat-%{major_version}.%{minor_version}-tomcat-users-webapp.patch
Patch2:        tomcat-%{major_version}.%{minor_version}-catalina-policy.patch
Patch3:        exclude-OSGi-metadata.patch

BuildArch:     noarch

BuildRequires: ant
BuildRequires: findutils
BuildRequires: java-11-devel
BuildRequires: javapackages-tools
BuildRequires: javapackages-local
BuildRequires: systemd
BuildRequires: systemd-rpm-macros
BuildRequires: aqute-bnd
BuildRequires: aqute-bndlib

Requires:      ant
Requires:      java-11-devel
Requires:      javapackages-tools
Requires:      procps
Requires(pre):    shadow-utils
Requires(post):   chkconfig
Requires(postun): chkconfig
Requires(preun):  chkconfig
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(preun): coreutils
Requires: pki-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}

# Add bundled so that everyone knows this is Tomcat.
Provides: bundled(tomcat) = %{version}.redhat-%{redhat_version}

Obsoletes:        pki-servlet-container <= 9.0.7

%description
Tomcat is the servlet engine that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%package -n pki-servlet-%{servletspec}-api
Group: Development/Libraries
Summary: Apache Tomcat Java Servlet v%{servletspec} API Implementation Classes
Requires(post): chkconfig
Requires(postun): chkconfig

%description -n pki-servlet-%{servletspec}-api
Apache Tomcat Servlet API Implementation Classes.

%prep
%setup -q -n %{packdname}

# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

# Since we don't support ECJ in RHEL anymore, remove the class that requires it
%{__rm} -f java/org/apache/jasper/compiler/JDTCompiler.java
# Also remove webservices naming factory as it's unused and causes unnecessary dependencies to be required
%{__rm} -rf java/org/apache/naming/factory/webservices

# Configure maven files
%mvn_package ":tomcat-servlet-api" tomcat-servlet-api


%build
export OPT_JAR_LIST="xalan-j2-serializer"

# Create a dummy file for later removal
touch HACK

# who needs a build.properties file anyway
%{ant} -Dbase.path="." \
  -Dbuild.compiler="modern" \
  -Dcommons-daemon.jar="HACK" \
  -Dcommons-daemon.native.src.tgz="HACK" \
  -Djdt.jar="HACK" \
  -Dtomcat-native.tar.gz="HACK" \
  -Dtomcat-native.home="." \
  -Dcommons-daemon.native.win.mgr.exe="HACK" \
  -Dnsis.exe="HACK" \
  -Dbnd.jar="$(build-classpath aqute-bnd/biz.aQute.bnd)" \
  -Dbndlib.jar="$(build-classpath aqute-bnd/biz.aQute.bndlib)" \
  -Dbndlibg.jar="$(build-classpath aqute-bnd/aQute.libg)" \
  -Dbndannotation.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
  -Dosgi-annotations.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
  -Dosgi-cmpn.jar="$(build-classpath osgi-compendium/osgi.cmpn)" \
  deploy dist-prepare dist-source

# remove some jars that we don't need
#%%{__rm} output/build/bin/commons-daemon.jar

%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initrddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_systemddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{bindir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > ${RPM_BUILD_ROOT}%{confdir}/conf.d/README
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{logdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tomcats
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{tempdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{workdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/tomcat

# move things into place
# First copy supporting libs to tomcat lib
pushd output/build
    %{__cp} -a bin/*.{jar,xml} ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} -a conf/*.{policy,properties,xml,xsd} ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -a lib/*.jar ${RPM_BUILD_ROOT}%{libdir}
popd

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/tomcat.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE3} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/tomcat
%{__install} -m 0644 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_sbindir}/tomcat
%{__install} -m 0644 %{SOURCE8} \
    ${RPM_BUILD_ROOT}%{_unitdir}/tomcat.service
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/tomcat-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE7} \
    > ${RPM_BUILD_ROOT}%{_bindir}/tomcat-tool-wrapper

%{__install} -m 0644 %{SOURCE21} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/tomcat/functions
%{__install} -m 0755 %{SOURCE30} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/tomcat/preamble
%{__install} -m 0755 %{SOURCE31} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/tomcat/server
%{__install} -m 0644 %{SOURCE32} \
    ${RPM_BUILD_ROOT}%{_unitdir}/tomcat@.service

# Substitute libnames in catalina-tasks.xml
sed -i \
   "s,el-api.jar,tomcat-el-%{elspec}-api.jar,;
    s,servlet-api.jar,tomcat-servlet-%{servletspec}-api.jar,;
    s,jsp-api.jar,tomcat-jsp-%{jspspec}-api.jar,;" \
    ${RPM_BUILD_ROOT}%{bindir}/catalina-tasks.xml

# create jsp and servlet API symlinks
pushd ${RPM_BUILD_ROOT}%{_javadir}
   %{__mv} tomcat/jsp-api.jar tomcat-jsp-%{jspspec}-api.jar
   %{__ln_s} tomcat-jsp-%{jspspec}-api.jar tomcat-jsp-api.jar
   %{__mv} tomcat/servlet-api.jar tomcat-servlet-%{servletspec}-api.jar
   %{__ln_s} tomcat-servlet-%{servletspec}-api.jar tomcat-servlet-api.jar
   %{__mv} tomcat/el-api.jar tomcat-el-%{elspec}-api.jar
   %{__ln_s} tomcat-el-%{elspec}-api.jar tomcat-el-api.jar
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/tomcat-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/tomcat-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/tomcat-el-%{elspec}-api.jar .
popd

# symlink to the FHS locations where we've installed things
pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

# Install the maven metadata
pushd res/maven
    for pom in *.pom; do
        # fix-up version in all pom files
        sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
    done
popd

%mvn_artifact res/maven/tomcat-servlet-api.pom output/build/lib/servlet-api.jar
%mvn_install

%pre
# add the tomcat user and group
%{_sbindir}/groupadd -g %{tcuid} -r tomcat 2>/dev/null || :
%{_sbindir}/useradd -c "Apache Tomcat" -u %{tcuid} -g tomcat \
    -s /sbin/nologin -r -d %{homedir} tomcat 2>/dev/null || :

%post
# install but don't activate
%systemd_post tomcat.service

# Collapse all of the alternatives installations into one
%{_sbindir}/update-alternatives --install %{_javadir}/jsp.jar jsp \
    %{_javadir}/tomcat-jsp-%{jspspec}-api.jar 20200
%{_sbindir}/update-alternatives --install %{_javadir}/servlet.jar servlet \
    %{_javadir}/tomcat-servlet-%{servletspec}-api.jar 30000
%{_sbindir}/update-alternatives --install %{_javadir}/elspec.jar elspec \
   %{_javadir}/tomcat-el-%{elspec}-api.jar 20300

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun tomcat.service

%postun
%systemd_postun_with_restart tomcat.service

# Collapse all of the alternatives removals into one
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jsp \
        %{_javadir}/tomcat-jsp-%{jspspec}-api.jar
    %{_sbindir}/update-alternatives --remove servlet \
        %{_javadir}/tomcat-servlet-%{servletspec}-api.jar
    %{_sbindir}/update-alternatives --remove elspec \
        %{_javadir}/tomcat-el-%{elspec}-api.jar
fi

%files
%defattr(0664,root,tomcat,0755)
%doc {LICENSE,NOTICE,RELEASE*}
%attr(0755,root,root) %{_bindir}/tomcat-digest
%attr(0755,root,root) %{_bindir}/tomcat-tool-wrapper
%attr(0755,root,root) %{_sbindir}/tomcat
%attr(0644,root,root) %{_unitdir}/tomcat.service
%attr(0644,root,root) %{_unitdir}/tomcat@.service
%attr(0755,root,root) %dir %{_libexecdir}/tomcat
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/tomcat/functions
%attr(0755,root,root) %{_libexecdir}/tomcat/preamble
%attr(0755,root,root) %{_libexecdir}/tomcat/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/tomcat
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}

%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}

%defattr(0664,root,tomcat,0770)
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}

%defattr(0644,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%config(noreplace) %{confdir}/tomcat.conf
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/context.xml
%config(noreplace) %{confdir}/server.xml
%attr(0640,root,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%attr(0664,root,tomcat) %{confdir}/tomcat-users.xsd
%attr(0664,root,tomcat) %config(noreplace) %{confdir}/jaspic-providers.xml
%attr(0664,root,tomcat) %{confdir}/jaspic-providers.xsd
%config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{bindir}/bootstrap.jar
%{bindir}/catalina-tasks.xml
%{homedir}/lib
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%{homedir}/logs
%{homedir}/conf

%defattr(-,root,root,-)
%dir %{libdir}
%{libdir}/*.jar
%{_javadir}/*.jar
%{bindir}/tomcat-juli.jar
%exclude %{_javadir}/tomcat-servlet-%{servletspec}*.jar

%files -n pki-servlet-%{servletspec}-api -f .mfiles-tomcat-servlet-api
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/tomcat-servlet-%{servletspec}*.jar

%changelog
* Thu Feb 24 2022 Chris Kelley <ckelley@redhat.com> - 1:9.0.50-1
- Update to JWS 5.6.1

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1:9.0.43-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jul 13 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.43-3
- Add back ant runtime dependency to allow compilation of JSPs at runtime (no ECJ support)

* Fri Jul 09 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.43-2
- Related: rhbz#1977948 Cleanup unused tomcat-juli.jar copy now that the maven artifacts have been removed

* Thu Jul 08 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.43-1
- Update to JWS 5.5, and drop jakarta-saaj dependency
- Updates to javapackages-local removed %%add_maven_depmap which broke the build,
  so I removed most of the maven artifacts as they aren't very useful anyway
- Cleaned up a few unnecessary patches

* Tue Jun 08 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.30-3
- Resolves: rhbz#1963851 CA instance installation fails with error message

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1:9.0.30-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Feb 03 2021 Alexander Scheel <ascheel@redhat.com> - 1:9.0.30-2
- Rebuild for RHEL 9

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
