"""Tests for helpers.py."""

import ckanext.mtcui.helpers as helpers


def test_mtcui_hello():
    assert helpers.mtcui_hello() == "Hello, mtcui!"
