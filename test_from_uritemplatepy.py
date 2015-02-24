# these tests are derived from the uritemplate-py project
# https://raw.github.com/uri-templates/uritemplate-py/master/test/uritemplate_test.py
# modified to run correctly here
#
# Copyright 2011-2012 The Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
from unittest import TestCase, main

from uritemplate import URITemplate, expand


class TestJSONFromUritemplatePy(TestCase):
    # test methods based on JSON data are attached to this class at
    # import time
    pass


nopunc = re.compile(r'[\W_]', re.MULTILINE)


def python_safe_name(s):
    """
    Return a name safe to use for a python function from string s.
    """
    s = s.strip()
    s = s.lower()
    s = re.sub(nopunc, ' ', s)
    s = s.strip()
    s = '_'.join(s.split())
    return str(s)


def make_test(test_name, template, variables, expected):
    def json_test_function(self):
        actual = unicode(expand(template, variables))
        msg = '%(template)r did not expand as expected, got %(actual)r.'\
                % locals()
        if type(expected) == type([]):
            self.assertTrue (actual in expected, msg)
        else:
            self.assertEqual(expected, actual)
    json_test_function.__name__ = test_name
    json_test_function.funcname = test_name
    return json_test_function


def build_tests_from_json(data_set, test_class=TestJSONFromUritemplatePy):
    """
    Build test methods from data_set and attach these to test_class.
    """
    with open(data_set) as fin:
        testdata = json.load(fin)

    # loop through all suite/cases and attach a test method to our test class
    for test_name, suite in testdata.items():
        variables = suite['variables']
        testcases = suite['testcases']
        for i, testcase in enumerate(testcases):
            # build a nice test method name
            fun_name = 'test_from_uritemplatepy %(test_name)s %(i)d' % locals()
            safe_name = python_safe_name(fun_name)
            template = testcase[0]
            expected = testcase[1]
            # closure on the test params
            test_method = make_test(safe_name , template, variables, expected)
            # attach that method to the class
            setattr(test_class, safe_name, test_method)


for jds in os.listdir('testfiles'):
    if not jds.endswith('.json'):
        continue
    pth = os.path.join('testfiles', jds)
    build_tests_from_json(pth)


#############################
# these tests are from the uritemplate-py project
# https://raw.github.com/uri-templates/uritemplate-py/master/test/variables_test.py
# modified to run correctly here
#
# Copyright 2011-2012 The Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class TestVariablesFromUritemplatePy(TestCase):

    def get_vars(self, template):
        for vr in URITemplate(template).variables:
            for n in vr.variable_names:
                yield n

    def test_simple(self):
        template = 'http://example.com/{x,y}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y']), vrs)

    def test_simple2(self):
        template = 'http://example.com/{x,y}/{z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_reserved(self):
        template = 'http://example.com/{+x,y}/{+z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_fragment(self):
        template = 'http://example.com/{#x,y},{#z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_label(self):
        template = 'http://{.x,y,z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_path_segment(self):
        template = 'http://example.com{/x,y}/w{/z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_parameter(self):
        template = 'http://example.com{;x,y}{;z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_query(self):
        template = 'http://example.com{?x,y,z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_query_continuation(self):
        template = 'http://example.com?a=1&b=2{&x,y}&r=13{&z}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_prefix_modifier(self):
        template = 'http://example.com{/x:5,y:7}{/z:2}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_explode_modifier(self):
        template = 'http://example.com{/x*,y*}/page{/z*}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['x', 'y', 'z']), vrs)

    def test_mixed_expansion_types(self):
        template = 'http://{a,b}.com{;c,d}{/e,f}/page{?g,h}{&i,j}{#k,l}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set('abcdefghijkl'), vrs)

    def test_overlapping_expansion(self):
        template = 'http://{a,b}.com{;a,b}{/a,b}/page{?a,b}{&a,b}{#a,b}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['a', 'b']), vrs)

    def test_partially_overlapping(self):
        template = 'http://{.a,b}{/b,c}/{c,d}'
        vrs = set(self.get_vars(template))
        self.assertEquals(set(['a', 'b', 'c', 'd']), vrs)



if __name__ == '__main__':
    main()
