import json
from pathlib import Path


# Project root:
# DevOps-Project/
# ├── app/
# │   └── services/
# │       └── license_service.py
# └── data/
#     └── license_rules.json

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LICENSE_RULES_FILE = PROJECT_ROOT / "data" / "license_rules.json"


def load_license_rules():
    """
    Load license rules from the project's JSON configuration file.
    """

    if not LICENSE_RULES_FILE.exists():
        print(f"License rules file not found: {LICENSE_RULES_FILE}")
        return {}

    try:
        with open(LICENSE_RULES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in license rules file: {e}")
        return {}

    except Exception as e:
        print(f"Could not load license rules: {e}")
        return {}


def normalize_license_name(license_name):
    """
    Normalize a license name for consistent lookup.
    """

    if license_name is None:
        return None

    if not isinstance(license_name, str):
        return None

    normalized = license_name.strip().lower()

    if not normalized:
        return None

    return normalized


def get_license_intelligence(license_name):
    """
    Analyze a license using the project's license rules.

    Rules:
    - None / missing license -> ignored
    - other -> requires manual analysis
    - unknown -> requires manual analysis
    - recognized license -> return license intelligence
    """

    normalized_license = normalize_license_name(license_name)

    # Case 1: No license provided
    if normalized_license is None:
        return None

    # Case 2: License is explicitly marked as "other"
    if normalized_license == "other":
        return None

    # Case 3: License is explicitly marked as "unknown"
    if normalized_license == "unknown":
        return None

    # Load known license rules
    license_rules = load_license_rules()

    # Try direct lookup
    rule = license_rules.get(normalized_license)

    # Try SPDX-style variations
    if rule is None:

        aliases = {
            "apache license 2.0": "apache-2.0",
            "apache license, version 2.0": "apache-2.0",
            "apache 2.0": "apache-2.0",
            "mit license": "mit",
            "bsd 2-clause": "bsd-2-clause",
            "bsd 3-clause": "bsd-3-clause",
        }

        alias = aliases.get(normalized_license)

        if alias:
            rule = license_rules.get(alias)

    # Case 4: License is not in our rules
    if rule is None:
        return None

    # Build intelligence result
    return {
        "license_name": rule.get("license_name"),
        "license_type": rule.get("license_type"),
        "commercial_use": rule.get("commercial_use"),
        "research_use": rule.get("research_use"),
        "private_use": rule.get("private_use"),
        "modification": rule.get("modification"),
        "redistribution": rule.get("redistribution"),
        "patent_grant": rule.get("patent_grant"),
        "attribution_required": rule.get("attribution_required"),
        "share_alike": rule.get("share_alike"),
        "copyleft": rule.get("copyleft"),
        "commercial_ready": rule.get("commercial_ready"),
        "risk": rule.get("risk"),
        "license_quality": rule.get("license_quality"),
        "open_score": rule.get("open_score"),
    }