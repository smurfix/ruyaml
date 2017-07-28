# coding: utf-8

import pytest   # NOQA

from ruamel import yaml
from roundtrip import round_trip


class XXX(yaml.comments.CommentedMap):
    @staticmethod
    def yaml_dump(dumper, data):
        return dumper.represent_mapping(u'!xxx', data)

    @classmethod
    def yaml_load(cls, constructor, node):
        data = cls()
        yield data
        constructor.construct_mapping(node, data)


yaml.add_constructor(u'!xxx', XXX.yaml_load, constructor=yaml.RoundTripConstructor)
yaml.add_representer(XXX, XXX.yaml_dump, representer=yaml.RoundTripRepresenter)


class TestIndentFailures:

    def test_tag(self):
        round_trip("""\
        !!python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_full_tag(self):
        round_trip("""\
        !!tag:yaml.org,2002:python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_standard_tag(self):
        round_trip("""\
        !!tag:yaml.org,2002:python/object:map
        name: Anthon
        location: Germany
        language: python
        """)

    def test_Y1(self):
        round_trip("""\
        !yyy
        name: Anthon
        location: Germany
        language: python
        """)

    def test_Y2(self):
        round_trip("""\
        !!yyy
        name: Anthon
        location: Germany
        language: python
        """)


class TestRoundTripCustom:
    def test_X1(self):
        round_trip("""\
        !xxx
        name: Anthon
        location: Germany
        language: python
        """)

    @pytest.mark.xfail(strict=True)
    def test_X_pre_tag_comment(self):
        round_trip("""\
        -
          # hello
          !xxx
          name: Anthon
          location: Germany
          language: python
        """)

    @pytest.mark.xfail(strict=True)
    def test_X_post_tag_comment(self):
        round_trip("""\
        - !xxx
          # hello
          name: Anthon
          location: Germany
          language: python
        """)
