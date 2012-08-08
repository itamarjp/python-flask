%global srcname Flask
%global srcversion 0.9

Name:           python-flask
Version:        0.9
Release:        3%{?dist}
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

Group:          Development/Libraries
License:        BSD
URL:            http://flask.pocoo.org/
Source0:        http://pypi.python.org/packages/source/F/Flask/%{srcname}-%{srcversion}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools-devel python-werkzeug python-sphinx
Requires:       python-werkzeug python-sphinx

%if 0%{?rhel}
BuildRequires:  python-jinja2-26
Requires:       python-jinja2-26
%else
BuildRequires:  python-jinja2
Requires:       python-jinja2
%endif



%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.



%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n %{srcname}-%{srcversion}
%{__sed} -i "1i __requires__ = ['Jinja2>=2.4']" setup.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=%{buildroot}%{python_sitelib}
%{__python} setup.py develop --install-dir %{buildroot}%{python_sitelib}
make -C docs html

rm -rf %{buildroot}%{python_sitelib}/site.py
rm -rf %{buildroot}%{python_sitelib}/site.py[co]
rm -rf %{buildroot}%{python_sitelib}/easy-install.pth
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc

%check
%{__python} setup.py test

%files
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.egg-link
%{python_sitelib}/flask

%files doc
%doc docs/_build/html examples

%changelog
* Wed Aug 8 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.0-1
- upstream 0.9
- spec cleanups

* Sun Jul  1 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.1-1
- upstream 0.8.1 (minor bugfixes)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.0-1
- upstream 0.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.7.2-2
- don't own easy-install.pth

* Fri Jul 22 2011 Steve Milner <smilner@fedoraproject.org> - 0.7.2-1
- update for upstream release

* Thu Feb 24 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-2
- fix rpmlint spelling warning
- BR python2-devel rather than python-devel
- run test suite in check

* Tue Feb 22 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-1
- Initial package
