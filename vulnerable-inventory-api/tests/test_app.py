"""Smoke tests — give your remediation agent a validation gate to run
after upgrading dependencies (e.g. `pytest -q`)."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app  # noqa: E402
from app.tasks import forecast_demand, render_release_notes  # noqa: E402


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200


def test_create_and_list_product():
    client = app.test_client()
    resp = client.post(
        "/products",
        json={"sku": "TEST-001", "name": "Test Widget", "quantity": 5},
    )
    assert resp.status_code == 201
    resp = client.get("/products")
    assert resp.status_code == 200
    skus = [p["sku"] for p in resp.get_json()]
    assert "TEST-001" in skus


def test_forecast_demand():
    assert forecast_demand([10] * 14) == 10.0
    assert forecast_demand([]) == 0.0


def test_render_release_notes():
    html = render_release_notes("# Release 1.0")
    assert "<h1>" in html
