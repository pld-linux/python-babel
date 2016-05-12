#
# TODO:
#	- tests fail on 'local' timezone
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# test target
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define	        module 	babel
Summary:	Babel - internationalization library for Python 2
Summary(pl.UTF-8):	Babel - biblioteka umiędzynaradawiająca dla Pythona 2
Name:		python-%{module}
Version:	2.3.4
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/Babel
Source0:	https://pypi.python.org/packages/6e/96/ba2a2462ed25ca0e651fb7b66e7080f5315f91425a07ea5b34d7c870c114/Babel-%{version}.tar.gz
# Source0-md5:	afa20bc55b0e991833030129ad498f35
Patch0:		tz.patch
URL:		http://babel.pocoo.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-devel-tools >= 1:2.6
BuildRequires:	python-setuptools
BuildRequires:	python-pytz
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-devel-tools >= 1:3.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-pytz
%endif
%{?with_doc:BuildRequires: sphinx-pdg}
Requires:	python-modules >= 1:2.6
Requires:	python-pytz
Obsoletes:	python-Babel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

%description -l pl.UTF-8
Babel to biblioteka Pythona zawierająca zintegrowany zbiór narzędzi
pomagających przy umiędzynaradawianiu i lokalizowaniu aplikacji w
Pythonie (w szczególności aplikacji WWW).

%package -n python3-%{module}
Summary:	Babel - internationalization library for Python 3
Summary(pl.UTF-8):	Babel - biblioteka umiędzynaradawiająca dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3
Requires:	python3-pytz

%description -n python3-%{module}
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

%description -n python3-%{module} -l pl.UTF-8
Babel to biblioteka Pythona zawierająca zintegrowany zbiór narzędzi
pomagających przy umiędzynaradawianiu i lokalizowaniu aplikacji w
Pythonie (w szczególności aplikacji WWW).

%package apidocs
Summary:	Python Babel API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona Babel
Group:		Documentation

%description apidocs
Python Babel API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona Babel.

%prep
%setup -q -n Babel-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
%{__rm} -r _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{pybabel,pybabel3}
%endif

%if %{with python2}
%py_install

%py_postclean
%endif

find $RPM_BUILD_ROOT%{py_sitescriptdir}/babel/locale-data -name '*.dat' | \
	sed -e "s#^$RPM_BUILD_ROOT##" | \
	sed -ne 's,.*/\([a-z][a-z][a-z]\?\)\(_[0-9][0-9][0-9]\|_[A-Z][a-z][a-z][a-z]\)\?\(_[A-Z][A-Z]\)\?\(_POSIX\)\?\.dat$,%lang(\1\3) &,p' > py2.lang

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/babel/locale-data -name '*.dat' | \
	sed -e "s#^$RPM_BUILD_ROOT##" | \
	sed -ne 's,.*/\([a-z][a-z][a-z]\?\)\(_[0-9][0-9][0-9]\|_[A-Z][a-z][a-z][a-z]\)\?\(_[A-Z][A-Z]\)\?\(_POSIX\)\?\.dat,%lang(\1\3) &,p' > py3.lang

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files -f py2.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%attr(755,root,root) %{_bindir}/pybabel
%dir %{py_sitescriptdir}/babel
%{py_sitescriptdir}/babel/global.dat
%{py_sitescriptdir}/babel/*.py[co]
%dir %{py_sitescriptdir}/babel/localtime
%{py_sitescriptdir}/babel/localtime/*.py[co]
%dir %{py_sitescriptdir}/babel/locale-data
%{py_sitescriptdir}/babel/locale-data/root.dat
%lang(ca_ES@valencia) %{py_sitescriptdir}/babel/locale-data/ca_ES_VALENCIA.dat
%dir %{py_sitescriptdir}/babel/messages
%{py_sitescriptdir}/babel/messages/*.py[co]
%{py_sitescriptdir}/Babel-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module} -f py3.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%attr(755,root,root) %{_bindir}/pybabel3
%dir %{py3_sitescriptdir}/babel
%{py3_sitescriptdir}/babel/__pycache__
%{py3_sitescriptdir}/babel/global.dat
%{py3_sitescriptdir}/babel/*.py
%{py3_sitescriptdir}/babel/localtime
%dir %{py3_sitescriptdir}/babel/locale-data
%{py3_sitescriptdir}/babel/locale-data/root.dat
%lang(ca_ES@valencia) %{py3_sitescriptdir}/babel/locale-data/ca_ES_VALENCIA.dat
%{py3_sitescriptdir}/babel/messages
%{py3_sitescriptdir}/Babel-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
