# TODO
# - lang tag /usr/share/python*/site-packages/babel/localedata/*
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define		pkgname	babel
Summary:	Babel Python library
Summary(pl.UTF-8):	Biblioteka Babel do Pythona
Name:		python-%{pkgname}
Version:	0.9.5
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	ftp://ftp.edgewall.com/pub/babel/Babel-%{version}.tar.gz
# Source0-md5:	05603f058644f81b9b5f75d0161a14dd
URL:		http://babel.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%pyrequires_eq	python-modules
Obsoletes:	python-Babel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

%package apidocs
Summary:	Python Babel API documentation
Group:		Documentation

%description apidocs
Python Babel API documentation.

%prep
%setup -q -n Babel-%{version}

mv doc/api apidoc

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.txt doc/*
%attr(755,root,root) %{_bindir}/pybabel
%{py_sitescriptdir}/babel
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/*.egg-info
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidoc/*
%endif
