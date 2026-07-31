from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PENDING_LICENSES_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "pending_licenses.json"
)

NORMALIZED_LICENSES_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "normalized_pending_licenses.json"
)


# Known aliases that can be normalized automatically.
LICENSE_ALIASES = {
    "openmdw1.1-license": "openmdw-1.1",
    "openmdw-1.1": "openmdw-1.1",

    "kimi-k3": "kimi-k3",

    "upstage-solar-license": "upstage-solar-license",

    "researchrail": "researchrail",

    "lfm1.0": "lfm1.0",

    "modified-mit": "modified-mit",

    "qwen": "qwen",

    "krea-2-community-license": (
        "krea-2-community-license"
    ),

    "nvidia-open-model-license": (
        "nvidia-open-model-license"
    ),

    "nyra-health-non-commercial-research": (
        "nyra-health-non-commercial-research"
    ),

    "fish-audio-research-license": (
        "fish-audio-research-license"
    ),

    "ltx-2": "ltx-2",

    "flux-1-dev-non-commercial-license": (
        "flux-1-dev-non-commercial-license"
    ),

    "ltx-2-community-license-agreement": (
        "ltx-2-community-license-agreement"
    ),

    "circlestone-labs-non-commercial-license": (
        "circlestone-labs-non-commercial-license"
    ),

    "nvidia-license": "nvidia-license",

    "cc-by-nc-4.0": "cc-by-nc-4.0",

    "gemma": "gemma",
}


def load_pending_licenses():
    """
    Load pending license records.
    """

    if not PENDING_LICENSES_FILE.exists():
        print(
            f"Pending license file not found: "
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


def normalize_license_name(license_name):
    """
    Normalize a license identifier.
    """

    if license_name is None:
        return None

    if not isinstance(license_name, str):
        return None

    normalized = license_name.strip().lower()

    if not normalized:
        return None

    return LICENSE_ALIASES.get(
        normalized,
        normalized
    )


def normalize_pending_licenses():
    """
    Normalize pending license records.

    The same model may appear multiple times because
    the enrichment process was executed more than once.

    We keep one record per unique
    model_id + normalized license combination.
    """

    pending_licenses = load_pending_licenses()

    normalized_records = []
    seen = set()

    for item in pending_licenses:

        model_id = item.get("model_id")
        original_license = item.get("license")

        normalized_license = normalize_license_name(
            original_license
        )

        key = (
            model_id,
            normalized_license
        )

        if key in seen:
            continue

        seen.add(key)

        normalized_records.append({
            "model_id": model_id,
            "license": normalized_license,
            "original_license": original_license,
            "status": "pending",
            "reason": item.get(
                "reason",
                "requires_manual_analysis"
            )
        })

    OUTPUT_DIR = NORMALIZED_LICENSES_FILE.parent
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        NORMALIZED_LICENSES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            normalized_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Original pending records: "
        f"{len(pending_licenses)}"
    )

    print(
        f"Normalized unique records: "
        f"{len(normalized_records)}"
    )

    print(
        f"Removed duplicate records: "
        f"{len(pending_licenses) - len(normalized_records)}"
    )

    print(
        f"Saved normalized licenses to: "
        f"{NORMALIZED_LICENSES_FILE}"
    )

    return normalized_records


if __name__ == "__main__":

    print("=" * 60)
    print("LICENSE NORMALIZATION")
    print("=" * 60)

    results = normalize_pending_licenses()

    print()
    print("NORMALIZED LICENSE SUMMARY")
    print("-" * 60)

    license_counts = {}

    for item in results:

        license_name = item.get(
            "license"
        )

        license_counts[license_name] = (
            license_counts.get(
                license_name,
                0
            ) + 1
        )

    for license_name, count in sorted(
        license_counts.items()
    ):

        print(
            f"{license_name} -> "
            f"{count} model(s)"
        )