from app.services.huggingface_service import get_top_models

models = get_top_models(5)

for model in models:
    print(model)