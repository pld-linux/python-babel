%define		fname	Babel
Summary:	Babel Python library
Summary(pl.UTF-8):	Biblioteka Babel do Pythona
Name:		python-%{fname}
Version:	0.9.5
Release:	0.1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	ftp://ftp.edgewall.com/pub/babel/%{fname}-%{version}.tar.gz
# Source0-md5:	05603f058644f81b9b5f75d0161a14dd
URL:		http://babel.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
#%pyrequires_eq	python-libs
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications.)

%prep
%setup -q -n %{fname}-%{version}

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.txt doc
%attr(755,root,root) %{_bindir}/pybabel
%{py_sitescriptdir}/babel
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{fname}-%{version}-py*.egg-info
%endif
