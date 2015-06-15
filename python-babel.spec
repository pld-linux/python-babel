# TODO
# - lang tag /usr/share/python*/site-packages/babel/localedata/*
#
# Conditional build:
%bcond_without  doc             # don't build doc
%bcond_without  tests   # do not perform "make test"
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module


%define	        module 	babel
Summary:	Babel Python library
Summary(pl.UTF-8):	Biblioteka Babel do Pythona
Name:		python-%{module}
Version:	1.3
Release:	3
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/B/Babel/Babel-%{version}.tar.gz
# Source0-md5:	5264ceb02717843cbc9ffce8e6e06bdb
URL:		http://babel.pocoo.org/
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-devel-tools
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-modules
%endif

Requires:	python-modules
Obsoletes:	python-Babel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

# %description -l pl.UTF-8

%package -n python3-%{module}
Summary:	Babel Python library
Summary(pl.UTF-8):	Biblioteka Babel do Pythona
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

# %description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	Python Babel API documentation
Group:		Documentation

%description apidocs
Python Babel API documentation.

%prep
%setup -q -n Babel-%{version}

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
        build --build-base build-2 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
        build --build-base build-3 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE README
%attr(755,root,root) %{_bindir}/pybabel
%dir %{py_sitescriptdir}/babel
%{py_sitescriptdir}/babel/*.dat
%{py_sitescriptdir}/babel/*.py[co]
%dir %{py_sitescriptdir}/babel/localtime
%{py_sitescriptdir}/babel/localtime/*.py[co]

%dir %{py_sitescriptdir}/babel/localedata
# TODO: %lang tag
%{py_sitescriptdir}/babel/localedata/*.dat
%dir %{py_sitescriptdir}/babel/messages
%{py_sitescriptdir}/babel/messages/*.py[co]

%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Babel-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/Babel-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

