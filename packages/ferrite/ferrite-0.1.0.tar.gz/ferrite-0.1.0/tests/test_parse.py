import pytest
from ferrite import parse as rustparse
from xmltodict import parse as pyparse

pytestmark = pytest.mark.parametrize("parse", [pyparse, rustparse])


def test_empty(parse):
    xml = "<a/>"
    target = {"a": None}
    assert parse(xml) == target


def test_empty_with_attributes(parse):
    xml = '<e name="value" />'
    target = {"e": {"@name": "value"}}
    assert parse(xml) == target


def test_text(parse):
    xml = "<a>text</a>"
    target = {"a": "text"}
    assert parse(xml) == target


def test_text_whitespace(parse):
    xml = "<a>  text  </a>"
    target = {"a": "text"}
    assert parse(xml) == target


def test_text_line_breaks(parse):
    xml = "<a>\ntext\n</a>"
    target = {"a": "text"}
    assert parse(xml) == target


def test_text_and_attributes(parse):
    xml = '<e name="value">text</e>'
    target = {"e": {"@name": "value", "#text": "text"}}
    assert parse(xml) == target


def test_with_children(parse):
    xml = "<e><a>1</a><b>2</b></e>"
    target = {"e": {"a": "1", "b": "2"}}
    assert parse(xml) == target


def test_identically_named_children(parse):
    xml = "<e><a>1</a><a>2</a></e>"
    target = {"e": {"a": ["1", "2"]}}
    assert parse(xml) == target


def test_more_identically_named_children(parse):
    xml = "<e><a>1</a><a>2</a><a>3</a></e>"
    target = {"e": {"a": ["1", "2", "3"]}}
    assert parse(xml) == target


def test_mixed_type_identically_named_children(parse):
    # xml = """
    #     <e>
    #         <a/>
    #         <a attr="attr-1" />
    #         <a>2</a>
    #         <a attr="attr-3">3</a>
    #     </e>
    # """
    xml = "<e><a/><a attr='attr-1' /><a>2</a><a attr='attr-3'>3</a></e>"
    target = {"e": {"a": [None, {"@attr": "attr-1"}, "2", {"@attr": "attr-3", "#text": "3"}]}}
    assert parse(xml) == target


def test_elements_and_text(parse):
    xml = "<e>1<a>2</a></e>"
    target = {"e": {"#text": "1", "a": "2"}}
    assert parse(xml) == target
