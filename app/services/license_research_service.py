from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESEARCH_CATALOG_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "license_research_catalog.json"
)

LICENSE_RULES_FILE = (
    PROJECT_ROOT
    / "data"
    / "license_rules.json"
)

RESEARCH_RESULTS_FILE = (
    PROJECT_ROOT
    / "output"
    / "license_analysis"
    / "license_research_results.json"
)


def load_json(file_path):
    """
    Load JSON using utf-8-sig so files created by
    Windows PowerShell with a UTF-8 BOM are supported.
    """

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return None

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig"
        ) as file:
            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ) as e:

        print(
            f"Could not load "
            f"{file_path}: {e}"
        )

        return None


def normalize_license_name(license_name):
    """
    Normalize license names for comparison.
    """

    if not license_name:
        return None

    return (
        license_name
        .lower()
        .strip()
        .replace("_", "-")
    )


def research_license(
    license_name,
    model_count,
    license_rules
):
    """
    Determine the current research status
    of a license.
    """

    if license_name is None:

        return {
            "license": None,
            "model_count": model_count,
            "status": "pending_model_investigation",
            "reason": (
                "No license name was discovered "
                "from Hugging Face metadata."
            ),
            "verified": False
        }

    normalized_name = (
        normalize_license_name(
            license_name
        )
    )

    normalized_rules = {
        normalize_license_name(
            key
        ): value
        for key, value in license_rules.items()
    }

    if normalized_name in normalized_rules:

        return {
            "license": license_name,
            "model_count": model_count,
            "status": "already_analyzed",
            "reason": (
                "License already exists "
                "in license_rules.json."
            ),
            "verified": True,
            "license_intelligence": (
                normalized_rules[
                    normalized_name
                ]
            )
        }

    return {
        "license": license_name,
        "model_count": model_count,
        "status": "requires_research",
        "reason": (
            "License identity discovered, "
            "but no verified license rule "
            "exists yet."
        ),
        "verified": False
    }


def run_license_research():

    catalog = load_json(
        RESEARCH_CATALOG_FILE
    )

    license_rules = load_json(
        LICENSE_RULES_FILE
    )

    if catalog is None:
        return []

    if license_rules is None:
        return []

    results = []

    print("=" * 60)
    print("LICENSE RESEARCH SERVICE")
    print("=" * 60)

    for index, item in enumerate(
        catalog,
        start=1
    ):

        license_name = item.get(
            "license"
        )

        model_count = item.get(
            "model_count",
            0
        )

        print(
            f"Checking "
            f"{index}/{len(catalog)}: "
            f"{license_name}"
        )

        result = research_license(
            license_name,
            model_count,
            license_rules
        )

        results.append(result)

    output_dir = (
        RESEARCH_RESULTS_FILE.parent
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RESEARCH_RESULTS_FILE,
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
        f"Saved {len(results)} research results to:"
    )

    print(
        RESEARCH_RESULTS_FILE
    )

    return results


if __name__ == "__main__":

    results = run_license_research()

    print()
    print("=" * 60)
    print("LICENSE RESEARCH SUMMARY")
    print("=" * 60)

    already_analyzed = 0
    requires_research = 0
    model_investigation = 0

    for result in results:

        status = result.get(
            "status"
        )

        if status == "already_analyzed":
            already_analyzed += 1

        elif status == "requires_research":
            requires_research += 1

        elif status == (
            "pending_model_investigation"
        ):
            model_investigation += 1

    print(
        f"Total research items: "
        f"{len(results)}"
    )

    print(
        f"Already analyzed: "
        f"{already_analyzed}"
    )

    print(
        f"Requires research: "
        f"{requires_research}"
    )

    print(
        f"Model investigation needed: "
        f"{model_investigation}"
    )