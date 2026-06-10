"""Inventory Management API.

A small demo service used to test automated dependency-remediation agents.
It deliberately exercises APIs from several pinned (outdated) libraries so
that an upgrade agent has real call sites to validate against.
"""

import io
import json

import requests
import yaml
from flask import Flask, jsonify, request
from jinja2 import Template
from PIL import Image
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Base = declarative_base()
engine = create_engine("sqlite:///inventory.db")
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    sku = Column(String(64), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)


Base.metadata.create_all(engine)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/products", methods=["GET"])
def list_products():
    session = Session()
    products = session.query(Product).all()
    return jsonify(
        [{"sku": p.sku, "name": p.name, "quantity": p.quantity} for p in products]
    )


@app.route("/products", methods=["POST"])
def create_product():
    payload = request.get_json(force=True)
    session = Session()
    product = Product(
        sku=payload["sku"],
        name=payload["name"],
        quantity=payload.get("quantity", 0),
    )
    session.add(product)
    session.commit()
    return jsonify({"id": product.id}), 201


@app.route("/import-config", methods=["POST"])
def import_config():
    """Load supplier sync config from uploaded YAML."""
    config = yaml.safe_load(request.data)
    return jsonify({"loaded_keys": list(config.keys())})


@app.route("/sync-supplier", methods=["POST"])
def sync_supplier():
    """Pull stock levels from an external supplier API."""
    supplier_url = request.json.get("url")
    resp = requests.get(supplier_url, timeout=10)
    return jsonify({"status_code": resp.status_code, "bytes": len(resp.content)})


@app.route("/report", methods=["GET"])
def report():
    """Render a simple HTML stock report."""
    session = Session()
    products = session.query(Product).all()
    template = Template(
        """
        <h1>Stock Report</h1>
        <ul>
        {% for p in products %}
          <li>{{ p.sku }} — {{ p.name }}: {{ p.quantity }}</li>
        {% endfor %}
        </ul>
        """
    )
    return template.render(products=products)


@app.route("/thumbnail", methods=["POST"])
def thumbnail():
    """Generate a 128x128 thumbnail for an uploaded product image."""
    image = Image.open(io.BytesIO(request.data))
    image.thumbnail((128, 128))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue(), 200, {"Content-Type": "image/png"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
