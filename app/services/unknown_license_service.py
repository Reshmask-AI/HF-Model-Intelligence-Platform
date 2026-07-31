from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PENDING_LICENSES_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "pending_licenses.json"
)


def load_pending_licenses():
    """
    Load licenses that are waiting for analysis.
    """

    if not PENDING_LICENSES_FILE.exists():
        return []

    try:
        with open(
            PENDING_LICENSES_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        print(f"Could not load pending licenses: {e}")
        return []


def analyze_pending_licenses():
    """
    Analyze pending licenses and classify them
    for the next stage of license research.
    """

    pending_licenses = load_pending_licenses()

    results = []

    for item in pending_licenses:

        model_id = item.get("model_id")
        license_name = item.get("license")

        if license_name is None:
            category = "missing_license"

        elif license_name.lower() == "other":
            category = "custom_or_unspecified_license"

        else:
            category = "specific_license_requires_research"

        results.append({
            "model_id": model_id,
            "license": license_name,
            "status": "pending_analysis",
            "category": category
        })

    return results


if __name__ == "__main__":

    results = analyze_pending_licenses()

    print("=" * 60)
    print("UNKNOWN LICENSE ANALYSIS")
    print("=" * 60)

    for item in results:
        print(
            f"Model: {item['model_id']}"
        )
        print(
            f"License: {item['license']}"
        )
        print(
            f"Category: {item['category']}"
        )
        print("-" * 60)