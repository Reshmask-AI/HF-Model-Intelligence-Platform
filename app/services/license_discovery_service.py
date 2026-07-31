from pathlib import Path
import json

from huggingface_hub import model_info


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PENDING_LICENSES_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "normalized_pending_licenses.json"
)

DISCOVERY_RESULTS_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "license_discovery_results.json"
)


def load_pending_licenses():
    """
    Load normalized pending license records.
    """

    if not PENDING_LICENSES_FILE.exists():
        print(
            f"File not found: "
            f"{PENDING_LICENSES_FILE}"
        )
        return []

    try:
        with open(
            PENDING_LICENSES_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        print(
            f"Could not load pending licenses: {e}"
        )
        return []


def discover_license(model_id):
    """
    Fetch license information directly from
    Hugging Face model metadata.
    """

    try:
        details = model_info(model_id)

        card_data = details.cardData or {}
        tags = getattr(
            details,
            "tags",
            []
        ) or []

        license_value = card_data.get(
            "license"
        )

        license_name = card_data.get(
            "license_name"
        )

        return {
            "model_id": model_id,
            "license": license_value,
            "license_name": license_name,
            "tags": tags,
            "status": "discovered"
        }

    except Exception as e:

        print(
            f"Error discovering license for "
            f"{model_id}: {e}"
        )

        return {
            "model_id": model_id,
            "license": None,
            "license_name": None,
            "tags": [],
            "status": "error",
            "error": str(e)
        }


def discover_other_licenses():

    pending_licenses = (
        load_pending_licenses()
    )

    # Only process records currently marked
    # as "other".
    other_models = [
        item
        for item in pending_licenses
        if item.get("license") == "other"
    ]

    print(
        f"Total normalized pending records: "
        f"{len(pending_licenses)}"
    )

    print(
        f"Models with license='other': "
        f"{len(other_models)}"
    )

    results = []

    for index, item in enumerate(
        other_models,
        start=1
    ):

        model_id = item.get(
            "model_id"
        )

        print(
            f"Checking {index}/"
            f"{len(other_models)}: "
            f"{model_id}"
        )

        result = discover_license(
            model_id
        )

        results.append(result)

    OUTPUT_DIR = (
        DISCOVERY_RESULTS_FILE.parent
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        DISCOVERY_RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(
        f"Saved {len(results)} discovery results to:"
    )

    print(
        DISCOVERY_RESULTS_FILE
    )

    return results


if __name__ == "__main__":

    print("=" * 60)
    print("LICENSE DISCOVERY")
    print("=" * 60)

    results = discover_other_licenses()

    print()
    print("=" * 60)
    print("DISCOVERY SUMMARY")
    print("=" * 60)

    discovered = 0
    missing = 0
    errors = 0

    for item in results:

        license_name = item.get(
            "license_name"
        )

        status = item.get(
            "status"
        )

        if status == "error":
            errors += 1

        elif license_name:
            discovered += 1

        else:
            missing += 1

    print(
        f"Total checked: {len(results)}"
    )

    print(
        f"Specific license_name found: "
        f"{discovered}"
    )

    print(
        f"No license_name found: "
        f"{missing}"
    )

    print(
        f"Errors: {errors}"
    )

    print()
    print(
        "DISCOVERED LICENSES"
    )

    print(
        "-" * 60
    )

    for item in results:

        print(
            f"MODEL: {item.get('model_id')}"
        )

        print(
            f"LICENSE: {item.get('license')}"
        )

        print(
            f"LICENSE_NAME: "
            f"{item.get('license_name')}"
        )

        print(
            "-" * 60
        )