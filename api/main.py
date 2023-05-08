
import modal 
import time

from typing import Any

MODEL_ID: str = "databricks/dolly-v2-3b"
CACHE_PATH: str = "/root/cache"


# Download model and cache into image. We'll download models from the Huggingface Hub
# and store them in our image. This skips the downloading of models during inference.
def download_model():
    _ = 3
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, use_cache=True, device_map="auto"
    )
    model.save_pretrained(CACHE_PATH, safe_serialization=True)

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, use_fast=True, use_cache=True
    )
    tokenizer.save_pretrained(CACHE_PATH, safe_serialization=True)


# Install dependencies.
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "jsonformer==0.11.0",
        "transformers",
        "torch",
        "accelerate",
        "safetensors",
        "fastapi"
    )
    .run_function(download_model)
)
stub = modal.Stub("jsonformer-example-3b", image=image)

if stub.is_inside(image):
    import warnings

    warnings.filterwarnings(
        "ignore", category=UserWarning, message="TypedStorage is deprecated"
    )

    from transformers import AutoModelForCausalLM, AutoTokenizer

@stub.cls(image=image, gpu="A10G", container_idle_timeout=300)
class DollyJsonformer:
    def __enter__(self):
        start_time = time.time()
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID,)
        print(f"Loading model took {time.time() - start_time} seconds")
        self.model = model
        self.tokenizer = tokenizer


    @modal.method()
    def generate(self, prompt: str, json_schema: dict[str, Any]) -> dict[str, Any]:
        from jsonformer import Jsonformer
        import json
        jsonformer = Jsonformer(self.model, self.tokenizer, json_schema, prompt, debug=True)
        print("Generating for", prompt, json.dumps(json_schema))
        generated_data = jsonformer()
        print("Generated", generated_data)
        return generated_data




@stub.local_entrypoint()
def main():
    dolly_jsonformer = DollyJsonformer()
    prompt = "Generate random plant information based on the following schema:"
    json_schema = {
        "type": "object",
        "properties": {
            "height_cm": {"type": "number"},
            "bearing_fruit": {"type": "boolean"},
            "classification": {
                "type": "object",
                "properties": {
                    "species": {"type": "string"},
                    "kingdom": {"type": "string"},
                    "family": {"type": "string"},
                    "genus": {"type": "string"},
                },
            },
        },
    }

    result = dolly_jsonformer.generate.call(prompt, json_schema)

    print(result)

@stub.function(
    container_idle_timeout=300,
    timeout=600,
)
@modal.asgi_app()
def web():
    from fastapi import FastAPI, Request, middleware
    from fastapi.middleware.cors import CORSMiddleware

    web_app = FastAPI()

    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    dolly_jsonformer = DollyJsonformer()

    @web_app.post("/generate")
    async def generate(request: Request):
        body = await request.json()
        prompt = body["prompt"]
        json_schema = body["json_schema"]
        result = dolly_jsonformer.generate.call(prompt, json_schema)
        return result

    return web_app