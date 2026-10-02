"""Unit tests: validation functions in isolation."""
import pytest

from app.validation import MAX_BODY, MAX_TITLE, parse_page, validate_note


def test_valid_note_is_trimmed():
    assert validate_note({"title": "  hi "}) == ({"title": "hi", "body": ""}, None)


@pytest.mark.parametrize("data", [None, [], "x", 5])
def test_non_object_rejected(data):
    assert validate_note(data)[1] == "JSON object required"


@pytest.mark.parametrize("title", [None, "", "   ", 3, [], {}])
def test_bad_titles(title):
    assert validate_note({"title": title})[1] == "title is required"


def test_length_boundaries():
    assert validate_note({"title": "x" * MAX_TITLE})[1] is None
    assert validate_note({"title": "x" * (MAX_TITLE + 1)})[1] is not None
    assert validate_note({"title": "a", "body": "y" * MAX_BODY})[1] is None
    assert validate_note({"title": "a", "body": "y" * (MAX_BODY + 1)})[1] is not None


def test_body_must_be_string():
    assert validate_note({"title": "a", "body": 1})[1] == "body must be a string"


@pytest.mark.parametrize(
    "args,ok",
    [({}, True), ({"limit": "1"}, True), ({"limit": "100"}, True), ({"limit": "0"}, False),
     ({"limit": "101"}, False), ({"limit": "x"}, False), ({"offset": "-1"}, False),
     ({"offset": "0"}, True)],
)
def test_parse_page(args, ok):
    assert (parse_page(args)[2] is None) == ok


def test_parse_page_defaults():
    assert parse_page({}) == (20, 0, None)
