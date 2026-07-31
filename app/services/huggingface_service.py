from pathlib import Path
import json

from huggingface_hub import list_models

from app.services.model_service import get_model_details
from app.services.license_service import get_license_intelligence
from app.services.license_queue_service import save_pending_license


def get_top_models(
    limit=10,
    license_filter=None,
    commercial_ready_filter=None,
    risk_filter=None
):
    models = list(list_models(limit=limit))

    results = []

    for model in models:
        model_data = get_model_details(model.id)

        license_name = model_data.get("license")

        license_info = get_license_intelligence(license_name)

        if license_info is None and license_name is not None:
            save_pending_license(
                model_id=model.id,
                license_name=license_name,
                reason="license_requires_analysis"
            )

        model_data["license_intelligence"] = license_info

        if license_filter is not None:
            if license_name is None:
                continue

            if license_name.lower() != license_filter.lower():
                continue

        if commercial_ready_filter is not None:
            if license_info is None:
                continue

            if license_info.get("commercial_ready") != commercial_ready_filter:
                continue

        if risk_filter is not None:
            if license_info is None:
                continue

            model_risk = license_info.get("risk")

            if model_risk is None:
                continue

            if model_risk.lower() != risk_filter.lower():
                continue

        results.append(model_data)

    output_dir = Path("output/huggingface")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "models.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved {len(results)} models to {output_file}"
    )

    return results
