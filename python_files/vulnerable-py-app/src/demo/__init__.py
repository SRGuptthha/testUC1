"""Sample app exercising several outdated/vulnerable dependencies.

Used to test a dependency remediation agent. Do not deploy.
"""
import yaml
import requests
from jinja2 import Template


def render_greeting(name: str) -> str:
    """jinja2 2.11.2 usage."""
    template = Template("Hello, {{ name }}!")
    return template.render(name=name)


def load_config(raw: str) -> dict:
    """PyYAML 5.3.1 usage (safe_load to avoid actual RCE in the sample)."""
    return yaml.safe_load(raw)


def fetch_status(url: str) -> int:
    """requests 2.25.0 / urllib3 1.26.5 usage."""
    resp = requests.get(url, timeout=10)
    return resp.status_code


def main() -> None:
    print(render_greeting("world"))
    cfg = load_config("app: demo\nversion: 1\nenabled: true\n")
    print("Loaded config:", cfg)


if __name__ == "__main__":
    main()
