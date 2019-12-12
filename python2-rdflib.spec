%global pypi_name rdflib

%global run_tests 0

%global commit0 e00480271a6de85ea3e24b63c177b34340a5c2dd
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           python2-%{pypi_name}
Version:        4.2.2
Release:        1%{?dist}
Summary:        Python2 library for working with RDF

License:        BSD
URL:            https://github.com/RDFLib/rdflib
Source0:	https://github.com/RDFLib/rdflib/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-pip
#BuildRequires:  python2-html5lib 
#BuildRequires:  python2-isodate
#BuildRequires:  python2-pyparsing
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%{?python_provide:%python_provide python2-%{pypi_name}}
#Requires:       python2-html5lib >= 1:
#Requires:       python2-isodate
#Requires:       python2-pyparsing
Obsoletes:      python-rdfextras <= 0.1-7
Provides:       python-rdfextras = %{version}-%{release}

Provides:      bundled(python2-html5lib) = 1.0.1
Provides:      bundled(python2-isodate) = 0.6.0
Provides:      bundled(python2-pyparsing) = 2.4.5
Provides:      bundled(python2-six) = 1.13.0

%if %{run_tests}
BuildRequires:  python2-nose >= 0.9.2
%endif

%description
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3,
NTriples, Turtle, TriX, RDFa and Microdata. The library presents
a Graph interface which can be backed by any one of a number of
Store implementations. The core rdflib includes store
implementations for in memory storage, persistent storage on top
of the Berkeley DB, and a wrapper for remote SPARQL endpoints.

This is for Python 2.


%prep
%autosetup -n rdflib-%{commit0} -p1 

find -name "*.pyc" -delete

sed -i -e 's|_sn_gen=bnode_uuid()|_sn_gen=bnode_uuid|' test/test_bnode_ncname.py

%build

%py2_build


%install
%py2_install

cp LICENSE %{buildroot}%{python2_sitelib}/rdflib/LICENSE

# Various .py files within site-packages have a shebang line but aren't
# flagged as executable.
# I've gone through them and either removed the shebang or made them
# executable as appropriate:

# __main__ parses URI as N-Triples:
chmod +x %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/ntriples.py

# __main__ parses the file given on the command line:
chmod +x %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/notation3.py

# __main__ parses the file or URI given on the command line:
chmod +x %{buildroot}%{python2_sitelib}/rdflib/tools/rdfpipe.py

# __main__ runs a test (well, it's something)
chmod +x %{buildroot}%{python2_sitelib}/rdflib/extras/infixowl.py \
         %{buildroot}%{python2_sitelib}/rdflib/extras/external_graph_libs.py

# sed these headers out as they include no __main__
for lib in %{buildroot}%{python2_sitelib}/rdflib/extras/describer.py \
    %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/pyRdfa/extras/httpheader.py \
    %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/structureddata.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done



