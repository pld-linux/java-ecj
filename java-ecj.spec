Summary:	Eclipse Compiler for Java
Summary(pl.UTF-8):	Eclipse Compiler for Java - kompilator Javy platformy Eclipse
Name:		java-ecj
Version:	4.9
Release:	2
License:	Eclipse Public License v1.0
Group:		Development/Languages/Java
Source0:	ftp://sourceware.org/pub/java/ecj-%{version}-source.tar.bz2
# Source0-md5:	056b8a279a6cb6a6baef4205ef0be5a8
Patch0:		%{name}-nodummysymbol.patch
URL:		http://www.eclipse.org/jdt/core/
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
# for %{_javadir}
Requires:	jpackage-utils
Requires:	jre
Obsoletes:	eclipse-ecj
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ECJ is the Java bytecode compiler of the Eclipse Platform. It is also
known as the JDT Core batch compiler.

%description -l pl.UTF-8
ECJ to kompilator kodu bajtowego Javy platformy Eclipse. Jest znany
także jako kompilator wsadowy JDT Core.

%prep
%setup -q -c
%patch0 -p1

%{__sed} -i -e 's/^	ecj /	$(ECJ) /' Makefile
%{__sed} -i -e 's/-1\.5/-source 1.5 -target 1.5/' Makefile

%build
#export JAVA_HOME="%{java_home}"

%{__make} compile \
	ECJ=javac

%{__make} ecj.jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir}}

cp -p ecj.jar $RPM_BUILD_ROOT%{_javadir}

cat >$RPM_BUILD_ROOT%{_bindir}/ecj <<EOF
#!/bin/sh

CLASSPATH="%{_datadir}/ecj.jar${CLASSPATH:+:$CLASSPATH}" \
java org.eclipse.jdk.internal.compiler.batch.Main "$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/ecj
%{_javadir}/ecj.jar
