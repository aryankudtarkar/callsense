"""Scaffold verification tests for the local SER prototype."""

import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify the local health endpoint returns expected JSON status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok", "app": "ser-prototype"}


def test_root_serves_html():
    """Verify the CallSense landing page links to the analysis workspace."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "CallSense — Speech Emotion Review" in response.text
    assert 'id="how-it-works"' in response.text
    assert 'id="faq"' in response.text
    assert 'href="/analyze"' in response.text
    assert '<script src="/static/landing.js" defer></script>' in response.text


def test_analysis_page_serves_audio_controls_and_analysis_script():
    response = client.get("/analyze")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert 'id="analyze-btn" class="primary" aria-describedby="analyze-help">' in response.text
    assert "emotion2vec+" in response.text
    assert "audio/mpeg" in response.text
    assert '<script src="/static/app.js" defer></script>' in response.text


def test_application_script_is_served_and_csp_allows_same_origin_scripts():
    script_response = client.get("/static/app.js")
    root_response = client.get("/analyze")
    assert script_response.status_code == 200
    assert "analyzeBtn.addEventListener('click'" in script_response.text
    assert "Check the authorization box above to enable analysis." in script_response.text
    assert "script-src 'self'" in root_response.headers["content-security-policy"]


def test_landing_page_script_is_served():
    response = client.get("/static/landing.js")
    assert response.status_code == 200
    assert "IntersectionObserver" in response.text
    assert "scroll-progress" in response.text

def test_audio_route_rejects_untyped_payload():
    """Ensure audio upload route rejects untyped / unvalidated payload."""
    response = client.post("/analyze", content=b"fake audio")
    assert response.status_code == 415
