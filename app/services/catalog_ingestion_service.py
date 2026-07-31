from pathlib import Path
import json

from huggingface_hub import list_models


def fetch_model_batch(limit=1000):
    models = list(list_models(limit=limit))

    print(f"Fetched {len(models)} models")

    return models


def save_model_batch(models, output_file):
    data = []

    for model in models:
        author = None

        if model.id and "/" in model.id:
            author = model.id.split("/")[0]

        data.append({
            "id": model.id,
            "author": author,
            "downloads": model.downloads,
            "likes": model.likes,
            "pipeline_tag": model.pipeline_tag,
        })

    output_path = Path(output_file)

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
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved {len(data)} models to {output_path}"
    )


def ingest_catalog_batches(
    batch_size=1000,
    max_batches=1
):
    models_iterator = iter(list_models())

    batch_number = 1

    while batch_number <= max_batches:

        batch = []

        for _ in range(batch_size):

            try:
                model = next(models_iterator)
                batch.append(model)

            except StopIteration:
                break

        if not batch:
            print("No more models found.")
            break

        output_file = (
            f"output/catalog/"
            f"batch_{batch_number:04d}.json"
        )

        save_model_batch(
            batch,
            output_file
        )

        print(
            f"Completed batch {batch_number}"
        )

        batch_number += 1