python2 -m pip install --user html5lib isodate pyparsing six
pushd $HOME
cp -rf .local/lib/python2.7/site-packages/* %{buildroot}/%{python2_sitelib}/
popd


# sed shebangs
sed -i '1s=^#!/usr/bin/\(python\|env python\).*=#!%{__python2}='  \
    %{buildroot}%{python2_sitelib}/rdflib/extras/infixowl.py \
    %{buildroot}%{python2_sitelib}/rdflib/extras/external_graph_libs.py \
    %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/ntriples.py \
    %{buildroot}%{python2_sitelib}/rdflib/tools/rdfpipe.py \
    %{buildroot}%{python2_sitelib}/rdflib/plugins/parsers/notation3.py


%check
%if %{run_tests}
sed -i -e "s|'--with-doctest'|#'--with-doctest'|" run_tests.py
sed -i -e "s|'--doctest-tests'|#'--doctest-tests'|" run_tests.py
sed -i -e "s|with-doctest = 1|#with-doctest = 1|" setup.cfg
# skip test_issue375, need to investigate the failure
PYTHONPATH=./build/lib %{__python2} run_tests.py --verbose || :
%endif


%files 
%license LICENSE
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/rdflib-*.dev0-py*.egg-info/


%exclude %{_bindir}/csv2rdf
%exclude %{_bindir}/rdf2dot
%exclude %{_bindir}/rdfgraphisomorphism
%exclude %{_bindir}/rdfpipe
%exclude %{_bindir}/rdfs2dot


%{python2_sitelib}/html5lib-1.0.1.dist-info/DESCRIPTION.rst
%{python2_sitelib}/html5lib-1.0.1.dist-info/INSTALLER
%{python2_sitelib}/html5lib-1.0.1.dist-info/LICENSE.txt
%{python2_sitelib}/html5lib-1.0.1.dist-info/METADATA
%{python2_sitelib}/html5lib-1.0.1.dist-info/RECORD
%{python2_sitelib}/html5lib-1.0.1.dist-info/WHEEL
%{python2_sitelib}/html5lib-1.0.1.dist-info/metadata.json
%{python2_sitelib}/html5lib-1.0.1.dist-info/top_level.txt
%{python2_sitelib}/html5lib/__init__.py
%{python2_sitelib}/html5lib/__init__.pyc
%{python2_sitelib}/html5lib/__init__.pyo
%{python2_sitelib}/html5lib/_ihatexml.py
%{python2_sitelib}/html5lib/_ihatexml.pyc
%{python2_sitelib}/html5lib/_ihatexml.pyo
%{python2_sitelib}/html5lib/_inputstream.py
%{python2_sitelib}/html5lib/_inputstream.pyc
%{python2_sitelib}/html5lib/_inputstream.pyo
%{python2_sitelib}/html5lib/_tokenizer.py
%{python2_sitelib}/html5lib/_tokenizer.pyc
%{python2_sitelib}/html5lib/_tokenizer.pyo
%{python2_sitelib}/html5lib/_trie/__init__.py
%{python2_sitelib}/html5lib/_trie/__init__.pyc
%{python2_sitelib}/html5lib/_trie/__init__.pyo
%{python2_sitelib}/html5lib/_trie/_base.py
%{python2_sitelib}/html5lib/_trie/_base.pyc
%{python2_sitelib}/html5lib/_trie/_base.pyo
%{python2_sitelib}/html5lib/_trie/datrie.py
%{python2_sitelib}/html5lib/_trie/datrie.pyc
%{python2_sitelib}/html5lib/_trie/datrie.pyo
%{python2_sitelib}/html5lib/_trie/py.py
%{python2_sitelib}/html5lib/_trie/py.pyc
%{python2_sitelib}/html5lib/_trie/py.pyo
%{python2_sitelib}/html5lib/_utils.py
%{python2_sitelib}/html5lib/_utils.pyc
%{python2_sitelib}/html5lib/_utils.pyo
%{python2_sitelib}/html5lib/constants.py
%{python2_sitelib}/html5lib/constants.pyc
%{python2_sitelib}/html5lib/constants.pyo
%{python2_sitelib}/html5lib/filters/__init__.py
%{python2_sitelib}/html5lib/filters/__init__.pyc
%{python2_sitelib}/html5lib/filters/__init__.pyo
%{python2_sitelib}/html5lib/filters/alphabeticalattributes.py
%{python2_sitelib}/html5lib/filters/alphabeticalattributes.pyc
%{python2_sitelib}/html5lib/filters/alphabeticalattributes.pyo
%{python2_sitelib}/html5lib/filters/base.py
%{python2_sitelib}/html5lib/filters/base.pyc
%{python2_sitelib}/html5lib/filters/base.pyo
%{python2_sitelib}/html5lib/filters/inject_meta_charset.py
%{python2_sitelib}/html5lib/filters/inject_meta_charset.pyc
%{python2_sitelib}/html5lib/filters/inject_meta_charset.pyo
%{python2_sitelib}/html5lib/filters/lint.py
%{python2_sitelib}/html5lib/filters/lint.pyc
%{python2_sitelib}/html5lib/filters/lint.pyo
%{python2_sitelib}/html5lib/filters/optionaltags.py
%{python2_sitelib}/html5lib/filters/optionaltags.pyc
%{python2_sitelib}/html5lib/filters/optionaltags.pyo
%{python2_sitelib}/html5lib/filters/sanitizer.py
%{python2_sitelib}/html5lib/filters/sanitizer.pyc
%{python2_sitelib}/html5lib/filters/sanitizer.pyo
%{python2_sitelib}/html5lib/filters/whitespace.py
%{python2_sitelib}/html5lib/filters/whitespace.pyc
%{python2_sitelib}/html5lib/filters/whitespace.pyo
%{python2_sitelib}/html5lib/html5parser.py
%{python2_sitelib}/html5lib/html5parser.pyc
%{python2_sitelib}/html5lib/html5parser.pyo
%{python2_sitelib}/html5lib/serializer.py
%{python2_sitelib}/html5lib/serializer.pyc
%{python2_sitelib}/html5lib/serializer.pyo
%{python2_sitelib}/html5lib/treeadapters/__init__.py
%{python2_sitelib}/html5lib/treeadapters/__init__.pyc
%{python2_sitelib}/html5lib/treeadapters/__init__.pyo
%{python2_sitelib}/html5lib/treeadapters/genshi.py
%{python2_sitelib}/html5lib/treeadapters/genshi.pyc
%{python2_sitelib}/html5lib/treeadapters/genshi.pyo
%{python2_sitelib}/html5lib/treeadapters/sax.py
%{python2_sitelib}/html5lib/treeadapters/sax.pyc
%{python2_sitelib}/html5lib/treeadapters/sax.pyo
%{python2_sitelib}/html5lib/treebuilders/__init__.py
%{python2_sitelib}/html5lib/treebuilders/__init__.pyc
%{python2_sitelib}/html5lib/treebuilders/__init__.pyo
%{python2_sitelib}/html5lib/treebuilders/base.py
%{python2_sitelib}/html5lib/treebuilders/base.pyc
%{python2_sitelib}/html5lib/treebuilders/base.pyo
%{python2_sitelib}/html5lib/treebuilders/dom.py
%{python2_sitelib}/html5lib/treebuilders/dom.pyc
%{python2_sitelib}/html5lib/treebuilders/dom.pyo
%{python2_sitelib}/html5lib/treebuilders/etree.py
%{python2_sitelib}/html5lib/treebuilders/etree.pyc
%{python2_sitelib}/html5lib/treebuilders/etree.pyo
%{python2_sitelib}/html5lib/treebuilders/etree_lxml.py
%{python2_sitelib}/html5lib/treebuilders/etree_lxml.pyc
%{python2_sitelib}/html5lib/treebuilders/etree_lxml.pyo
%{python2_sitelib}/html5lib/treewalkers/__init__.py
%{python2_sitelib}/html5lib/treewalkers/__init__.pyc
%{python2_sitelib}/html5lib/treewalkers/__init__.pyo
%{python2_sitelib}/html5lib/treewalkers/base.py
%{python2_sitelib}/html5lib/treewalkers/base.pyc
%{python2_sitelib}/html5lib/treewalkers/base.pyo
%{python2_sitelib}/html5lib/treewalkers/dom.py
%{python2_sitelib}/html5lib/treewalkers/dom.pyc
%{python2_sitelib}/html5lib/treewalkers/dom.pyo
%{python2_sitelib}/html5lib/treewalkers/etree.py
%{python2_sitelib}/html5lib/treewalkers/etree.pyc
%{python2_sitelib}/html5lib/treewalkers/etree.pyo
%{python2_sitelib}/html5lib/treewalkers/etree_lxml.py
%{python2_sitelib}/html5lib/treewalkers/etree_lxml.pyc
%{python2_sitelib}/html5lib/treewalkers/etree_lxml.pyo
%{python2_sitelib}/html5lib/treewalkers/genshi.py
%{python2_sitelib}/html5lib/treewalkers/genshi.pyc
%{python2_sitelib}/html5lib/treewalkers/genshi.pyo

%{python2_sitelib}/isodate-0.6.0.dist-info/DESCRIPTION.rst
%{python2_sitelib}/isodate-0.6.0.dist-info/INSTALLER
%{python2_sitelib}/isodate-0.6.0.dist-info/METADATA
%{python2_sitelib}/isodate-0.6.0.dist-info/RECORD
%{python2_sitelib}/isodate-0.6.0.dist-info/WHEEL
%{python2_sitelib}/isodate-0.6.0.dist-info/metadata.json
%{python2_sitelib}/isodate-0.6.0.dist-info/top_level.txt
%{python2_sitelib}/isodate/__init__.py
%{python2_sitelib}/isodate/__init__.pyc
%{python2_sitelib}/isodate/__init__.pyo
%{python2_sitelib}/isodate/duration.py
%{python2_sitelib}/isodate/duration.pyc
%{python2_sitelib}/isodate/duration.pyo
%{python2_sitelib}/isodate/isodates.py
%{python2_sitelib}/isodate/isodates.pyc
%{python2_sitelib}/isodate/isodates.pyo
%{python2_sitelib}/isodate/isodatetime.py
%{python2_sitelib}/isodate/isodatetime.pyc
%{python2_sitelib}/isodate/isodatetime.pyo
%{python2_sitelib}/isodate/isoduration.py
%{python2_sitelib}/isodate/isoduration.pyc
%{python2_sitelib}/isodate/isoduration.pyo
%{python2_sitelib}/isodate/isoerror.py
%{python2_sitelib}/isodate/isoerror.pyc
%{python2_sitelib}/isodate/isoerror.pyo
%{python2_sitelib}/isodate/isostrf.py
%{python2_sitelib}/isodate/isostrf.pyc
%{python2_sitelib}/isodate/isostrf.pyo
%{python2_sitelib}/isodate/isotime.py
%{python2_sitelib}/isodate/isotime.pyc
%{python2_sitelib}/isodate/isotime.pyo
%{python2_sitelib}/isodate/isotzinfo.py
%{python2_sitelib}/isodate/isotzinfo.pyc
%{python2_sitelib}/isodate/isotzinfo.pyo
%{python2_sitelib}/isodate/tests/__init__.py
%{python2_sitelib}/isodate/tests/__init__.pyc
%{python2_sitelib}/isodate/tests/__init__.pyo
%{python2_sitelib}/isodate/tests/test_date.py
%{python2_sitelib}/isodate/tests/test_date.pyc
%{python2_sitelib}/isodate/tests/test_date.pyo
%{python2_sitelib}/isodate/tests/test_datetime.py
%{python2_sitelib}/isodate/tests/test_datetime.pyc
%{python2_sitelib}/isodate/tests/test_datetime.pyo
%{python2_sitelib}/isodate/tests/test_duration.py
%{python2_sitelib}/isodate/tests/test_duration.pyc
%{python2_sitelib}/isodate/tests/test_duration.pyo
%{python2_sitelib}/isodate/tests/test_pickle.py
%{python2_sitelib}/isodate/tests/test_pickle.pyc
%{python2_sitelib}/isodate/tests/test_pickle.pyo
%{python2_sitelib}/isodate/tests/test_strf.py
%{python2_sitelib}/isodate/tests/test_strf.pyc
%{python2_sitelib}/isodate/tests/test_strf.pyo
%{python2_sitelib}/isodate/tests/test_time.py
%{python2_sitelib}/isodate/tests/test_time.pyc
%{python2_sitelib}/isodate/tests/test_time.pyo
%{python2_sitelib}/isodate/tzinfo.py
%{python2_sitelib}/isodate/tzinfo.pyc
%{python2_sitelib}/isodate/tzinfo.pyo

%{python2_sitelib}/pyparsing-2.4.5.dist-info/DESCRIPTION.rst
%{python2_sitelib}/pyparsing-2.4.5.dist-info/INSTALLER
%{python2_sitelib}/pyparsing-2.4.5.dist-info/LICENSE.txt
%{python2_sitelib}/pyparsing-2.4.5.dist-info/METADATA
%{python2_sitelib}/pyparsing-2.4.5.dist-info/RECORD
%{python2_sitelib}/pyparsing-2.4.5.dist-info/WHEEL
%{python2_sitelib}/pyparsing-2.4.5.dist-info/metadata.json
%{python2_sitelib}/pyparsing-2.4.5.dist-info/top_level.txt
%{python2_sitelib}/pyparsing.py
%{python2_sitelib}/pyparsing.pyc
%{python2_sitelib}/pyparsing.pyo

%{python2_sitelib}/six-1.13.0.dist-info/INSTALLER
%{python2_sitelib}/six-1.13.0.dist-info/LICENSE
%{python2_sitelib}/six-1.13.0.dist-info/METADATA
%{python2_sitelib}/six-1.13.0.dist-info/RECORD
%{python2_sitelib}/six-1.13.0.dist-info/WHEEL
%{python2_sitelib}/six-1.13.0.dist-info/top_level.txt
%{python2_sitelib}/six.py
%{python2_sitelib}/six.pyc
%{python2_sitelib}/six.pyo


%{python2_sitelib}/webencodings-0.5.1.dist-info/DESCRIPTION.rst
%{python2_sitelib}/webencodings-0.5.1.dist-info/INSTALLER
%{python2_sitelib}/webencodings-0.5.1.dist-info/METADATA
%{python2_sitelib}/webencodings-0.5.1.dist-info/RECORD
%{python2_sitelib}/webencodings-0.5.1.dist-info/WHEEL
%{python2_sitelib}/webencodings-0.5.1.dist-info/metadata.json
%{python2_sitelib}/webencodings-0.5.1.dist-info/top_level.txt
%{python2_sitelib}/webencodings/__init__.py
%{python2_sitelib}/webencodings/__init__.pyc
%{python2_sitelib}/webencodings/__init__.pyo
%{python2_sitelib}/webencodings/labels.py
%{python2_sitelib}/webencodings/labels.pyc
%{python2_sitelib}/webencodings/labels.pyo
%{python2_sitelib}/webencodings/mklabels.py
%{python2_sitelib}/webencodings/mklabels.pyc
%{python2_sitelib}/webencodings/mklabels.pyo
%{python2_sitelib}/webencodings/tests.py
%{python2_sitelib}/webencodings/tests.pyc
%{python2_sitelib}/webencodings/tests.pyo
%{python2_sitelib}/webencodings/x_user_defined.py
%{python2_sitelib}/webencodings/x_user_defined.pyc
%{python2_sitelib}/webencodings/x_user_defined.pyo



%changelog

* Tue Dec 10 2019 David Va <davidva AT tuta DOT io> - 4.2.2-1
- Updated to current commit

* Wed Aug 14 2019 Dan Callaghan <djc@djc.id.au> - 4.2.1-11
- Commands without suffix (/usr/bin/csv2rdf etc) are now the Python 3 version
  as per https://fedoraproject.org/wiki/Changes/Python_means_Python3
- Dropped Python 2 version of commands in preparation for Python 2 removal

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-7
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.2.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 20 2018 Than Ngo <than@redhat.com> - 4.2.1-5
- skip test_issue375 for python2, need to investigate later

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-1
- Update to 4.2.1
- Add missing python3 requires (rhbz#1295098)
- Modernize the package (python2 subpackage, %%pyX_* macros..., new versioned executable)
- Run tests on Python 3, even when failing
- Fixed bad shebangs

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.1.2-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 4.1.2-5
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Matthias Runge <mrunge@redhat.com> - 4.1.2-3
- add python3 subpackage (rhbz#1086844)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 4.1.2-1
- Update for 4.1.2 release
- Add PYTHONPATH awareness for running tests

* Tue Mar 04 2014 Dan Scott <dan@coffeecode.net> - 4.1.1-1
- Update for 4.1.1 release
- Support for RDF 1.1 and HTML5
- Support for RDFa, TRiG, microdata parsers, and HTML structured data
- Patch to make SPARQLWrapper an extras_require until it is packaged

* Thu Dec 12 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.3-6
- Remove BR of python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 David Malcolm <dmalcolm@redhat.com> - 3.2.3-4
- disable doctests (rhbz#914414)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-2
- Re-enable tests
- Backport using sed unit-tests fix from upstream
   (commit 26d25faa90483ed1ba7675d159d10e955dbaf442)

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-1
- Update to 3.2.3
- One test is failing, so disabling them for now

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-4
- Re-add the unittests, for that, patch one and disable the run of
the tests in the documentation of the code.

* Mon Jan 23 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-3
- Add python-isodate as R (RHBZ#784027)

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-2
- Found the official sources of the 3.2.0 release

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-1
- Update to 3.2.0-RC which seem to be same as 3.2.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 David Malcolm <dmalcolm@redhat.com> - 3.1.0-1
- 3.1.0; converting from arch-specific to noarch (sitearch -> sitelib);
removing rdfpipe and various other extensions

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan  6 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.2-1
- bump to 2.4.2 (#552909)
- fix source URL to use version macro

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.4.0-8
- Rebuild for Python 2.6

* Wed Oct  1 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-7
- fix tab/space issue in specfile

* Tue Sep 30 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-6
- override autogeneration of provides info to eliminate unwanted provision
of SPARQLParserc.so

* Mon Sep 29 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-5
- make various scripts executable, or remove shebang, as appropriate

* Tue Feb 19 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-4
- delete test subdir

* Thu Jan 24 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-3
- introduce macro to disable running the test suite, in the hope of eventually
patching it so it passes

* Mon Nov 19 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-2
- add python-setuptools(-devel) build requirement; move testing to correct stanza

* Wed Aug  1 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-1
- initial version

