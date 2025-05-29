"""Tests for views.py."""

import pytest
import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "mtcui")
@pytest.mark.usefixtures("with_plugins")
def test_mtcui_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("mtcui.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, mtcui!"
