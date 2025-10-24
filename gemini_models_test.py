from google import genai

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyAD3wQTHhvNGjq2DViwOBKMYf8zGT2NMrI")

# List available models
models = client.models.list()
for m in models:
    print(m.name)
