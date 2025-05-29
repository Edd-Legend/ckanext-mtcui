"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.mtcui.logic import validators


def test_mtcui_reauired_with_valid_value():
    assert validators.mtcui_required("value") == "value"


def test_mtcui_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.mtcui_required(None)
