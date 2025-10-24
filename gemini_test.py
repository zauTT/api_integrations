import google.generativeai as genai

genai.configure(api_key="AIzaSyAD3wQTHhvNGjq2DViwOBKMYf8zGT2NMrI")

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = "Summarize today's crypto market in one fun sentence."
response = model.generate_content(
    prompt,
    request_options={"timeout": 60}
)
print(response.text)