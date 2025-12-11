import os
from huggingface_hub import InferenceClient


from dotenv import load_dotenv
import os

load_dotenv()  # lê o .env

hf_token = os.environ.get("HF_TOKEN")


client = InferenceClient(
    provider="sambanova",
    api_key=hf_token,
)

result = client.feature_extraction(
    "Today is a sunny day and I will get some ice cream.",
    model="intfloat/e5-mistral-7b-instruct",
)

print(result)