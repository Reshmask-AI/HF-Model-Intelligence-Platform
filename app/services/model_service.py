from huggingface_hub import model_info


def get_model_details(model_id):
    """
    Fetch detailed information about a Hugging Face model.

    Parameters
    ----------
    model_id : str
        Hugging Face model ID.

    Returns
    -------
    dict
        Normalized model metadata.
    """

    try:
        details = model_info(model_id)

        card_data = details.cardData or {}
        tags = getattr(details, "tags", []) or []

        # Get the primary license value.
        license_name = card_data.get("license")

        # Hugging Face sometimes reports:
        # license: other
        # license_name: kimi-k3
        #
        # Use the specific license_name when available.
        if license_name == "other":
            specific_license_name = card_data.get("license_name")

            if specific_license_name:
                license_name = specific_license_name

        return {
            "id": details.id,
            "author": getattr(details, "author", None),
            "downloads": getattr(details, "downloads", 0),
            "likes": getattr(details, "likes", 0),
            "pipeline_tag": getattr(details, "pipeline_tag", None),
            "license": license_name,
            "tags": tags,
            "created_at": str(getattr(details, "created_at", None)),
            "last_modified": str(getattr(details, "last_modified", None)),
        }

    except Exception as e:
        print(
            f"Error fetching model details for "
            f"'{model_id}': {e}"
        )

        return {
            "id": model_id,
            "author": None,
            "downloads": 0,
            "likes": 0,
            "pipeline_tag": None,
            "license": None,
            "tags": [],
            "created_at": None,
            "last_modified": None,
        }
