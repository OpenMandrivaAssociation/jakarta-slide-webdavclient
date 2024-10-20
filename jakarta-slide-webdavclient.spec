# Copyright (c) 2000-2007, JPackage Project
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
%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section		devel
%define base_name	slide

Summary:	Slide WebDAV client
Name:		jakarta-slide-webdavclient
Version:	2.1
Release:	4.0.8
Group:		Development/Java
License:	Apache Software License
Url:		https://jakarta.apache.org/slide/
Source0:	jakarta-slide-webdavclient-src-2.1.tar.gz
Source1:	%{name}.sh
Source2:	jakarta-slide-webdavclient-2.2-WebdavResource.java
Source3:	slide-webdavlib-2.1.pom
Patch0:		jakarta-slide-webdavclient-3.0-compat.patch
%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-antlr
BuildRequires:	antlr
BuildRequires:	geronimo-j2ee-connector-1.5-api
BuildRequires:	geronimo-jta-1.0.1B-api
BuildRequires:	jakarta-commons-httpclient >= 3.0
BuildRequires:	jakarta-commons-transaction
BuildRequires:	java-rpmbuild
BuildRequires:	jdom
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	servletapi5
BuildRequires:	xml-im-exporter
BuildRequires:	xml-im-exporter
Requires:	geronimo-j2ee-connector-1.5-api
Requires:	geronimo-jta-1.0.1B-api
Requires:	jakarta-commons-httpclient
Requires:	jakarta-commons-transaction
Requires:	jdom
Requires:	xml-im-exporter

%description
Slide includes a fully featured WebDAV client library and command line
client.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
%{summary}.

%prep
%setup -qn jakarta-slide-webdavclient-src-2.1
%remove_java_binaries
cp %{SOURCE2} clientlib/src/java/org/apache/webdav/lib/WebdavResource.java

%patch0 -p0 -b .sav

%build
export CLASSPATH=$(build-classpath \
antlr \
commons-httpclient \
commons-httpclient-contrib \
commons-transaction \
j2ee-connector \
jta \
servlet \
jdom \
xml-im-exporter \
)
%ant \
	-Dbuild.sysclasspath=first \
	-Dant.build.javac.source=1.4

%install
install -dm 755 %{buildroot}%{_bindir}
install -pm 755 %{SOURCE1} %{buildroot}%{_bindir}/webdavclient

install -dm 755 %{buildroot}%{_javadir}/%{base_name}
install -pm 644 \
	dist/lib/jakarta-slide-webdavlib-%{version}.jar \
	%{buildroot}%{_javadir}/%{base_name}/%{name}-webdavlib-%{version}.jar
install -pm 644 \
	dist/lib/jakarta-slide-commandline-%{version}.jar \
	%{buildroot}%{_javadir}/%{base_name}/%{name}-commandline-%{version}.jar
(cd %{buildroot}%{_javadir}/%{base_name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
(cd %{buildroot}%{_javadir}/%{base_name} && for jar in jakarta-*.jar; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)

%add_to_maven_depmap slide slide-webdavlib %{version} JPP/slide jakarta-slide-webdavclient-webdavlib
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 %{SOURCE3} \
	%{buildroot}%{_datadir}/maven2/poms/JPP.slide-jakarta-slide-webdavclient-webdavlib.pom
#javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/doc/clientjavadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%doc LICENSE
%{_javadir}/%{base_name}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%attr(0755,root,root) %{_bindir}/webdavclient
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-*-%{version}.jar.*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

