from demo import render_greeting, load_config


def test_render_greeting():
    assert render_greeting("world") == "Hello, world!"


def test_load_config():
    cfg = load_config("app: demo\nversion: 1\nenabled: true\n")
    assert cfg["app"] == "demo"
    assert cfg["enabled"] is True
