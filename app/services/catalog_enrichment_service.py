from pathlib import Path
import json

from app.services.model_service import get_model_details
from app.services.license_service import get_license_intelligence
from app.services.license_queue_service import save_pending_license


def enrich_model(model_id):
    """
    Fetch detailed model metadata and license intelligence
    for a single Hugging Face model.
    """

    model_data = get_model_details(model_id)

    license_name = model_data.get("license")

    license_info = get_license_intelligence(
        license_name
    )

    if (
        license_info is None
        and license_name is not None
    ):
        save_pending_license(
            model_id=model_id,
            license_name=license_name,
            reason="license_requires_analysis"
        )

    model_data["license_intelligence"] = license_info

    return model_data


def enrich_model_batch(
    models,
    output_file
):
    """
    Enrich a batch of Hugging Face models
    and save the results to a JSON file.
    """

    enriched_models = []

    for index, model in enumerate(
        models,
        start=1
    ):

        print(
            f"Enriching model "
            f"{index}/{len(models)}: "
            f"{model.id}"
        )

        enriched_model = enrich_model(
            model.id
        )

        enriched_models.append(
            enriched_model
        )

    output_path = Path(
        output_file
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            enriched_models,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved {len(enriched_models)} "
        f"enriched models to "
        f"{output_path}"
    )

    return enriched_models