%global pkg_name felix-osgi-compendium
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

%global bundle org.osgi.compendium
%global felixdir %{_javadir}/felix
%global POM %{_mavenpomdir}/JPP.felix-%{bundle}.pom

Name:    %{?scl_prefix}%{pkg_name}
Version: 1.4.0
Release: 19.11%{?dist}
Summary: Felix OSGi R4 Compendium Bundle

License: ASL 2.0
URL:     http://felix.apache.org
Source0: http://www.apache.org/dist/felix/%{bundle}-%{version}-project.tar.gz

Patch0:         0001-Fix-servlet-api-dependency.patch
Patch1:         0002-Fix-compile-target.patch
Patch2:         0003-Add-CM_LOCATION_CHANGED-property-to-ConfigurationEve.patch
Patch3:         0004-Add-TARGET-property-to-ConfigurationPermission.patch
# This is an ugly patch that adds getResourceURL method. This prevents jbosgi-framework
# package from bundling osgi files. Once the jbosgi-framework will be updated
# to a new version without the need for this patch, REMOVE it!
Patch4:         0005-Add-getResourceURL-method-to-make-jbosgi-framework-h.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix_java_common}javapackages-tools
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-surefire-provider-junit
BuildRequires: %{?scl_prefix}felix-parent
BuildRequires: %{?scl_prefix}felix-osgi-core
BuildRequires: %{?scl_prefix}felix-osgi-foundation
BuildRequires: %{?scl_prefix_java_common}tomcat-servlet-3.0-api

%description
OSGi Service Platform Release 4 Compendium Interfaces and Classes.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{bundle}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# fix servlet api properly
%patch0 -p1
# fix compile source/target
%patch1 -p1
# add CM_LOCATION_CHANGED property
%patch2 -p1
# add TARGET property
%patch3 -p1
# add getResourceURL method
%patch4 -p1

%mvn_file :%{bundle} "felix/%{bundle}"
%mvn_alias "org.apache.felix:%{bundle}" "org.osgi:%{bundle}"
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.4.0-19.11
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.4.0-19.10
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.4.0-19.9
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 1.4.0-19.8
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.4.0-19.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.3
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-19.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.0-19
- Mass rebuild 2013-12-27

* Wed Sep 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-18
- Add missing BR: felix-parent

* Thu Aug 22 2013 Michal Srb <msrb@redhat.com> - 1.4.0-17
- Migrate away from mvn-rpmbuild (Resolves: rhbz#997463)

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-16
- Remove workaround for rpm bug #646523

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.0-15
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.0-13
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Marek Goldmann <mgoldman@redhat.com> 1.4.0-11
- Add getResourceURL method to XMLParserActivator

* Fri Jun 15 2012 Marek Goldmann <mgoldman@redhat.com> 1.4.0-10
- Add CM_LOCATION_CHANGED property to ConfigurationEvent
- Add TARGET property to ConfigurationPermission

* Wed Mar 21 2012 Alexander Kurtakov <akurtako@redhat.com> 1.4.0-9
- Move to tomcat 7.x servlet api.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.0-7
- Add org.osgi groupId to depmap
- Packaging fixes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.0-5
- Fix servlet api in pom

* Mon Dec 27 2010 Mat Booth <fedora@matbooth.co.uk> 1.4.0-4
- Fix POM names RHBZ #655800.
- Versionless jars/docs, update maven plug-in BRs.
- Other misc guideline compliances.

* Mon Jul 12 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.4.0-3
- Avoid owning the %%{_javadir}/%%{project} directory

* Wed Jul 07 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.4.0-2
- Use maven instead of ant

* Tue Jun 22 2010 Victor G. Vasilyev <victor.vasilyev@sun.com> 1.4.0-1
- Release 1.4.0
