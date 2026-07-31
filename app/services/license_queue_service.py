from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output" / "license_analysis"

PENDING_LICENSES_FILE = OUTPUT_DIR / "pending_licenses.json"


def save_pending_license(
    model_id,
    license_name,
    reason="requires_manual_analysis"
):
    """
    Save a model with an unknown, other, or unrecognized license
    for later license analysis.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pending_licenses = []

    # Load existing pending licenses
    if PENDING_LICENSES_FILE.exists():

        try:
            with open(
                PENDING_LICENSES_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                pending_licenses = json.load(file)

        except (json.JSONDecodeError, OSError):
            pending_licenses = []

    # Avoid duplicate model/license entries
    for item in pending_licenses:
        if (
            item.get("model_id") == model_id
            and item.get("license") == license_name
        ):
            return

    # Add new pending license
    pending_licenses.append({
        "model_id": model_id,
        "license": license_name,
        "status": "pending",
        "reason": reason
    })

    # Save file
    with open(
        PENDING_LICENSES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            pending_licenses,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Pending license saved: "
        f"{model_id} -> {license_name}"
    )


def get_pending_licenses():
    """
    Return all licenses waiting for analysis.
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

    except (json.JSONDecodeError, OSError):
        return []