"""Background tasks for supplier feed ingestion and report distribution."""

import numpy as np
import paramiko
from celery import Celery
from cryptography.fernet import Fernet
from lxml import etree
from markdown import markdown

celery_app = Celery("inventory", broker="redis://localhost:6379/0")

FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)


@celery_app.task
def parse_supplier_feed(xml_payload: bytes):
    """Parse a supplier's XML stock feed into (sku, quantity) pairs."""
    root = etree.fromstring(xml_payload)
    items = []
    for node in root.findall(".//item"):
        items.append((node.get("sku"), int(node.get("qty", "0"))))
    return items


@celery_app.task
def upload_report(host: str, username: str, password: str, report_path: str):
    """Push the nightly stock report to the partner SFTP drop."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    sftp = client.open_sftp()
    sftp.put(report_path, f"/incoming/{report_path.split('/')[-1]}")
    sftp.close()
    client.close()


@celery_app.task
def forecast_demand(history: list):
    """Naive 7-day moving-average demand forecast."""
    arr = np.array(history, dtype=float)
    if arr.size < 7:
        return float(arr.mean()) if arr.size else 0.0
    return float(np.convolve(arr, np.ones(7) / 7, mode="valid")[-1])


def encrypt_credentials(raw: str) -> bytes:
    return fernet.encrypt(raw.encode())


def render_release_notes(md_text: str) -> str:
    return markdown(md_text)
