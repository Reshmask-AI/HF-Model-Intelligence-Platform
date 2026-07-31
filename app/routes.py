from flask import Blueprint, jsonify, request

from app.services.huggingface_service import get_top_models


api = Blueprint("api", __name__)


@api.route("/")
def home():
    return jsonify({
        "project": "HF Model Intelligence Platform",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "models": "/models"
        }
    })


@api.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@api.route("/models", methods=["GET"])
def models():
    limit = request.args.get("limit", default=5, type=int)

    license_filter = request.args.get("license")
    commercial_ready = request.args.get("commercial_ready", type=lambda value: value.lower() == "true")
    risk_filter = request.args.get("risk")

    print("=" * 60)
    print(f"Received limit = {limit}")
    print(f"License filter = {license_filter}")
    print(f"Commercial ready filter = {commercial_ready}")
    print(f"Risk filter = {risk_filter}")
    print("=" * 60)

    models = get_top_models(
        limit=limit,
        license_filter=license_filter,
        commercial_ready_filter=commercial_ready,
        risk_filter=risk_filter
    )

    return jsonify(models)
