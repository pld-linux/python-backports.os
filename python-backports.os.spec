#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (not needed for 3.5+)

Summary:	Backport of new features in Python's os module
Summary(pl.UTF-8):	Backport nowych funkcji z modułu Pythona os
Name:		python-backports.os
Version:	0.1.1
Release:	2
License:	PSF v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/backports-os/
Source0:	https://files.pythonhosted.org/packages/source/b/backports.os/backports.os-%{version}.tar.gz
# Source0-md5:	39286340acee2f2999b6da13c89bdd67
URL:		https://pypi.org/project/backports.os/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-future
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%endif
Requires:	python-backports
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides backports of new features in Python's os module
under the backports namespace.

%description -l pl.UTF-8
Ten pakiet zawiera backport nowych funkcji z modułu Pythona os
umieszczony w przestrzeni nazw backports.

%package -n python3-backports.os
Summary:	Backport of new features in Python's os module
Summary(pl.UTF-8):	Backport nowych funkcji z modułu Pythona os
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-backports.os
This package provides backports of new features in Python's os module
under the backports namespace.

%description -n python3-backports.os -l pl.UTF-8
Ten pakiet zawiera backport nowych funkcji z modułu Pythona os
umieszczony w przestrzeni nazw backports.

%prep
%setup -q -n backports.os-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-2/lib \
%{__python} -m unittest discover -s tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m unittest discover -s tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
# packaged in python-backports package
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/backports/__init__.py*
%endif

%if %{with python3}
%py3_install

# not needed for python3 (PEP-420)?
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/backports/{__init__.py,__pycache__/__init__.*}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/backports/os.py[co]
%{py_sitescriptdir}/backports.os-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-backports.os
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/backports/os.py
%{py3_sitescriptdir}/backports/__pycache__/os.cpython-*.py[co]
%{py3_sitescriptdir}/backports.os-%{version}-py*.egg-info
%endif
